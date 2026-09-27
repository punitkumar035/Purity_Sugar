# Surface Heat Exchanger Property Window Specification
## Component Code: `PW-HEX-01`
### SUGARS Station Type Code: `12` | Object Tag Prefix: `HEX`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-HEX-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/juice-heating.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Heat_Exchanger/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [HEX] SURFACE HEAT EXCHANGER PROPERTY WORKSPACE                [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [2nd Carb. Heaters____] Station No [ 12 ] Tag [HEX-02]    │
├────────────────────────────────────────────────────────────────────────┤
│ [Operating Specs]  [Heat Transfer & Sizing]  [Connections]  [Results]  │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ PORT 0 (PROCESS STREAM) TEMPERATURE CONTROL (MAGENTA BORDERS) ────┐ │
│ │ (*) Out:       [  90.0 ] °C (Target process discharge temperature)  │ │
│ │ ( ) Rise:      [   7.5 ] K  (Process fluid temperature rise)        │ │
│ │ ( ) Approach:  [   5.5 ] K  (T1_out - T0_out temperature difference)│ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ PORT 1 (UTILITY STREAM) CONTROLS ─────────────────────────────────┐ │
│ │ [x] Input Flow Required (Sugars calculates required steam/vapour)   │ │
│ │     Temperature Out: [ _____ ] °C (For liquid-liquid exchange)      │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ HEAT TRANSFER & EQUIPMENT SIZING (MAGENTA BORDERS) ───────────────┐ │
│ │ ( ) Effectiveness: [  60.0 ] % (30% shell & tube / 60% plate)      │ │
│ │ (*) HTC & Surface:                                                 │ │
│ │     Heat Transfer Coef: [ 1850.0 ] W/m²·K                          │ │
│ │     Heating Surface:    [  350.0 ] m²                              │ │
│ │ Condensate Drop:        [    4.0 ] K (Subcooling below T_sat)       │ │
│ │ Heat Loss to Ambient:   [   0.50 ] % of transferred duty           │ │
│ │ Flow Direction:         (o) Counter-current   ( ) Co-current       │ │
│ │ Type:                   (o) Condensing Steam  ( ) Non-condensing   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ LIVE THERMAL BALANCES & RATINGS (READ-ONLY) ──────────────────────┐ │
│ │ Process Stream Flow: [ 120.000 ] TPH  Temp In: [ 65.0 ] → Out [ 90.0]│
│ │ Heating Steam Flow:  [   5.450 ] TPH  Condensate Flow: [ 5.450 ] TPH │
│ │ Thermal Duty:        [   3.480 ] MW   LMTD:   [ 18.45 ] K           │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Process Mass: PASS] [✓ Utility Mass: PASS] [✓ Enthalpy Closure: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Descriptive title (e.g. Raw Juice Heater) |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag |
| `port0Mode` | Port 0 Control Mode | Enum | — | YES | `OUT_TEMP`, `TEMP_RISE`, `APPROACH` (Mutually exclusive Magenta) |
| `port0TempOut` | Port 0 Temp Out | Float | `°C` | Dynamic | Active when `port0Mode == 'OUT_TEMP'` |
| `port0TempRise` | Port 0 Temp Rise | Float | `K` | Dynamic | Active when `port0Mode == 'TEMP_RISE'` |
| `port0Approach` | Port 0 Approach | Float | `K` | Dynamic | Active when `port0Mode == 'APPROACH'`. Difference $T_{1,out} - T_{0,out}$. |
| `port1InputRequired`| Input Flow Required | Boolean | — | YES | When checked, Sugars calculates utility mass rate |
| `port1TempOut` | Port 1 Temp Out | Float | `°C` | Dynamic | Specified outlet temperature for liquid heating media |
| `ratingMode` | Sizing / Rating Mode | Enum | — | YES | `EFFECTIVENESS` vs `HTC_AND_AREA` (Mutually exclusive) |
| `effectivenessPct`| Effectiveness (%) | Float | `%` | Dynamic | Active when `ratingMode == 'EFFECTIVENESS'` |
| `htc` | Heat Transfer Coef | Float | $W/m^2\cdot K$ | Dynamic | Active when `ratingMode == 'HTC_AND_AREA'` |
| `heatingSurface` | Heating Surface Area | Float | $m^2$ | Dynamic | Active when `ratingMode == 'HTC_AND_AREA'` |
| `condensateDropK`| Condensate Drop | Float | `K` | YES | Subcooling of condensate below saturation |
| `heatLossPct` | Heat Loss | Float | `%` | YES | Ambient radiation/convection loss |
| `flowDirection` | Flow Direction | Enum | — | YES | `COUNTER_CURRENT` vs `CO_CURRENT` |
| `exchangerType` | Exchanger Type | Enum | — | YES | `CONDENSING` vs `NON_CONDENSING` |
