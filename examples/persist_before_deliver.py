#!/usr/bin/env python3
"""
persist_before_deliver.py
─────────────────────────
Reference implementation of MILO's audit-first command bus discipline at the
publication level. Demonstrates four architectural mechanisms described in
the manuscripts:

  1. Persist-before-deliver — every command is written to a durable,
     append-only audit log BEFORE it dispatches to its target. If the
     process terminates between dispatch and execution, replay of the
     audit log reconstructs exact state.

  2. Explicit-target dispatch — every command has exactly one explicit
     target. No implicit resolvers, no opaque routing magic.

  3. Reflex predicates before fanout — critical signals are evaluated
     against reflex predicates and may request a hold of the affected unit
     before subscribers see the underlying signal.

  4. Pre-execution gating with three outputs — every consequential action
     passes through a pre-execution gate that returns one of {allow,
     hold/block, recommend}. Operator override is always logged.

TOY DEMO; NOT CONNECTED TO ANY PLC. Targets named plc.inspection_flag.*
are in-memory stand-ins for inspection-tier flags (release / hold / reject).
Scores are toy values standing in for the vision vendor's model scores.
Safety functions (E-stop, interlocks, safety PLC/SIS) are outside MILO and
are never commanded.

This is a minimal, dependency-free reference. It is NOT the production
MILO implementation. It is sufficient to verify that the architectural
discipline described in the manuscripts can produce a reconstructable
audit trail from first principles.

Run:

    python3 persist_before_deliver.py

The script writes audit records to ./audit.jsonl and prints the
resulting state. Re-run the script and observe that the audit log
appends rather than overwrites.

License: CC BY 4.0
Author: Jorge Enrique Flores Montano · JM Automated Solutions, LLC
Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026;
No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application
Serial No. 99706004.
"""

from __future__ import annotations

import json
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

AUDIT_PATH = Path(__file__).parent / "audit.jsonl"


# ── Audit substrate ────────────────────────────────────────────────────
def persist(event: dict) -> None:
    """Append a single record to the durable audit log with fsync.

    Append-only continuity is the minimum architectural property required
    for post-hoc reconstructability. Production hardening adds
    cryptographic chain-of-custody, custodial separation between the
    orchestrator and an independent integrity service, and replicated
    audit trails to external write-once-read-many sinks (cf. NIST SP
    800-92 on log management and NIST SP 800-53 control AU-9 on
    protection of audit information). This reference implements only
    the substrate property; hardening is a separate deployment
    commitment.
    """
    event = {"ts": time.time(), "id": str(uuid.uuid4()), **event}
    with AUDIT_PATH.open("a") as f:
        f.write(json.dumps(event) + "\n")
        f.flush()
        import os
        os.fsync(f.fileno())


# ── Command bus ────────────────────────────────────────────────────────
@dataclass
class CommandBus:
    """Explicit-target dispatch with persist-before-deliver discipline."""

    handlers: dict[str, Callable[[dict], dict]] = field(default_factory=dict)
    pre_gate: Callable[[dict], dict] | None = None

    def register(self, target: str, handler: Callable[[dict], dict]) -> None:
        if target in self.handlers:
            raise ValueError(f"target {target!r} already registered")
        self.handlers[target] = handler

    def dispatch(self, target: str, payload: dict, operator: str) -> dict:
        # 1. Persist-before-deliver: audit BEFORE any side-effect.
        cmd = {"kind": "command", "target": target, "payload": payload, "operator": operator}
        persist(cmd)

        # 2. Pre-execution gate: allow / hold / recommend.
        if self.pre_gate is not None:
            gate_result = self.pre_gate(cmd)
            persist({"kind": "gate_result", "for_command": target, **gate_result})
            if gate_result["decision"] == "hold":
                return {"status": "held", "reason": gate_result["reason"]}
            if gate_result["decision"] == "recommend":
                # A "recommend" output surfaces a safer alternative; the
                # operator must re-issue, so we stop here.
                return {"status": "recommended_alternative", "alternative": gate_result["alternative"]}

        # 3. Explicit-target dispatch: exactly one handler per target.
        if target not in self.handlers:
            persist({"kind": "dispatch_error", "target": target, "reason": "unregistered"})
            return {"status": "error", "reason": f"no handler for {target!r}"}

        result = self.handlers[target](payload)
        persist({"kind": "result", "target": target, "result": result})
        return result


