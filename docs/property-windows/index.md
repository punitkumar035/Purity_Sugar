# Sugar Software Property Window Architecture & Registry
## Comprehensive Property Window Registry

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Authoritative Basis**: Approved Sugar Stencils (`/docs/stencil/`) & `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Schema Definition**: [`schemas/property-window-schema.json`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/schemas/property-window-schema.json)  
> **Status**: `ALL 22 MODULES ENGINEERING-VALIDATED`

---

## 1. Architectural Mission & Principles

A property window in the Sugar software is an **engineering interface**, not a generic settings form. It provides real-time visibility, configuration, and thermodynamic traceability for every equipment unit, stream, boundary, and connection.

### Non-Negotiable Directives
1. **Stencil Precedence**: A property window implements an approved stencil from `/docs/stencil/modules/`. It never redefines or invents fields.
2. **Read-Only Calculations**: Fields classified as `CALCULATED` or `INTERMEDIATE` are strictly `editable = false` by default, visually set apart with engineering styling and unit badges.
3. **Explicit Units Everywhere**: Every numerical property displays its official engineering unit (`TPH`, `kg/h`, `°C`, `bar`, `kPa`, `°Brix`, `%`, `m²`, `kg/m²·h`).
4. **Controlled Selections**: Engineering choices use dropdowns (`DROPDOWN`) or switches (`BOOLEAN` [ON/OFF]); never raw text inputs.
5. **Real-Time Reactive Recalculation**: Editing an input triggers recalculation of all dependent fields, revalidation, and cross-checks immediately.
6. **Validation Badges**: Status is communicated via explicit badges: `[✓ PASS]`, `[⚠ WARNING]`, `[✕ ERROR]`, `[ⓘ INFO]`. Color alone is never the sole indicator.

---

## 2. Standard Property Window Section Hierarchy

Every property window conforms to the following standardized 10-section structure:

```text
┌────────────────────────────────────────────────────────┐
│ [STATION TYPE] [EQUIPMENT TAG]                     [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number, Tag, Name, Type Code                │
├────────────────────────────────────────────────────────┤
│ 2. REQUIRED PROCESS INPUTS                             │
│    Throughputs, Target Brix, Operating Pressures (Unit)│
├────────────────────────────────────────────────────────┤
│ 3. OPTIONAL INPUTS & OPERATION MODES                   │
│    Vapour Bleed, Condensate Flash, Mode Switches       │
├────────────────────────────────────────────────────────┤
│ 4. OPERATING & THERMODYNAMIC PARAMETERS                │
│    Temperatures, Vacuum Levels, Heat Transfer Coefs    │
├────────────────────────────────────────────────────────┤
│ 5. CALCULATED RESULTS (READ-ONLY)                      │
│    Evaporated Water, Product Flow, Steam Demand (Unit) │
├────────────────────────────────────────────────────────┤
│ 6. INTERMEDIATE VALUES & TRACEABILITY                  │
│    Dry Substance Flow, Enthalpy Drops, BPE, Latent Ht  │
├────────────────────────────────────────────────────────┤
│ 7. REFERENCE VALUES & COEFFICIENTS                     │
│    Solubility Coefs, Boiling Point Elevation Coefs     │
├────────────────────────────────────────────────────────┤
│ 8. PROCESS CONNECTIONS & TOPOLOGY                      │
│    Feed Inlets, Vapor Outlets, Condensate Lines        │
├────────────────────────────────────────────────────────┤
│ 9. VALIDATION & OPERATING LIMITS                       │
│    ✓ Inputs within physical ranges                     │
├────────────────────────────────────────────────────────┤
│ 10. INDEPENDENT CROSS-CHECKS                           │
│    ✓ Mass Balance Closure: < 0.05% PASS                │
│    ✓ Dry Substance Balance Closure: < 0.01% PASS       │
└────────────────────────────────────────────────────────┘
```

---

## 3. Comprehensive Property Window Registry (22 Specifications)

| Station / Object | Stencil ID | Property Window Spec | Status | Help Book Ref |
|---|---|---|---|---|
| **Vacuum Pan** | `STENCIL-PAN-01` | [`modules/vacuum-pan.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/vacuum-pan.md) | `ENGINEERING-VALIDATED` | `Pan/` |
| **Evaporator Station** | `STENCIL-EVAP-01` | [`modules/evaporator.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/evaporator.md) | `ENGINEERING-VALIDATED` | `Evaporator/` |
| **Juice & Process Heater** | `STENCIL-HEAT-01` | [`modules/juice-heater.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/juice-heater.md) | `ENGINEERING-VALIDATED` | `Heat_Exchanger/` |
| **Direct Injection Heater** | `STENCIL-INJ-01` | [`modules/injection-heater.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/injection-heater.md) | `ENGINEERING-VALIDATED` | `Injection_Heater/` |
| **Sugar Melter** | `STENCIL-MELT-01` | [`modules/sugar-melter.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/sugar-melter.md) | `ENGINEERING-VALIDATED` | `Melter/` |
| **Blender / Magma Mixer** | `STENCIL-BLND-01`| [`modules/magma-mixer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/magma-mixer.md) | `ENGINEERING-VALIDATED` | `Blender/` |
| **Centrifugal Station** | `STENCIL-CENT-01` | [`modules/centrifugal.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/centrifugal.md) | `ENGINEERING-VALIDATED` | `Centrifugal/` |
| **Cooling Crystallizer** | `STENCIL-CRYS-01` | [`modules/crystallizer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/crystallizer.md) | `ENGINEERING-VALIDATED` | `Crystallizer/` |
| **Flash Recovery Tank** | `STENCIL-FLS-01` | [`modules/flash-tank.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/flash-tank.md) | `ENGINEERING-VALIDATED` | `Flash_Tank/` |
| **Sugar Rotary Dryer** | `STENCIL-DRY-01` | [`modules/sugar-dryer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/sugar-dryer.md) | `ENGINEERING-VALIDATED` | `Dryer/` |
| **Sugar Cooler & Heat Loss**| `STENCIL-CLR-01` | [`modules/sugar-cooler.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/sugar-cooler.md) | `ENGINEERING-VALIDATED` | `Cooler/` |
| **Mechanical Vapor Comp (MVR)**| `STENCIL-CMP-01`| [`modules/vapor-compressor.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/vapor-compressor.md) | `ENGINEERING-VALIDATED` | `Compressor/` |
| **Steam Thermocompressor**| `STENCIL-TCM-01` | [`modules/thermocompressor.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/thermocompressor.md) | `ENGINEERING-VALIDATED` | `Thermocompressor/` |
| **Pressure Reducer (PRV)**| `STENCIL-PRV-01` | [`modules/pressure-reducer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/pressure-reducer.md) | `ENGINEERING-VALIDATED` | `Pressure_Reducer/` |
| **Process Pump** | `STENCIL-PMP-01` | [`modules/process-pump.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/process-pump.md) | `ENGINEERING-VALIDATED` | `Pump/` |
| **Process & Storage Tank** | `STENCIL-TNK-01` | [`modules/process-tank.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/process-tank.md) | `ENGINEERING-VALIDATED` | `Tank/` |
| **Steam Turbine & Turbo Alt**| `STENCIL-TRB-01`| [`modules/steam-turbine.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/steam-turbine.md) | `ENGINEERING-VALIDATED` | `Turbine/`, `Turbo_Alternator/` |
| **Contact & Surface Condenser**| `STENCIL-CND-01`| [`modules/condensers.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/condensers.md) | `ENGINEERING-VALIDATED` | `Contact_Condenser/`, `Surface_Condenser/` |
| **Separator & Filter** | `STENCIL-SEP-01` | [`modules/separator-filter.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/separator-filter.md) | `ENGINEERING-VALIDATED` | `Separator_Filter/` |
| **Cross-Page Connector** | `STENCIL-CONN-01`| [`modules/cross-page-connector.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/cross-page-connector.md) | `ENGINEERING-VALIDATED` | Phase 4 Visio |
| **Boundary Source / Sink**| `STENCIL-BND-01` | [`modules/boundary-source.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/boundary-source.md) | `ENGINEERING-VALIDATED` | Program Overview |
| **Stream / Pipeline Conn**| `STENCIL-STRM-01`| [`modules/stream-connection.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/property-windows/modules/stream-connection.md) | `ENGINEERING-VALIDATED` | 15-Component Model |
