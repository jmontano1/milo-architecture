# MILO — Architecture pointer

This file previously contained a general software-engineering overview. It has been
narrowed to a pointer so that this repository matches the documented plant-floor design.

**The plant-floor design of MILO is set out in the MILO Methods Statement**
(JM Automated Solutions, LLC). This repository does not restate it in full.

## Scope (restated from the MILO Methods Statement)

- MILO is a **human-in-the-loop disposition layer above the plant PLC** for automated
  inspection (accept/reject/hold) on regulated food, pharmaceutical and medical-device lines.
- **Perception scores come from the vision vendor's models.** The vendor's inspection
  models stay with the vendor.
- **MILO proposes; a named person or a rule approved in advance at commissioning disposes.**
  If no person decides, the unit stays held; nothing is released by timeout.
- **MILO's only command path is one conduit to the plant PLC**, which writes
  inspection-tier flags only. MILO does not edit ladder or structured-text logic.
- **MILO has no connection to the safety PLC.** E-stop, light curtains, interlocks and
  safety-rated robot functions stay outside MILO.
- **If MILO or a record write fails, MILO issues no command**; the plant PLC's own
  fail-safe default applies.
- Standards (IEC 61508 / IEC 62061 / ISO 10218 / ISA/IEC 62443, 21 CFR Part 11, GAMP) are
  **design intent**; compliance is assessed at each plant's commissioning and validation.
  No test results are claimed here.

## Software discipline shown in this repository

The software decomposition follows the public reference: a **pre-execution gate** with three
outputs (allow, hold, recommend), an **audit-first command bus** that persists each command
before delivery (persist-before-deliver), **single-target dispatch**, and an **append-only
audit log**. The toy demos in [`examples/`](examples/) illustrate only these properties;
they are not connected to any PLC.

See also [PRINCIPLES.md](PRINCIPLES.md) and the five
[self-published preprints](articles/README.md) (Zenodo; not peer-reviewed).

---

© 2026 Jorge Enrique Flores Montano · JM Automated Solutions, LLC
~MILO™ is a trademark of Jorge Enrique Flores Montano · Two U.S. provisional patent applications filed (No. 63/993,825, Mar 1, 2026; No. 64/016,665, Mar 25, 2026); not granted. ~MILO trademark application Serial No. 99706004.
