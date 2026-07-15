# Mechanism → paper → public code map

| Mechanism | Architectural claim | Paper | Public demo |
|---|---|---|---|
| **Persist-before-deliver** | Intent is durable before side effects | Art. 4, 5 | `examples/persist_before_deliver.py` |
| **Explicit-target dispatch** | No implicit routing of consequential actions | Art. 4 | same |
| **Reflex before fanout** | Critical signals short-circuit before general subscribers | Art. 4, 5 | same |
| **Pre-execution gate** (allow / hold / recommend) | Consequence-aware authorization before execution | Art. 2, 3 | same + `supervisory_primacy_override.py` |
| **Human override with audit** | Supervisory Primacy — human disposes; trail required | Art. 3 | `examples/supervisory_primacy_override.py` |
| **Independence as architectural property** (entropy class) | Multi-source independence as designed-for property | Art. 1 | *principle-level only in public repo* |
| **Viability vs prediction** | Remain useful under distribution shift | Art. 5 | narrative + mechanisms above |

## Self-check

```bash
python3 examples/test_reference.py
```

CI runs the same entrypoint on every push to `main`.

*Last updated: 2026-07-15.*
