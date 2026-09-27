# Sugar Software Multi-Agent System: Stencil Architect Directives

## Agent 9 Mandate: Sugar Stencil Architect
The Stencil Architect converts domain knowledge from `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`) into exhaustive, structured software specifications under `/docs/stencil/`.

### 1. Mandatory Workflow Gate
Before Agent 4 (Developer) writes or modifies any process or equipment module, Agent 9 (Sugar Stencil Architect) must produce the corresponding specification under `/docs/stencil/modules/` and have it marked as `ENGINEERING-VALIDATED`.

### 2. Standard Stencil Output Directory
All deliverables must reside in:
```text
/docs/stencil/
│
├── skill-index.md
├── module-index.md
├── field-registry.md
├── formula-registry.md
├── dependency-map.md
├── validation-registry.md
├── cross-check-registry.md
│
├── modules/
│   ├── [module-name].md
│   └── ...
│
└── schemas/
    └── stencil-schema.json
```

### 3. Absolute No-Invention Enforcement
The Stencil Agent must never invent formulas, coefficients, capacities, operating ranges, or limits.
If information is not explicitly documented in `Sugar's Help Book`:
- Mark as `UNKNOWN / REFERENCE_REQUIRED`.
- Flag for review by Agent 0 (Master) and Agent 2 (Engineering Specialist).
- Record the explicit engineering assumption in `/docs/engineering-assumptions.md`.
