# For independent reviewers

This repository URL — **https://github.com/jmontano1/milo-architecture** — appears in the
author’s public architectural papers and related materials as the open **architectural reference**
for MILO (Modular Intelligent Learning Orchestrator).

You do **not** need a private account or any secret credentials.

## What this repository is

| Item | Detail |
|---|---|
| Author | Jorge Enrique Flores Montano · JM Automated Solutions |
| ORCID | https://orcid.org/0009-0003-1859-8418 |
| Concept DOI | https://doi.org/10.5281/zenodo.20117025 |
| Trademark | ~MILO™ · USPTO Serial **99706004** (intent-to-use) |
| Patent | Patent pending |
| License (docs/manuscripts) | CC BY 4.0 · see [LICENSE](LICENSE) |

## What to open (in order)

1. **This file** — orientation  
2. **[VERIFY.md](VERIFY.md)** — independent URL checklist (DOIs, ORCID, USPTO, Federal Register)  
3. **[CLAIMS.md](CLAIMS.md)** — what is asserted vs explicitly **not** claimed  
4. **[MECHANISM_MAP.md](MECHANISM_MAP.md)** — architecture mechanisms → papers → runnable demos  
5. **[examples/](examples/)** — stdlib demos (no network, no secrets):

```bash
python3 examples/test_reference.py
python3 examples/persist_before_deliver.py
python3 examples/supervisory_primacy_override.py
```

6. **Articles** under [`articles/`](articles/) and permanent Zenodo DOIs listed in VERIFY.md  
7. **[ARCHITECTURE.md](ARCHITECTURE.md)** · **[PRINCIPLES.md](PRINCIPLES.md)** · **[STANDARDS_CROSSWALK.md](STANDARDS_CROSSWALK.md)**

## Claim hygiene (read carefully)

- **DOE Genesis Mission:** materials were **transmitted** under document identifiers  
  **MILO-ES-2026-002** and **MILO-ES-2026-003-DOE** (and related FOA materials where applicable).  
  This repository claims **transmission only** — **not** DOE endorsement, selection, partnership,  
  contract, funding, or award.  
- **IEEE TII manuscript TII-26-4335:** **transmission / submission record only** —  
  **not** acceptance, peer-review assignment, or publication.  
- **Zenodo:** open archive with permanent DOIs; **not** peer review by Zenodo.  
- **Demos:** pedagogical reference implementations of architectural *discipline*;  
  **not** production OT/SCADA software and **not** customer deployments.

## What you will **not** find here

- Customer names, plant data, NDA materials, or employer trade secrets  
- Immigration case files or confidential counsel exhibits  
- Live commercial product backends (separate company surfaces)

## Continuous integrity

GitHub Actions runs the public self-check on every push to `main`  
([workflow: reference-ci](.github/workflows/ci.yml)).

---

*Maintained for independent technical and documentary verification of the public architectural reference.*
