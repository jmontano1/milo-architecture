# Evaluation guide — what is real, what is original, where to verify

This page exists so a reviewer can establish, quickly and without ambiguity, **what in this
repository is built versus design-stage, what is original versus established, and where every
claim is anchored.** It is written to be read before the papers, not after.

## 1. What MILO is, in one sentence

An architecture for AI in high-consequence environments (grids, nuclear, advanced
manufacturing, supervised autonomy) engineered for **viability** — remaining operational,
auditable, and human-controllable under conditions it was never trained to expect — rather
than for prediction accuracy.

## 2. Built vs. design-stage

| Layer | State | Where to verify |
|---|---|---|
| Audit-first command flow (persist-before-deliver) | ✅ **runnable reference** | [`examples/persist_before_deliver.py`](examples/persist_before_deliver.py) — run it; inspect `audit.jsonl` |
| Pre-execution gate (allow · hold · recommend) | ✅ runnable reference | same example, steps 1–3 |
| Single-target dispatch | ✅ runnable reference | same example, step 5 |
| Reflex predicate → emergency halt | ✅ runnable reference | same example, step 4 |
| Inference gateway · specialist-agent fleet · health supervisor · coordination ledger · adaptation plane | 🔶 **design-stage** | [`ARCHITECTURE.md`](ARCHITECTURE.md) §2–§3 (described, not implemented here) |
| Operator-cognitive layer (Principles 7–8) | 🔶 design-stage, **original** | [`PRINCIPLES.md`](PRINCIPLES.md); [Article 4](articles/04-Eight-Structural-Principles.md) |

**Source-code status:** all source-code rights for the underlying MILO implementation are
reserved; patent pending (USPTO Serial No. 99706004). This repository releases the
architectural manuscripts (CC BY 4.0) and one minimal reference, not the production codebase.

## 3. Original vs. established

The eight structural principles deliberately separate borrowed law from original contribution:

- **Established laws applied as design constraints (Principles 1–6):** Second Law of
  Thermodynamics, Ashby's Law of Requisite Variety, Shannon information theory, Principle of
  Least Action (single-target dispatch), Lyapunov-style bounded response, power-law /
  tail-event architecture. *Verifiable against the cited public standards and literature.*
- **Original frameworks (Principles 7–8), proposed by the author:** Individual-Baseline
  Variance Modeling and Precision Perturbation Without Variance Compression — the
  operator-cognitive layer. *These are the novel claims; everything else is grounding.*

## 4. External anchors (independently checkable)

- **Persistent identifiers:** concept DOI [`10.5281/zenodo.20117025`](https://doi.org/10.5281/zenodo.20117025); five per-article DOIs (see [README](README.md) paper table).
- **Standards grounding:** NIST SP 800-82r3, NIST SP 800-90B, ISA/IEC 62443, EU AI Act
  Article 14, NIST AI RMF 1.0 (Appendix C), CISA Critical Manufacturing priorities.
- **Trademark / patent:** ~MILO™ USPTO Serial No. 99706004 (Class 009); patent pending.
- **Federal context:** submitted to the U.S. DOE Genesis Mission (EO 14363).
- **Author:** Jorge Enrique Flores Montano · [ORCID 0009-0003-1859-8418](https://orcid.org/0009-0003-1859-8418).

## 5. Operational integrity constraints (how to falsify "is this safe-by-design?")

The architecture commits to eight invariants meant to be enforced as code-level invariants,
not toggleable policy: no coercion; individual baseline only (never a population norm); no
surveillance architecture; operator authority preserved; operational transparency; data
sovereignty; override always available; independent oversight. A reviewer can test any design
or implementation against this list — see the full statements in [README](README.md#eight-operational-integrity-constraints).
