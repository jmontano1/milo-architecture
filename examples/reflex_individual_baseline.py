#!/usr/bin/env python3
"""MILO — Behavioral-Baseline Reflex  (minimal reference)

A fast, pre-reasoning reflex arc. Body analogy: a spinal reflex ADDS a protective
action (pull the hand from heat) — it does not switch off the brain. Here, a sharp
deviation from the user's OWN interaction baseline ADDS safeguards around the
reasoning engine; it never blocks or preempts the operator.

WHAT THIS IS:  a per-user, individual-baseline anomaly gate. It learns only this
  individual's rolling baseline for a few cheap signals and raises a 3-level reflex
  state when the current turn deviates sharply from that learned baseline.

WHAT THIS IS NOT:  it does not detect emotion, stress, distress, or intent — such
  claims would be unvalidated. It detects *deviation from the user's established
  pattern* and responds conservatively. It is a reference, not the production system.

Honors MILO's stated integrity constraints (see ../EVALUATION.md, ../README.md):
  * Individual baseline only — no fixed or population thresholds (Principle 7).
  * Operator authority is the invariant — reasoning ALWAYS proceeds; the reflex only
    ADDS safeguards, never narrows or preempts options (Principle 8 / Constraint #4).
  * No surveillance — the baseline is in-memory and bounded; it is never persisted as
    a profile. Only the reflex DECISION is appended to an audit log (audit-first),
    never a dossier on the person (Constraints #3, #6, #7).
"""

from __future__ import annotations

import json
import math
import os
import time
from collections import deque

AUDIT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reflex_audit.jsonl")

NORMAL, CAUTION, HEIGHTENED = "NORMAL", "CAUTION", "HEIGHTENED"
_RANK = {NORMAL: 0, CAUTION: 1, HEIGHTENED: 2}
_STEP_DOWN = {HEIGHTENED: CAUTION, CAUTION: NORMAL, NORMAL: NORMAL}


class RunningBaseline:
    """Rolling mean/std over ONE individual's own recent values (bounded window)."""

    def __init__(self, window: int = 20, warmup: int = 5) -> None:
        self.warmup = warmup
        self._v: deque = deque(maxlen=window)

    def ready(self) -> bool:
        return len(self._v) >= self.warmup

    def zscore(self, x: float) -> float:
        if not self.ready():
            return 0.0
        mean = sum(self._v) / len(self._v)
        sd = math.sqrt(sum((v - mean) ** 2 for v in self._v) / max(1, len(self._v) - 1))
        return 0.0 if sd < 1e-9 else (x - mean) / sd

    def observe(self, x: float) -> None:
        self._v.append(float(x))


class BehavioralBaselineReflex:
    """Pre-reasoning reflex: escalates on individual-baseline deviation, only ever
    ADDING safeguards. `observe()` returns a decision; reasoning always proceeds."""

    def __init__(self, signals=("message_length", "reply_delay", "caps_ratio"),
                 caution_z: float = 1.5, heightened_z: float = 2.5,
                 calm_to_clear: int = 2) -> None:
        self.signals = tuple(signals)
        self.baselines = {s: RunningBaseline() for s in self.signals}
        self.caution_z = caution_z
        self.heightened_z = heightened_z
        self.calm_to_clear = calm_to_clear
        self.level = NORMAL
        self._calm = 0

    def observe(self, sample: dict) -> dict:
        warming = not all(b.ready() for b in self.baselines.values())
        devs = {s: abs(self.baselines[s].zscore(float(sample.get(s, 0.0)))) for s in self.signals}
        max_dev = max(devs.values()) if devs else 0.0

        # proposed level from THIS turn's deviation against the person's own baseline
        if warming:
            proposed = NORMAL  # never escalate before the individual's baseline is known
        elif max_dev >= self.heightened_z:
            proposed = HEIGHTENED
        elif max_dev >= self.caution_z:
            proposed = CAUTION
        else:
            proposed = NORMAL

        # hysteresis: escalate immediately; de-escalate only after sustained calm
        if _RANK[proposed] > _RANK[self.level]:
            self.level, self._calm = proposed, 0
        elif proposed == NORMAL:
            self._calm += 1
            if self._calm >= self.calm_to_clear:
                self.level, self._calm = _STEP_DOWN[self.level], 0
        else:
            self._calm = 0  # still elevated — hold the level, do not decay

        # learn AFTER deciding, so a spike does not immediately mask itself
        for s in self.signals:
            self.baselines[s].observe(float(sample.get(s, 0.0)))

        decision = {
            "ts": round(time.time(), 3),
            "level": self.level,
            "warming_up": warming,
            "max_deviation_sd": round(max_dev, 2),
            "deviations_sd": {k: round(v, 2) for k, v in devs.items()},
            "safeguards": self._safeguards(),
            "reasoning_proceeds": True,  # INVARIANT — the reflex never blocks the operator
        }
        _append_audit(decision)
        return decision

    def _safeguards(self) -> list:
        if self.level == HEIGHTENED:
            return ["require_explicit_confirmation", "simplify_output",
                    "state_uncertainty", "audit_action_for_review"]
        if self.level == CAUTION:
            return ["soften_language", "add_clarity"]
        return []


