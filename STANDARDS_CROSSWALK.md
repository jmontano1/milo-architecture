# Standards crosswalk (public tags → intent)

Topic tags on this repository align the architecture to **recognized frameworks**.
Alignment means *design intent* and *vocabulary compatibility* — not a certification,
assessment, or compliance claim. Compliance is assessed at each plant's commissioning and
validation. Functional safety (IEC 61508 / IEC 62061 / ISO 10218) stays outside MILO: E-stop,
light curtains, interlocks and the safety PLC/SIS are not connected to MILO.

| Framework | Public intent in this reference | Where discussed |
|---|---|---|
| **NIST AI RMF 1.0** (AI 100-1), incl. human–AI interaction themes | Human oversight, transparency of interventions, risk management language | Article 3 · PRINCIPLES |
| **EU AI Act Article 14** | Human oversight capacities; override / stop; resist automation bias | Article 3 |
| **ISA/IEC 62443** | Industrial cybersecurity posture; composition with OT security levels | Article 2 |
| **NIST SP 800-82r3** | OT / ICS security guidance context for industrial control | Article 2 |
| **NIST SP 800-90B** | Entropy / randomness source evaluation context | Article 1 |
| **Viable System Model / resilience engineering / antifragility** (Beer, Hollnagel, Taleb lineages) | Viability under distribution shift, not prediction-only optimization | Article 5 |

## What we do **not** publish here

- Site-specific control logic, ladder/structured text, or MES/ERP credentials  
- Plant audit findings or NDA-covered process parameters  
- Live facility network diagrams  

Those belong in private engagement packages, not this public architectural reference.

*Last updated: 2026-07-15.*
