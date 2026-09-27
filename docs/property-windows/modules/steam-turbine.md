# Steam Turbine & Turbo Alternator Property Window Specification
## Component Code: `PW-TRB-01` / `PW-GEN-01`
### SUGARS Station Type Codes: `17` (Turbine) & `18` (Turbo Alternator) | Object Tag Prefix: `TRB` / `GEN`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-TRB-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/steam-turbine.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Turbine/`, `Turbo_Alternator/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [GEN] COGENERATION TURBO ALTERNATOR PROPERTY WORKSPACE          [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [TG Set #1 Backpressure] Station No [ 18 ] Equip Tag [GEN-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Thermal Expansion]  [Exhaust Pressure]  [Power & Eff]  [Balances]     │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ THERMAL EXPANSION MODE (MAROON MUTUALLY EXCLUSIVE) ────────────────┐ │
│ │ Select Thermal Control Option:                                       │ │
│ │  (o) Isentropic Efficiency (eta_s): [ 72.00 ] %                      │ │
│ │  ( ) Exhaust Temperature Out:       [ 135.0 ] °C                     │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ EXHAUST DISCHARGE PRESSURE (MAGENTA MUTUALLY EXCLUSIVE) ───────────┐ │
│ │ Select Backpressure Option:                                          │ │
│ │  (o) Discharge Pressure:    [ 200.0 ] kPa                            │ │
│ │  ( ) Pressure Drop across stages:[2,300.0] kPa                       │ │
│ │  ( ) Pressure Feedback:     [ EXHAUST STEAM HEADER ] [ ] Active      │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ POWER GENERATION & REQUIRED STEAM CONTROL ────────────────────────┐ │
│ │ Station Classification:     (o) Turbo Alternator   ( ) Mech Turbine  │ │
│ │ Target Power Demand:        [ 5,000.0 ] kW (0.0 = Throttle Known)    │ │
│ │ Mechanical Efficiency (eta_m):[ 98.50 ] %                            │ │
│ │ Generator Efficiency (eta_g): [ 96.50 ] %                            │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ EXPANSION THERMODYNAMICS & GENERATION RESULTS (READ-ONLY) ────────┐ │
│ │ Throttle Steam Flow:    [ 42.850 ] TPH   Throttle Press: [2,500.0]kPa│
│ │ Throttle Temperature:   [ 380.0  ] °C    Exhaust Pressure:[ 200.0]kPa│
│ │ Exhaust Temperature:    [ 138.4  ] °C    Exhaust Enthalpy:[2,748 ]kJ │
│ │ Isentropic Enthalpy Drop:[ 582.4 ] kJ/kg Actual Drop (dh):[ 419.3]kJ │
│ │ Shaft Mechanical Power: [ 5,260.4] kW    Specific Steam: [  8.57 ]kg/kWh
│ │ Net Electrical Output:  [ 5,000.0] kWe (5.00 MWe) ⚡                 │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Isentropic Valid: PASS] [✓ Power Balance: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `stationClass` | Station Class | Enum | — | YES | `MECHANICAL_DRIVE` (Turbine) vs `TURBO_ALTERNATOR` (Turbogenerator). |
| `thermalMode` | Thermal Mode | Radio | — | YES | Maroon selector: `ISENTROPIC_EFF` vs `TEMPERATURE_OUT`. |
| `isentropicEff` | Isentropic Efficiency| Float | `%` | Dynamic | Active when `thermalMode == ISENTROPIC_EFF`. Range: $40.0 \text{ to } 92.0\%$. |
| `exhaustTemp` | Exhaust Temp Out | Float | `°C` | Dynamic | Active when `thermalMode == TEMPERATURE_OUT`. Exhaust steam temperature. |
| `pressureMode` | Pressure Mode | Radio | — | YES | Magenta selector: `DISCHARGE_PRESS`, `PRESSURE_DROP`, `FEEDBACK`. |
| `dischargePressure`| Discharge Pressure| Float| `kPa` | Dynamic | Active when `pressureMode == DISCHARGE_PRESS`. Backpressure held during simulation. |
| `pressureDrop` | Pressure Drop | Float | `kPa` | Dynamic | Active when `pressureMode == PRESSURE_DROP`. Expansion differential. |
| `useFeedback` | Pressure Feedback | Checkbox| — | Dynamic | Active when `pressureMode == FEEDBACK`. Inherits pressure from exhaust header. |
| `targetPowerKW` | Target Power Output| Float | `kW` | YES | $0.0 \implies$ calculates power from steam flow; $>0.0 \implies$ throttle steam is Required Flow. |
| `mechanicalEff` | Mechanical Efficiency| Float| `%` | YES | Shaft/gearbox efficiency ($85.0 \text{ to } 99.5\%$). |
| `generatorEff` | Generator Efficiency| Float | `%` | Dynamic | Active for Turbo Alternator ($85.0 \text{ to } 99.0\%$). Hidden/locked for Mechanical Drive. |

---

## 3. UI Reactive Logic & Bidirectional Power Solving
1. **Dynamic Reverse Solving**: If `targetPowerKW > 0.0`, the UI tags the inlet throttle steam port badge with `[R]` (Required Flow), notifying the user that boiler steam is automatically computed.
2. **Specific Steam Consumption Indicator**: Displays Specific Steam Consumption ($kg\text{ steam}/kWh$) dynamically as an efficiency benchmark.

---

## 4. Engineering Closure Badges
- **Mass Conservation Badge**: Green when $|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}| = 0.0$.
- **Thermodynamic Expansion Badge**: Green when $P_{\text{out}} < P_{\text{in}}$ and $h_{\text{out}} < h_{\text{in}}$.
- **Power Generation Badge**: Green when $\dot{W}_{\text{shaft}} > \dot{W}_{\text{elec}} > 0.0\text{ kW}$.