def _append_audit(decision: dict) -> None:
    # audit-first: persist the reflex DECISION, never a behavioral profile of the person
    with open(AUDIT_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(decision, ensure_ascii=False) + "\n")


def _demo() -> None:
    line = "─" * 60
    print(line + "\n MILO behavioral-baseline reflex — minimal reference\n" + line)
    open(AUDIT_PATH, "w").close()  # fresh audit trail for the demo
    reflex = BehavioralBaselineReflex()

    steady = [
        {"message_length": 42, "reply_delay": 9, "caps_ratio": 0.04},
        {"message_length": 38, "reply_delay": 12, "caps_ratio": 0.06},
        {"message_length": 51, "reply_delay": 8, "caps_ratio": 0.03},
        {"message_length": 45, "reply_delay": 11, "caps_ratio": 0.05},
        {"message_length": 40, "reply_delay": 10, "caps_ratio": 0.04},
        {"message_length": 47, "reply_delay": 9, "caps_ratio": 0.05},
    ]
    print("\n1) Learn this person's OWN baseline (no population norms):")
    for s in steady:
        d = reflex.observe(s)
        print("   len=%3d delay=%3d caps=%.2f  -> %-10s (warming=%s)"
              % (s["message_length"], s["reply_delay"], s["caps_ratio"], d["level"], d["warming_up"]))

    print("\n2) A turn that deviates sharply from THEIR pattern:")
    d = reflex.observe({"message_length": 3, "reply_delay": 95, "caps_ratio": 0.0})
    print("   len=  3 delay= 95 caps=0.00  -> %s  (max %.1f SD from their own norm)"
          % (d["level"], d["max_deviation_sd"]))
    print("      safeguards ADDED : %s" % d["safeguards"])
    print("      reasoning_proceeds: %s   <- operator is never preempted" % d["reasoning_proceeds"])

    print("\n3) Sustained return to their normal pattern (de-escalates with hysteresis):")
    for s in [{"message_length": 44, "reply_delay": 10, "caps_ratio": 0.05},
              {"message_length": 46, "reply_delay": 9, "caps_ratio": 0.04},
              {"message_length": 41, "reply_delay": 11, "caps_ratio": 0.05},
              {"message_length": 48, "reply_delay": 10, "caps_ratio": 0.04}]:
        d = reflex.observe(s)
        print("   len=%3d delay=%3d caps=%.2f  -> %s" % (s["message_length"], s["reply_delay"], s["caps_ratio"], d["level"]))

    print("\nReflex DECISIONS (not a profile) were audited to: %s" % AUDIT_PATH)
    print("Replay:  cat examples/reflex_audit.jsonl | python3 -m json.tool --no-ensure-ascii")


if __name__ == "__main__":
    _demo()
