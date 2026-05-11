# Examples — Reference Implementations of MILO Architectural Patterns

This directory contains minimal, dependency-free reference implementations of the architectural patterns described in the MILO manuscripts. They are *not* the production MILO orchestration system; they are sufficient to verify that the architectural discipline described in the papers can be implemented from first principles using only the Python standard library.

## persist_before_deliver.py

Demonstrates the four architectural mechanisms most central to MILO's audit-first command bus discipline:

1. **Persist-before-deliver** — every command is written to a durable, append-only audit log *before* it dispatches to its target. If the process terminates between dispatch and execution, replay of the audit log reconstructs exact state.
2. **Explicit-target dispatch** — every command has exactly one explicit target; no implicit resolvers, no opaque routing.
3. **Reflex predicates before fanout** — critical signals are evaluated against reflex predicates and may dispatch a halt command before subscribers see the underlying signal.
4. **Pre-execution gating with three outputs** — every consequential action passes through a pre-execution gate that returns one of `{allow, hold/block, recommend}`; operator override is always logged.

### Run

```bash
python3 persist_before_deliver.py
```

The script writes an audit trail to `./audit.jsonl` and prints the resulting state. Re-run the script and observe that the audit log appends rather than overwrites.

### Verify the audit trail

```bash
cat audit.jsonl | python3 -m json.tool --no-ensure-ascii | less
```

Each command in the audit log records the operator, the target, the payload, and (where applicable) the pre-execution gate decision and the eventual result. The trail is reconstructable post-hoc regardless of how the process terminated.

### What this is — and what it isn't

This reference implements only the architectural *substrate*: append-only continuity sufficient for post-hoc reconstructability. Production deployments in high-consequence environments add three further commitments (per Article 3 of the architectural series): **cryptographic chain-of-custody** for audit records, **custodial separation** between the orchestrator and an independent integrity service, and **external WORM replication** to a sink under separate administrative control. Those hardening commitments are required for the high-consequence deployment posture; they are not implemented here.

## Related reading

- [Article 2 — Latency-Aware Authentication](../articles/02-Latency-Aware-Authentication.md) — formal sketch of the pre-execution gate, consequence-class composition with ISA/IEC 62443 SL tiers.
- [Article 3 — Supervisory Primacy](../articles/03-Supervisory-Primacy.md) — full audit-substrate threat model and operator-authority commitments.
- [Article 4 — Eight Structural Principles](../articles/04-Eight-Structural-Principles.md) — the eight design constraints that govern this discipline.

---

© 2026 Jorge Enrique Flores Montano · JM Automated Solutions · ~MILO™ is a trademark of Jorge Enrique Flores Montano · USPTO Serial No. 99706004 · Patent Pending.
