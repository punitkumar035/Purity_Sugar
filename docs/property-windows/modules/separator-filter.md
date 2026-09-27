# Separator / Filter Station Property Window Specification
## Component Code: `PW-SEP-01`
### SUGARS Station Type Code: `20` | Object Tag Prefix: `SEP`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-SEP-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/separator-filter.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Separator_Filter/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [SEP] SEPARATOR / FILTER STATION PROPERTY WORKSPACE             [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Runoff Separator____] Station No [ 20 ] Equip Tag [SEP-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Separation Specs]  [Diluent & Wash]  [Component Splits]  [Balances]   │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DILUENT & WASH CONTROL (MAGENTA MUTUALLY EXCLUSIVE BORDER) ───────┐ │
│ │ Mode:                                                              │ │
│ │   (o) No Ratio (Inlet wash flow on Port 1 is fixed / independent)  │ │
│ │   ( ) Ratio to Component (Wash flow calculated dynamically)        │ │
│ │                                                                    │ │
│ │ [If Ratio to Component Selected]:                                  │ │
│ │ Ratio Multiplier:  [  0.150 ] kg wash / kg basis stream            │ │
│ │ Ratio Basis:       [ Total Flow ▼ ] (Total, Sucrose, DS, Water)     │ │
│ │                                                                    │ │
│ │ Diluent Distribution:                                              │ │
│ │ % Diluent to Out Flow #1: [ 30.00 ] % (Remainder exits in Out #2)   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ SELECTIVE COMPONENT SEPARATION MATRIX ────────────────────────────┐ │
│ │ Component Name             │ % Entering Out Flow #1 │ % in Out #2   │
│ │ ───────────────────────────┼────────────────────────┼────────────── │
│ │ 1. [ Sucrose Crystals   ▼] │ [ 100.00 ] %           │ [   0.00 ] % 🔒│
│ │ 2. [ Dissolved Sucrose  ▼] │ [  50.00 ] %           │ [  50.00 ] % 🔒│
│ │ 3. [ Water              ▼] │ [  40.00 ] %           │ [  60.00 ] % 🔒│
│ │ 4. [ Non-Sucrose 1      ▼] │ [  30.00 ] %           │ [  70.00 ] % 🔒│
│ │ 5. [ All Other Comps    ─] │ [   0.00 ] %           │ [ 100.00 ] % 🔒│
│ │                                                                    │ │
│ │ Color Agent Split:                                                 │ │
│ │ % of Color to Out Flow #1: [ 100.00 ] % (<100% shifts to Out #2)   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ SEPARATION STREAM RESULTS (READ-ONLY) ────────────────────────────┐ │
│ │ Feed In (Port 0):  [ 50.000 ] TPH | Brix: [ 88.50 ] °B | Purity: 82.0│ │
│ │ Wash In (Port 1):  [  2.500 ] TPH | Brix: [  0.00 ] °B             │ │
│ │ Out Flow #1:       [ 22.150 ] TPH | Brix: [ 92.40 ] °B (Sugar/Cake)│ │
│ │ Out Flow #2:       [ 30.350 ] TPH | Brix: [ 84.10 ] °B (Molasses)  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ DS Balance: PASS] [✓ Enthalpy Closure: PASS] 
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag |
| `diluentMode` | Diluent Mode | Enum | — | YES | `NO_RATIO` vs `RATIO_COMPONENT`. Triggers Magenta border. |
| `diluentRatio` | Ratio Multiplier | Float | — | Dynamic | Active when `RATIO_COMPONENT`. Dimmed when `NO_RATIO`. |
| `diluentRatioBasis`| Ratio Basis | Enum | — | Dynamic | Basis component: `TOTAL`, `SUCROSE`, `DS`, `WATER`. |
| `diluentOut1Pct` | % Diluent to Out 1 | Float | `%` | YES | Fraction of incoming diluent reporting to Output #1 (0.0 to 100.0%). |
| `comp1Name` | Component 1 | Enum | — | YES | Selects component from 15-component ledger. |
| `comp1Out1Pct` | Comp 1 Out #1 % | Float | `%` | YES | % of Component 1 entering Out Flow #1. |
| `comp2Name` | Component 2 | Enum | — | YES | Selects component from 15-component ledger. |
| `comp2Out1Pct` | Comp 2 Out #1 % | Float | `%` | YES | % of Component 2 entering Out Flow #1. |
| `comp3Name` | Component 3 | Enum | — | YES | Selects component from 15-component ledger. |
| `comp3Out1Pct` | Comp 3 Out #1 % | Float | `%` | YES | % of Component 3 entering Out Flow #1. |
| `comp4Name` | Component 4 | Enum | — | YES | Selects component from 15-component ledger. |
| `comp4Out1Pct` | Comp 4 Out #1 % | Float | `%` | YES | % of Component 4 entering Out Flow #1. |
| `otherCompOut1Pct`| Other Comps Out #1 %| Float | `%` | YES | Split for unlisted components (default 0%). |
| `colorOut1Pct` | Color Split Out #1 %| Float | `%` | YES | Default 100%. Lower values send more color to Out Flow #2 (decolorization). |

---

## 3. Centrifugal & Filtration Preset Profiles

To support rapid configuration in centrifugal and filter stations, the property window provides standard presets:
1. **Centrifugal High-Grade / Wash Runoff Splitter**:
   - Wash In: Sweetwater/water on Port 1.
   - Out 1 (Wash Runoff / High Purity), Out 2 (Green Runoff / Mother Liquor).
2. **Centrifugal Sugar / Molasses Separation**:
   - Comp 1 (Crystals): 100% to Out 1 (Sugar).
   - Comp 2 (Dissolved Sucrose): 10% to Out 1, 90% to Out 2.
   - Comp 3 (Water): 2% to Out 1, 98% to Out 2.
3. **Rotary Vacuum Filter (Mud Separation)**:
   - Comp 1 (Insoluble Matter / Fiber / Mud): 98% to Out 2 (Filter Cake), 2% to Out 1 (Filtrate).
   - Wash water on Port 1 with Diluent Ratio = 0.08 on Cane or Mud DS.

---

## 4. Validation & Cross-Checks

1. **Mass Balance Closure**: Out 1 Flow + Out 2 Flow == Feed In Flow + Diluent In Flow ($\pm 0.001\%$).
2. **Dry Substance Closure**: Out 1 DS kg/h + Out 2 DS kg/h == Feed DS kg/h + Diluent DS kg/h ($\pm 0.0001\%$).
3. **Color Balance**: Total color units conserved across separation.
