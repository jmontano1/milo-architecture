# ~MILO™ — Modular Intelligent Learning Orchestrator

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20117025.svg)](https://doi.org/10.5281/zenodo.20117025)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![reference-ci](https://github.com/jmontano1/milo-architecture/actions/workflows/ci.yml/badge.svg)](https://github.com/jmontano1/milo-architecture/actions/workflows/ci.yml)

> *MILO does not predict the future. It remains viable in any future.*

**Human-in-the-loop disposition layer for automated inspection in regulated manufacturing.**

> **Scope of the proposed endeavor.** MILO is a human-in-the-loop disposition layer above the plant PLC for automated inspection (accept/reject/hold) on regulated food, pharmaceutical and medical-device lines. The papers below discuss general architectural principles; applications outside industrial inspection are research discussion, not the product scope.

| | |
|---|---|
| **DOI** | Concept DOI [`10.5281/zenodo.20117024`](https://doi.org/10.5281/zenodo.20117024) (all versions); v1.0.0 DOI [`10.5281/zenodo.20117025`](https://doi.org/10.5281/zenodo.20117025) |
| **Patent / trademark** | Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application Serial No. 99706004. (Trademark filed March 16, 2026; intent-to-use, Class 009.) |
| **Inventor** | Jorge Enrique Flores Montano · Founder, JM Automated Solutions, LLC · [ORCID 0009-0003-1859-8418](https://orcid.org/0009-0003-1859-8418) |
| **License (docs)** | [CC BY 4.0](LICENSE) · *All source-code rights reserved* |
| **Contact** | jmontano@jmautomated.com |
| **Verify claims** | [VERIFY.md](VERIFY.md) · [CLAIMS.md](CLAIMS.md) · [STANDARDS_CROSSWALK.md](STANDARDS_CROSSWALK.md) · [MECHANISM_MAP.md](MECHANISM_MAP.md) |
| **Independent reviewers** | **Start here → [FOR_INDEPENDENT_REVIEWERS.md](FOR_INDEPENDENT_REVIEWERS.md)** |

### Arrived from a paper or exhibit that cites this repository?

This GitHub URL is the public architectural reference printed alongside the MILO article series
and related materials. Open **[FOR_INDEPENDENT_REVIEWERS.md](FOR_INDEPENDENT_REVIEWERS.md)** first
(60-second path: VERIFY → CLAIMS → demos → articles/DOIs). No login required.

**Quick self-check (no network, no secrets):**

```bash
python3 examples/test_reference.py
```

---

## What MILO is

MILO is a **human-in-the-loop disposition layer above the plant PLC** for automated inspection on regulated food, pharmaceutical and medical-device lines. Perception scores come from the vision vendor's models; MILO proposes a disposition, and a named person or a rule approved in advance at commissioning disposes. MILO's only command path is one conduit to the plant PLC, which writes inspection-tier flags; MILO has no connection to the safety PLC. If MILO or a record write fails, MILO issues no command and the plant PLC's own fail-safe default applies. The plant-floor design is set out in the MILO Methods Statement.

The dominant paradigm in AI today optimizes for **prediction accuracy** against an expected future distribution. MILO is designed for **viability** — the capacity to remain operational, auditable, and human-controllable under operational futures the system was not trained to expect. The architectural mechanisms that produce viability — audit-first command flow, modular subsystems with strict separation of concerns, bounded recovery pathways, tail-event preparation, reviewed-outcome learning, and preserved operator authority — together produce a system that does not require accurate prediction to remain useful.

MILO references established standards as design intent (NIST SP 800-82r3 for operational-technology security, NIST SP 800-90B for cryptographic entropy, ISA/IEC 62443 for industrial cybersecurity, EU AI Act Article 14 for human oversight, NIST AI RMF 1.0 for AI risk management), not as a certification or compliance claim; compliance is assessed at each plant's commissioning and validation. It draws on the cybernetics, control theory, information theory, and resilience-engineering lineages of Beer, Ashby, Shannon, Lyapunov, Hollnagel, Taleb, and Clauset.

---

## Architecture at a glance

```mermaid
flowchart LR
    OP[Human Operator]
    GATE[Pre-Execution Gate<br/>allow · hold · recommend]
    BUS[Audit-First Command Bus<br/><i>persist-before-deliver</i>]
    SUB[Discrete Single-Responsibility<br/>Subsystems]
    SIG[Audit-First Signal Substrate<br/>reflex predicates before fanout]
    REFLEX[Critical-Signal Hold<br/>hold request to plant PLC]
    AUDIT[(Append-Only Audit Log<br/>+ cryptographic chain-of-custody<br/>+ custodial separation<br/>+ external WORM replication)]

    OP -->|"consequential<br/>action"| GATE
    GATE -->|allow| BUS
    GATE -.->|hold / recommend| OP
    BUS -->|"explicit-target<br/>dispatch"| SUB
    SUB -->|signals| SIG
    SIG -->|"critical"| REFLEX
    SIG -.->|"non-critical<br/>fanout"| SUB
    REFLEX -->|hold request| BUS

    BUS -.persists.-> AUDIT
    SIG -.persists.-> AUDIT
    REFLEX -.persists.-> AUDIT
    GATE -.persists.-> AUDIT
```

Every visible state in the architecture is backed by a persisted event. Audit precedes delivery; explicit-target dispatch precludes implicit routing; reflex predicates short-circuit critical signals before subscribers see them; operator override is always available and always logged. Safety functions (E-stop, interlocks, safety PLC/SIS) are outside MILO and are never commanded by it. A minimal runnable reference implementing four of these mechanisms in ~150 lines of standard-library Python is provided in [`examples/persist_before_deliver.py`](examples/persist_before_deliver.py).

For where the plant-floor design is documented, see [**ARCHITECTURE.md**](ARCHITECTURE.md).

---

## Architectural papers

Five standalone papers articulate MILO's architecture, each grounded in established external sources. **All five are self-published preprints (Zenodo); not peer-reviewed.** Two PDF formats are provided for every paper:

- **Standard PDF** (`pdfs/`) — rendered from markdown via ReportLab. Primary citation-anchor version with inline architectural figures, hyperlinked references, and PDF bookmarks.
- **Scholarly LaTeX PDF** (`pdfs-singlecol/`) — single-column scholarly typesetting via pandoc + tectonic with the LaTeX `article` class. The full LaTeX source bundle (with figures) is in [`latex-sources/`](latex-sources/).

| # | Title | DOI | Standard | LaTeX | Domain |
|---|---|---|:---:|:---:|---|
| 1 | [Independence as an Architectural Property: A Research Direction for Multi-Source Cryptographic Entropy](articles/01-Independence-as-Architectural-Property.md) | [10.5281/zenodo.20117647](https://doi.org/10.5281/zenodo.20117647) | [📄](pdfs/MILO_Article_01_ThermalEntropy.pdf) | [📑](pdfs-singlecol/MILO_Article_01_ThermalEntropy_singlecol.pdf) | Cryptographic entropy · TRNG · NIST SP 800-90B |
| 2 | [Latency-Aware Authentication in Industrial Control Environments](articles/02-Latency-Aware-Authentication.md) | [10.5281/zenodo.20117651](https://doi.org/10.5281/zenodo.20117651) | [📄](pdfs/MILO_Article_02_LatencyAuth.pdf) | [📑](pdfs-singlecol/MILO_Article_02_LatencyAuth_singlecol.pdf) | OT cybersecurity · ISA/IEC 62443 · NIST SP 800-82r3 |
| 3 | [Supervisory Primacy: Human-in-the-Loop AI Orchestration for High-Consequence Domains](articles/03-Supervisory-Primacy.md) | [10.5281/zenodo.20117662](https://doi.org/10.5281/zenodo.20117662) | [📄](pdfs/MILO_Article_03_SupervisoryPrimacy.pdf) | [📑](pdfs-singlecol/MILO_Article_03_SupervisoryPrimacy_singlecol.pdf) | AI governance · HITL · EU AI Act Article 14 |
| 4 | [Eight Structural Principles for Adaptive AI Architecture](articles/04-Eight-Structural-Principles.md) | [10.5281/zenodo.20117703](https://doi.org/10.5281/zenodo.20117703) | [📄](pdfs/MILO_Article_04_GoverningPrinciples.pdf) | [📑](pdfs-singlecol/MILO_Article_04_GoverningPrinciples_singlecol.pdf) | Adaptive AI theory · Cybernetics · Control theory |
| 5 | [Adaptive Resilience: Why AI Systems Must Remain Viable in Any Future](articles/05-Adaptive-Resilience.md) | [10.5281/zenodo.20117716](https://doi.org/10.5281/zenodo.20117716) | [📄](pdfs/MILO_Article_05_AdaptiveResilience.pdf) | [📑](pdfs-singlecol/MILO_Article_05_AdaptiveResilience_singlecol.pdf) | AI resilience · Viability · Non-stationary environments |

**Concept DOI** (whole architectural reference, all versions): [10.5281/zenodo.20117024](https://doi.org/10.5281/zenodo.20117024) · **v1.0.0 DOI:** [10.5281/zenodo.20117025](https://doi.org/10.5281/zenodo.20117025)

See [`articles/README.md`](articles/README.md) for full abstracts of each paper.

---

## Eight structural principles

The MILO architecture is governed by eight design-time constraints. Six are established physical, informational, control-theoretic, and statistical laws applied as architectural design constraints. Two are original frameworks proposed by the author for the operator-cognitive performance layer of high-consequence systems.

1. **Second Law of Thermodynamics** — entropy treated as an architectural diagnostic signal, not a fault to be suppressed.
2. **Ashby's Law of Requisite Variety** — a regulator must possess variety at least equal to the system it regulates; implemented as a fleet of specialist agents, not a single generalist.
3. **Shannon Information Theory** — variance reduction occurs at the signal-carrier level, not redundantly at each consumer.
4. **Principle of Least Action — Single-Target Dispatch** — every command has exactly one explicit target; no implicit resolvers, no opaque dispatchers.
5. **Lyapunov-Style Bounded Response** — every adaptive subsystem admits an explicit halt-and-resume pathway; adaptation that drifts unboundedly is failure, not learning.
6. **Power-Law Distribution Architecture** — engineered for the 99th-percentile event, not the median.
7. **Individual-Baseline Variance Modeling** *(original)* — operator-layer interventions calibrated against the individual's own established performance baseline, never a population norm.
8. **Precision Perturbation Without Variance Compression** *(original)* — operator-layer interventions shift probability mass toward high-reliability decision outputs while preserving operator authority and the variability that *is* the operator's adaptive intelligence.

See [PRINCIPLES.md](PRINCIPLES.md) for fuller treatments, and [Article 4](articles/04-Eight-Structural-Principles.md) for the full synthesis.

---

## Eight operational integrity constraints

Architectural commitments designed to be implemented as **enforceable code-level invariants** in deployment builds — not as runtime policy or configuration that can be toggled off under operational pressure.

1. **No coercion, ever** — the system issues recommendations, never compels.
2. **Individual baseline only** — measurements compared against the operator's own baseline, never against a population norm, government standard, or productivity target.
3. **No surveillance architecture** — designed as a performance-support tool, not a monitoring infrastructure.
4. **Operator authority is the invariant** — the system expands effective decision options; it never narrows or preempts them.
5. **Operational transparency** — every recommendation includes a plain-language explanation.
6. **Data sovereignty** — operator-layer data belongs to the institutional program under documented data governance.
7. **Override always available** — operators can override any recommendation at any time, with overrides logged for audit but never used for adverse personnel action.
8. **Independent oversight** — operator-layer deployments require institutional ethics-board review, published consent frameworks, and periodic third-party audits.

---

## U.S. national-interest context

National-interest context: see U.S. smart-manufacturing policy. The architecture is consistent with the U.S. **NIST AI Risk Management Framework 1.0** (Appendix C on Human-AI Interaction), with **CISA Critical Manufacturing Sector** cybersecurity priorities, and with the **EU AI Act Article 14** human-oversight requirements for cross-border interoperability.

---

## Author

**Jorge Enrique Flores Montano** is the founder of JM Automated Solutions, LLC and the inventor of MILO. He holds an M.S. in Industrial Engineering (December 2018, with a minor in Applied Statistics and a certification in Public Utilities Regulation Economics) and a B.S. in Mechatronics Engineering (May 2016, with a minor in Industrial Automation). He is a CONACYT-SENER federal scholar and a member of Alpha Pi Mu, the U.S. industrial-engineering honor society. He has hands-on experience deploying industrial vision and automation systems in food, beverage, pharmaceutical and medical-device manufacturing. His work in adaptive AI architecture focuses on cryptographic entropy sourcing, industrial control authentication, supervisory primacy for human-in-the-loop AI, and the structural principles of viable adaptive AI orchestration.

---

## License and citation

The architectural manuscripts in this repository are released under the **Creative Commons Attribution 4.0 International License** ([CC BY 4.0](LICENSE)) for academic and public use, with attribution to Jorge Enrique Flores Montano and reference to USPTO Serial No. 99706004.

**All source-code rights for the underlying MILO implementation are reserved.** Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application Serial No. 99706004.

### How to cite

```bibtex
@misc{flores_montano_milo_2026,
  author       = {Flores Montano, Jorge Enrique},
  title        = {{MILO} --- {M}odular {I}ntelligent {L}earning {O}rchestrator:
                  A Public Architectural Reference},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20117025},
  url          = {https://doi.org/10.5281/zenodo.20117025},
  note         = {v1.0.0 (version DOI); concept DOI 10.5281/zenodo.20117024. Self-published preprint series; not peer-reviewed. CC BY 4.0.}
}
```

Or use the structured `CITATION.cff` for automatic citation export — GitHub renders a "Cite this repository" widget at the top-right of the repo page.

---

## A note on the mark form

The mark filed at USPTO is `~MILO` with a leading tilde. The tilde is part of the registered mark form, included to distinguish the application from senior MILO marks held by unrelated owners in different International Classes (e.g., Nestlé's MILO in Class 30 for chocolate beverages, dating to the 1930s). The author's application is in **International Class 009** (downloadable AI software). The acronym "MILO" remains the spoken/written name of the system and is used in body text throughout the manuscripts; `~MILO™` is the brand-mark form used in trademark notices and on the title page of each paper.

---

## Status

- ✅ ~MILO™ trademark filed (USPTO Serial No. 99706004 — March 16, 2026)
- ✅ Five architectural manuscripts complete (self-published preprints; not peer-reviewed)
- ✅ Two U.S. provisional patent applications filed (No. 63/993,825; No. 64/016,665); not granted
- ⏳ arXiv preprint deposition in preparation
- ⏳ No peer review to date

---

© 2026 Jorge Enrique Flores Montano · JM Automated Solutions, LLC  
Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application Serial No. 99706004.
