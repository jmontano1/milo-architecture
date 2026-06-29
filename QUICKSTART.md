# Quickstart — run the MILO reference in 60 seconds

This repository is an **architectural reference**. Most of MILO is described at the
architectural level (see [`ARCHITECTURE.md`](ARCHITECTURE.md)); **one** mechanism is provided
as a minimal, runnable reference so the central claim — *audit precedes delivery* — can be
executed and inspected, not just read.

## Run it

No dependencies. Python 3.8+ standard library only.

```bash
git clone https://github.com/jmontano1/milo-architecture
cd milo-architecture
python3 examples/persist_before_deliver.py
```

## What you should see

```
1) Routine force application (50 N):
    {'applied_n': 50}
2) Near-threshold force (90 N):
    {'status': 'recommended_alternative', 'alternative': {'target': 'actuator.apply_force', 'payload': {'force_n': 80}}}
3) Over-threshold force (150 N):
    {'status': 'blocked', 'reason': 'force_n=150 exceeds safety threshold 100 N'}
4) Critical signal arrives → reflex dispatches emergency halt
5) Unknown target:
    {'status': 'error', 'reason': "no handler for 'nonexistent.target'"}
```

Then inspect the append-only audit trail it produced:

```bash
cat examples/audit.jsonl | python3 -m json.tool --no-ensure-ascii
```

## What this demonstrates (and what it does not)

`examples/persist_before_deliver.py` (~150 lines, standard library) implements **four** of the
architecture's mechanisms, end to end:

| Mechanism | What you observe above |
|---|---|
| **Audit-first, persist-before-deliver** | every command is written to `audit.jsonl` *before* it dispatches |
| **Pre-execution gate** (allow · hold · recommend) | 50 N allowed · 90 N → recommended alternative · 150 N → blocked |
| **Single-target dispatch** | unknown target errors explicitly — no implicit resolver |
| **Reflex predicate** | a critical signal short-circuits to an emergency halt before normal fanout |

> **It is a reference, not the production system.** The remaining subsystems described in
> [`ARCHITECTURE.md`](ARCHITECTURE.md) §2 (inference gateway, specialist-agent fleet, health
> supervisor, coordination ledger, adaptation plane) are **design-stage** and are not in this
> repository. See [`EVALUATION.md`](EVALUATION.md) for the exact built-vs-designed boundary.
