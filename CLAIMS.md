# Claim hygiene — what this repository asserts (and does not)

This file is for technical reviewers who need a
**stable, conservative** reading of public claims associated with **this GitHub URL**
and the permanent Zenodo DOIs listed in [VERIFY.md](VERIFY.md).

## Asserted (publicly verifiable)

| Claim | Verification |
|---|---|
| Five architectural papers + concept DOI on Zenodo | [VERIFY.md](VERIFY.md) |
| This repository is the open architectural reference under CC BY 4.0 (text/docs) | [LICENSE](LICENSE), this repo URL |
| Runnable reference demos of audit-first and supervisory override | `examples/` + CI |
| USPTO trademark ~MILO™ Serial 99706004 (intent-to-use) | TSDR link in VERIFY.md |
| Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted | Author statement |
| Manuscript TII-26-4335 **transmitted** to IEEE TII | Submission record — **no acceptance / peer-review assignment / publication claimed** |

## Explicitly **not** claimed

- IEEE acceptance, peer-review assignment, or publication  
- Peer review of any paper: the papers are self-published preprints (Zenodo); not peer-reviewed  
- That the toy Python demos are production OT / SCADA software  
- Any plant data, PLC programs, or NDA-covered process details  
- Certification or compliance with any standard: standards are design intent; compliance is assessed at each plant's commissioning and validation  
- Performance benchmarks not backed by a public method and result in this repo  

## Status

MILO is pre-commercial; no customer deployments exist. Source code is not public. This repository is an architectural reference + pedagogical code so third parties
can understand and reproduce the *discipline* (persist-before-deliver, explicit dispatch,
reflex-before-fanout, pre-execution gate, human override audit).

*Last updated: 2026-07-15.*
