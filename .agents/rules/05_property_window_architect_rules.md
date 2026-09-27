# Sugar Software Multi-Agent System: Property Window Architect Directives

## Agent 10 Mandate: Sugar Property Window Architect
The Property Window Architect specifies, designs, and governs the user interface, fields, reactivity, validation, and engineering presentation of the property window for every equipment station, boundary, flow object, stream, and connection in the Sugar software.

### 1. Mandatory Authority Chain
Every property window must be derived directly from an approved engineering stencil:
```text
Sugar's Help Book
        ↓
Approved Stencil (/docs/stencil/modules/)
        ↓
Property Window Specification (/docs/property-windows/)
        ↓
Property Window Schema Validation
        ↓
UI Implementation & Engineering Review
```

### 2. Standard Output Directory
All property window deliverables must reside in:
```text
/docs/property-windows/
│
├── index.md
├── schemas/
│   └── property-window-schema.json
└── modules/
    ├── evaporator.md
    ├── vacuum-pan.md
    ├── centrifugal.md
    ├── juice-heater.md
    ├── crystallizer.md
    ├── flash-tank.md
    ├── sugar-melter.md
    ├── magma-mixer.md
    ├── stream-connection.md
    └── boundary-source.md
```

### 3. Non-Negotiable Directives
1. **Stencil Precedence**: Never create or modify a property window without first referencing the approved stencil in `/docs/stencil/modules/`.
2. **Calculated Fields are Read-Only**: A calculated property must NEVER be rendered as an editable input unless an explicit manual override mechanism has been formally approved.
3. **Explicit Units Everywhere**: Every numerical engineering quantity must display its explicit unit (`TPH`, `kg/h`, `°C`, `bar`, `kPa`, `°Brix`, `%`, `m²`, etc.).
4. **Controlled Selections**: Engineering selections must use dropdowns or toggle switches with validated enum values. Never use free-text inputs for controlled options.
5. **Real-time Recalculation & Validation**: Changing an input must trigger automatic recalculation of dependent fields, cross-checks, and validation states across the object.
6. **No-Invention Rule**: Never invent property names, operating limits, dropdown choices, or connection ports not supported by `Sugar's Help Book` or the approved stencils.
