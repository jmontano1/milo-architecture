# Examples — Reference Implementations of MILO Architectural Patterns

**Toy demos; not connected to any PLC.** Targets named `plc.inspection_flag.*` (release / hold / reject) are in-memory stand-ins for inspection-tier flags; scores are toy values standing in for the vision vendor's model scores. Safety functions (E-stop, interlocks, safety PLC/SIS) are outside MILO and are never commanded.

This directory contains minimal, dependency-free reference implementations of the architectural patterns described in the MILO manuscripts. They are *not* the production MILO orchestration system; they are sufficient to verify that the architectural discipline described in the papers can be implemented from first principles using only the Python standard library.

**Self-check (CI entrypoint):**

```bash
python3 test_reference.py
```

## persist_before_deliver.py

Demonstrates four mechanisms central to MILO's audit-first command bus discipline:

1. **Persist-before-deliver** — every command is written to a durable, append-only audit log *before* it dispatches.
2. **Explicit-target dispatch** — exactly one explicit target; no opaque routing.
3. **Reflex predicates before fanout** — a critical signal may request a hold of the affected unit before subscribers see it.
4. **Pre-execution gating** — `{allow, hold/block, recommend}` before consequential action.

```bash
python3 persist_before_deliver.py
```

## supervisory_primacy_override.py

Demonstrates **Supervisory Primacy** (Article 3): a proposed reject flag is **held** for a named person; the person **authorizes** it with a logged rationale; the audit trail reconstructs the full sequence.

```bash
python3 supervisory_primacy_override.py
```

## What this is — and what it isn't

These references implement the architectural *substrate* only. Production high-consequence deployments add cryptographic chain-of-custody, custodial separation, and external WORM replication (Article 3). They are not implemented here.

**Never committed here:** plant data, plant logic, credentials, NDA materials, or MILO source code. MILO is pre-commercial; no customer deployments exist.

## Related reading

- [MECHANISM_MAP.md](../MECHANISM_MAP.md) — mechanism → paper → file
- [Article 2 — Latency-Aware Authentication](../articles/02-Latency-Aware-Authentication.md)
- [Article 3 — Supervisory Primacy](../articles/03-Supervisory-Primacy.md)
- [Article 4 — Eight Structural Principles](../articles/04-Eight-Structural-Principles.md)

---

© 2026 Jorge Enrique Flores Montano · JM Automated Solutions, LLC · Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application Serial No. 99706004.