# ── Signal substrate with reflex predicates ────────────────────────────
@dataclass
class SignalBus:
    """Persist each signal, evaluate reflex predicates, then fan out."""

    reflexes: list[Callable[[dict], dict | None]] = field(default_factory=list)
    subscribers: list[Callable[[dict], None]] = field(default_factory=list)
    bus: CommandBus | None = None

    def emit(self, signal: dict) -> None:
        persist({"kind": "signal", **signal})

        # Reflex predicates run BEFORE fanout — they can short-circuit
        # the signal at the carrier level (Shannon Principle 3 in
        # Article 4 of the architectural series).
        for reflex in self.reflexes:
            reflex_cmd = reflex(signal)
            if reflex_cmd is not None and self.bus is not None:
                persist({"kind": "reflex_fired", "from_signal": signal.get("name")})
                self.bus.dispatch(**reflex_cmd, operator="reflex:auto")

        # Only then fan out to general subscribers.
        for sub in self.subscribers:
            sub(signal)


# ── Demo wiring (toy demo; not connected to any PLC) ──────────────────
UNCERTAIN_BAND = (0.40, 0.60)  # toy values for the demo only


def main() -> None:
    bus = CommandBus()

    # Pre-execution gate: allow / hold / recommend on a proposed release flag.
    def gate(cmd: dict) -> dict:
        if cmd["target"] == "plc.inspection_flag.release":
            score = cmd["payload"].get("vendor_score", 0.0)
            if cmd["payload"].get("consequence") == "high":
                return {
                    "decision": "hold",
                    "reason": "high-consequence unit held for a named person",
                }
            if UNCERTAIN_BAND[0] <= score <= UNCERTAIN_BAND[1]:
                return {
                    "decision": "recommend",
                    "alternative": {
                        "target": "plc.inspection_flag.hold",
                        "payload": {"unit_id": cmd["payload"].get("unit_id")},
                    },
                    "reason": "vendor score in uncertain band; recommend hold for per-unit review",
                }
        return {"decision": "allow"}

    bus.pre_gate = gate

    # Register exactly ONE handler per target. No implicit routing.
    # Handlers only record an in-memory flag; nothing is sent to a PLC.
    for flag in ("release", "hold", "reject"):
        bus.register(
            f"plc.inspection_flag.{flag}",
            lambda p, flag=flag: {"flag_written": flag, "unit_id": p.get("unit_id")},
        )
    bus.register("log.write", lambda p: {"logged": p["message"]})

    # Signal substrate with a reflex that requests a hold on critical signals.
    signals = SignalBus(bus=bus)

    def reflex_critical_signal_hold(signal: dict) -> dict | None:
        if signal.get("severity") == "critical":
            return {"target": "plc.inspection_flag.hold", "payload": {"unit_id": signal.get("unit_id")}}
        return None

    signals.reflexes.append(reflex_critical_signal_hold)

    print("─" * 60)
    print(" MILO persist-before-deliver — toy demo (not connected to any PLC)")
    print("─" * 60)
    print()
    print("Audit log: ", AUDIT_PATH)
    print()

    # 1) Confident score, routine unit — allowed, logged, flag written.
    print("1) Confident vendor score, routine unit (U-0001):")
    print("   ", bus.dispatch("plc.inspection_flag.release",
                             {"unit_id": "U-0001", "vendor_score": 0.97, "consequence": "routine"},
                             operator="op:reviewer"))

    # 2) Uncertain score — gate recommends a hold instead.
    print("2) Vendor score in uncertain band (U-0002):")
    print("   ", bus.dispatch("plc.inspection_flag.release",
                             {"unit_id": "U-0002", "vendor_score": 0.52, "consequence": "routine"},
                             operator="op:reviewer"))

    # 3) High-consequence unit — gate holds for a named person.
    print("3) High-consequence unit (U-0003):")
    print("   ", bus.dispatch("plc.inspection_flag.release",
                             {"unit_id": "U-0003", "vendor_score": 0.95, "consequence": "high"},
                             operator="op:reviewer"))

    # 4) Critical signal arrives — reflex requests a hold before subscribers see it.
    print("4) Critical signal arrives → reflex requests a hold of the affected unit:")
    signals.emit({"name": "vendor_score_drift", "severity": "critical", "unit_id": "U-0004"})

    # 5) Unknown target — explicit-target dispatch refuses.
    print("5) Unknown target:")
    print("   ", bus.dispatch("nonexistent.target", {}, operator="op:reviewer"))

    print()
    print("Done. Audit trail written to:", AUDIT_PATH)
    print("Replay it with:  cat audit.jsonl | python3 -m json.tool --no-ensure-ascii")
    print()
    print("Each command was persisted BEFORE it dispatched. If this process")
    print("had crashed at any point, replay of audit.jsonl would reconstruct")
    print("exact state.")


if __name__ == "__main__":
    sys.exit(main())
