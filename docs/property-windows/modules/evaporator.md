# Evaporator Station Property Window Specification
## Component Code: `PW-EVAP-01`
### SUGARS Station Type Code: `9` | Object Tag Prefix: `EVAP`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-EVAP-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/evaporator.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Evaporator/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

The Evaporator Property Window provides a multi-tab engineering interface strictly reflecting the control options from Sugar's Help Book:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [EVAP] EVAPORATOR EFFECT PROPERTY WORKSPACE                     [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [1st Effect_________] Station No [ 1 ] Equip Tag [EVAP-01]│
│ Effect Number [ 1 ] (Motive steam required for Effect 1)               │
├────────────────────────────────────────────────────────────────────────┤
│ [Properties]  [Heat Transfer & Area]  [Vapour & Losses]  [Results & CC]│
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ OPERATING SPECIFICATION MODE (MUTUALLY EXCLUSIVE / MAGENTA) ──────┐ │
│ │ (*) Option A: Heat Transfer Coef (U) & Heating Surface Area (A)    │ │
│ │     Heat Transfer Coef: [ 1850.0 ] W/m²·K   [Calc U / Surface Area]│ │
│ │     Heating Surface:    [ 2200.0 ] m²                              │ │
│ │ ( ) Option B: Vapour Out Pressure & Saturation Temperature         │ │
│ │     Vapour Pressure:    [ ______ ] kPa abs                         │ │
│ │     Saturation Temp:    [ ______ ] °C                              │ │
│ │ ( ) Option C: Juice Flow Out Temperature                           │ │
│ │     Flow Out Temp:      [ ______ ] °C                              │ │
│ │ ( ) Option D: Pressure Feedback from Downstream Receiver/Condenser │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ CONCENTRATION & LOSS CONTROLS ────────────────────────────────────┐ │
│ │ Total Solids Target:    [ 65.00 ] % DS (Auto-adjusts 1st eff steam) │ │
│ │ Heat Loss to Ambient:   [  1.50 ] % of gross duty                  │ │
│ │ Condensate Drop:        [  2.00 ] K (Subcooling below T_sat)       │ │
│ │ Entrainment Sugar Loss: [    50 ] ppm (carried over in vapour)     │ │
│ │ BPE Adjustment Factor:  [  1.00 ] multiplier                       │ │
│ │ Color Rise:             [  5.00 ] % increase across body           │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ LIVE THERMODYNAMIC BALANCES (READ-ONLY) ──────────────────────────┐ │
│ │ Water Evaporated:    [ 32.450 ] TPH   Calandria Steam: [ 34.120 ] TPH│
│ │ Concentrated Syrup:  [ 28.150 ] TPH   Steam Economy:   [  0.951 ]    │
│ │ Boiling Juice Temp:  [ 104.25 ] °C    BPE Elevation:   [   2.35 ] °C │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ DS Balance: PASS] [✓ Enthalpy Closure: PASS] │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Up to 20 chars (e.g. 1st Effect) |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID (1–9999) |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars) |
| `effectNumber` | Effect Number | Integer | — | YES | Sequential position (1..N). Motive steam strictly required for Effect 1. |
| `specMode` | Operating Mode | Enum | — | YES | `HTC_AREA`, `VAPOUR_P_T`, `FLOW_OUT_TEMP`, `PRESSURE_FEEDBACK` (Mutually exclusive with Magenta border) |
| `heatTransferCoef` | Heat Transfer Coef | Float | $W/m^2\cdot K$ | Dynamic | Active only when `specMode == 'HTC_AREA'` |
| `heatingSurface` | Heating Surface Area | Float | $m^2$ | Dynamic | Active only when `specMode == 'HTC_AREA'` |
| `vaporPressure` | Vapour Out Pressure | Float | $kPa\text{ abs}$ | Dynamic | Active only when `specMode == 'VAPOUR_P_T'`. Auto-calculates sat temp. |
| `satTemperature` | Saturation Temp | Float | $°C$ | Dynamic | Active only when `specMode == 'VAPOUR_P_T'`. Auto-calculates pressure. |
| `flowOutTemp` | Flow Out Temp | Float | $°C$ | Dynamic | Active only when `specMode == 'FLOW_OUT_TEMP'` |
| `totalSolidsPct` | Total Solids Target | Float | `%` | YES | Target dry substance of outlet syrup |
| `heatLossPct` | Heat Loss | Float | `%` | YES | Radiation and conduction loss from calandria steam |
| `condensateDropK`| Condensate Drop | Float | $K$ | YES | Degrees of subcooling below steam saturation temperature |
| `entrainmentPpm` | Entrainment Loss | Float | $ppm$ | YES | Carryover of syrup droplets in vapor |
| `bpeFactor` | BPE Factor | Float | — | YES | Multiplier on calculated BPE (default 1.0) |
| `colorRise` | Color Rise | Float | `%` / `CU` | YES | Increase in syrup color |

---

## 3. Interactive Sizing Tool Popup (`Calc U / Surface Area`)

When the user clicks the sizing button next to Heat Transfer Coefficient or Heating Surface, a modal popup opens with two reciprocal calculation options:
1. **Solve for Heating Surface Area ($A$)**: Given design thermal duty ($Q$), Heat Transfer Coefficient ($U$), and $\Delta T_{eff} = T_{steam,sat} - T_{juice,boil}$:
   $$A = \frac{Q}{U \cdot \Delta T_{eff}}$$
2. **Solve for Heat Transfer Coefficient ($U$)**: Given design thermal duty ($Q$), Heating Surface Area ($A$), and $\Delta T_{eff}$:
   $$U = \frac{Q}{A \cdot \Delta T_{eff}}$$
Clicking "Apply" writes the calculated value directly back to the active property field.
