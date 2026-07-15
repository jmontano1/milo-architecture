# Claim hygiene — what this repository asserts (and does not)

This file is for reviewers (including immigration and technical officers) who need a
**stable, conservative** reading of public claims associated with **this GitHub URL**
and the permanent Zenodo DOIs listed in [VERIFY.md](VERIFY.md).

## Asserted (publicly verifiable)

| Claim | Verification |
|---|---|
| Five architectural papers + concept DOI on Zenodo | [VERIFY.md](VERIFY.md) |
| This repository is the open architectural reference under CC BY 4.0 (text/docs) | [LICENSE](LICENSE), this repo URL |
| Runnable reference demos of audit-first and supervisory override | `examples/` + CI |
| USPTO trademark ~MILO™ Serial 99706004 (intent-to-use) | TSDR link in VERIFY.md |
| Patent pending (provisional; details confidential during pendency) | Author statement; private verification on request |
| Materials **transmitted** to DOE Genesis Mission channels under **MILO-ES-2026-002** and **MILO-ES-2026-003-DOE** | Author/counsel records — **transmission only** |
| Manuscript TII-26-4335 **transmitted** to IEEE TII | Submission record — **no acceptance / peer-review assignment / publication claimed** |
| Subject-matter alignment with Genesis Mission priority areas | **Asserted by the author**, not as DOE endorsement |

## Explicitly **not** claimed

- DOE selection, endorsement, partnership, contract, funding, or award  
- IEEE acceptance, peer-review assignment, or publication  
- That Zenodo constitutes peer review  
- That the toy Python demos are production OT / SCADA software  
- Any customer name, plant data, PLC programs, or NDA-covered process details  
- Performance benchmarks not backed by a public method and result in this repo  

## Production vs public reference

The **private** MILO product mono-repo and any customer deployments are **out of scope**
here. This repository is an architectural reference + pedagogical code so third parties
can understand and reproduce the *discipline* (persist-before-deliver, explicit dispatch,
reflex-before-fanout, pre-execution gate, human override audit).

*Last updated: 2026-07-15.*
