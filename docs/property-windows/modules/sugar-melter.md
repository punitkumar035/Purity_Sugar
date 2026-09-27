# Sugar Melter Station Property Window Specification
## Component Code: `PW-MELT-01`
### SUGARS Station Type Code: `16` | Object Tag Prefix: `MELT`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-MELT-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-melter.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Melter/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [MELT] SUGAR MELTER PROPERTY WORKSPACE                          [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [High Melter_________] Station No [ 16 ] Equip Tag [MELT-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Melter Specs]  [Solvent & Dilution]  [Heating & Thermal]  [Balances]  │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ SYRUP & DISSOLUTION CONTROLS ─────────────────────────────────────┐ │
│ │ Hold TDM at (%):        [ 67.00 ] % (Controls Port 9 Diluent flow) │ │
│ │ Target Out Temperature: [ 85.00 ] °C (Controls Port 10 Steam flow) │ │
│ │ Heating Type:           (o) Injection (steam dilutes liquor)       │ │
│ │                         ( ) Coil (clean condensate discharged)     │ │
│ │ Color Rise:             [  5.00 ] % increase                       │ │
│ │ Heat Loss to Ambient:   [  1.00 ] % of transferred duty            │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ REQUIRED FLOW SELECTION (ACTIVE WHEN MELTER OUTLET IS REQUIRED) ──┐ │
│ │ Target Outlet Flow Demand: 45.000 TPH                                │ │
│ │ Select which inlet stream adjusts to satisfy downstream demand:     │ │
│ │   (o) Port 0: Sugar Feed (Raw Sugar Affination C-Magma)             │ │
│ │   ( ) Port 9: Diluent Water / Sweetwater                            │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISSOLUTION THERMODYNAMICS & STREAM RESULTS (READ-ONLY) ──────────┐ │
│ │ Melt Liquor Flow:       [ 45.000 ] TPH   Melt Brix:     [ 67.00 ] °B │
│ │ Dissolved Sucrose Rate: [ 30.150 ] TPH   Residual Cryst:[  0.00 ] % 🔒
│ │ Solvent Water Demand:   [ 12.350 ] TPH   Motive Steam:  [  1.85 ] TPH│
│ │ Endothermic Dissolution:[ -1,655 ] kW    Gross Duty:    [  3,240 ] kW│
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ DS Balance: PASS] [✓ Crystal Extinction: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag |
| `holdTdmPct` | Hold TDM at (%) | Float | `%` | Dynamic | Controls Port 9 diluent flow rate. Dimmed if Port 9 is not connected. Enter 0.00% to disable control. |
| `temperatureOut`| Temperature Out | Float | `°C` | Dynamic | Controls Port 10 heating flow rate. Dimmed if Port 10 is not connected. |
| `heatingType` | Heating Type | Enum | — | YES | `INJECTION` (steam mixes into liquor) vs `COIL` (condensate leaves via Port 12). |
| `colorRise` | Color Rise | Float | `%` / `CU` | YES | Optical color formation across vessel. |
| `heatLossPct` | Heat Loss | Float | `%` | YES | Thermal loss to surroundings (% of transferred heat). |
| `requiredFlowInlet`| Required Flow Inlet | Port ID | — | Dynamic | Active only when melter output flow is a Required Flow. Lets user select which inlet flow balances the station. |

---

## 3. Dissolution Physics Verification

Under `RULES_v5.md` (§A9) and `Sugar's Help Book`:
- **Complete Crystal Extinction**: All sucrose crystals entering via Ports 0–8 are converted to dissolved sucrose.
- **Heat of Dissolution**: Absorbs $54.9\text{ kJ/kg}$ of crystal sucrose dissolved.
- **Atmospheric Pressure**: The vessel discharges strictly at $101.325\text{ kPa}$ absolute.
