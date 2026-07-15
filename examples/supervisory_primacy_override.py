#!/usr/bin/env python3
"""
supervisory_primacy_override.py
───────────────────────────────
Minimal public reference for *Supervisory Primacy* (Article 3):

  - Consequential actions pass a pre-execution gate (allow / hold / recommend).
  - The human operator may **override a hold**.
  - Every override is logged on the same append-only audit substrate.
  - The AI never silently bypasses the human; the human never acts without trail.

This is pedagogical code (stdlib only). It is NOT production MILO, NOT a
customer deployment, and contains NO proprietary process data.

Run:

    python3 supervisory_primacy_override.py

License: CC BY 4.0
Author: Jorge Enrique Flores Montano · JM Automated Solutions
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

AUDIT_PATH = Path(__file__).parent / "override_audit.jsonl"


def persist(event: dict) -> None:
    event = {"ts": time.time(), "id": str(uuid.uuid4()), **event}
    with AUDIT_PATH.open("a") as f:
        f.write(json.dumps(event) + "\n")
        f.flush()
        os.fsync(f.fileno())


@dataclass
class SupervisedBus:
    """Gate first; human override always available and always logged."""

    handlers: dict[str, Callable[[dict], dict]] = field(default_factory=dict)

    def register(self, target: str, handler: Callable[[dict], dict]) -> None:
        self.handlers[target] = handler

    def propose(self, target: str, payload: dict, operator: str) -> dict:
        """AI/system proposes; gate may hold. Returns gate decision."""
        proposal = {
            "kind": "proposal",
            "target": target,
            "payload": payload,
            "operator": operator,
        }
        persist(proposal)

        # Toy policy: "isolate_feeder" is high-consequence → hold for human.
        if target == "grid.isolate_feeder":
            decision = {
                "kind": "gate_result",
                "decision": "hold",
                "reason": "high-consequence isolation requires human confirmation",
                "target": target,
            }
            persist(decision)
            return decision

        decision = {"kind": "gate_result", "decision": "allow", "target": target}
        persist(decision)
        return self._execute(target, payload, operator, via="allow")

    def override_hold(
        self,
        target: str,
        payload: dict,
        operator: str,
        rationale: str,
    ) -> dict:
        """Human disposes after hold — Supervisory Primacy."""
        persist(
            {
                "kind": "human_override",
                "target": target,
                "payload": payload,
                "operator": operator,
                "rationale": rationale,
                "prior_decision": "hold",
            }
        )
        result = self._execute(target, payload, operator, via="override")
        return {"status": "override_logged", "result": result}

    def _execute(self, target: str, payload: dict, operator: str, via: str) -> dict:
        if target not in self.handlers:
            err = {"status": "error", "reason": f"no handler for {target!r}"}
            persist({"kind": "dispatch_error", **err})
            return err
        result = self.handlers[target](payload)
        persist(
            {
                "kind": "result",
                "target": target,
                "result": result,
                "operator": operator,
                "via": via,
            }
        )
        return result


def main() -> int:
    if AUDIT_PATH.exists():
        AUDIT_PATH.unlink()

    bus = SupervisedBus()
    bus.register("grid.isolate_feeder", lambda p: {"isolated": p.get("feeder_id")})
    bus.register("log.write", lambda p: {"logged": p.get("message")})

    print("─" * 60)
    print(" MILO supervisory-primacy override — minimal reference")
    print("─" * 60)

    print("\n1) Low-consequence log — allowed:")
    print("   ", bus.propose("log.write", {"message": "shift start"}, operator="op:jorge"))

    print("\n2) High-consequence isolation — held for human:")
    held = bus.propose(
        "grid.isolate_feeder",
        {"feeder_id": "F-17"},
        operator="op:jorge",
    )
    print("   ", held)
    assert held["decision"] == "hold"

    print("\n3) Human overrides hold with rationale — executed + audited:")
    out = bus.override_hold(
        "grid.isolate_feeder",
        {"feeder_id": "F-17"},
        operator="op:jorge",
        rationale="field crew confirmed clear; emergency isolation authorized",
    )
    print("   ", out)

    print("\nAudit trail:", AUDIT_PATH)
    print("Records:")
    for ln in AUDIT_PATH.read_text().splitlines():
        rec = json.loads(ln)
        print(f"  - {rec['kind']}: { {k: rec[k] for k in rec if k not in ('ts', 'id')} }")

    print("\nProperty: every hold and every override is reconstructable from the log.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
