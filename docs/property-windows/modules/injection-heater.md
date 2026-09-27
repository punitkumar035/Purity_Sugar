# Direct Injection Heater Property Window Specification
## Component Code: `PW-INJ-01`
### SUGARS Station Type Code: `13` | Object Tag Prefix: `INJ`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-INJ-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/injection-heater.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Injection_Heater/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [INJ] DIRECT INJECTION HEATER PROPERTY WORKSPACE                [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Massecuite Heater___] Station No [ 13 ] Tag [INJ-01]     │
├────────────────────────────────────────────────────────────────────────┤
│ [Operating Specs]  [Stream Connections]  [Dilution & Balances]         │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ HEATING CONTROL SPECIFICATION (MUTUALLY EXCLUSIVE / MAGENTA) ─────┐ │
│ │ (*) Temperature Out: [  90.0 ] °C (Target heated process discharge) │ │
│ │ ( ) Temperature Rise:[   7.5 ] K  (Degrees of temperature increase) │ │
│ │                                                                      │ │
│ │ Heat Loss to Ambient:[  0.50 ] % of transferred duty                │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ PROCESS DILUTION BEHAVIOR (HELP BOOK NOTICE) ─────────────────────┐ │
│ │ Direct steam injection condenses 100% into the process stream.       │ │
│ │ Steam heating flow is ALWAYS a Required Flow [R].                   │ │
│ │ Process dry substance (%Brix) will decrease due to dilution.         │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ CALCULATED INJECTION RESULTS & DILUTION (READ-ONLY) ──────────────┐ │
│ │ Inlet Juice Flow:    [ 100.000 ] TPH   Inlet Brix:  [  15.00 ] °Brix │
│ │ Injected Steam Flow: [   2.350 ] TPH   (Calculated Required Flow)    │
│ │ Outlet Juice Flow:   [ 102.350 ] TPH   Outlet Brix: [  14.65 ] °Brix 🔒
│ │ Temperature In → Out:[ 75.0 ] → [ 90.0 ] °C   Heat Duty: [ 1.45 ] MW │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Closure: 100.0%] [✓ DS Conservation: PASS] [✓ Enthalpy: PASS]  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Descriptive title |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag |
| `controlMode` | Control Mode | Enum | — | YES | `TEMP_OUT` vs `TEMP_RISE` (Mutually exclusive Magenta) |
| `temperatureOut`| Temperature Out | Float | `°C` | Dynamic | Active when `controlMode == 'TEMP_OUT'` |
| `temperatureRise`| Temperature Rise | Float | `K` | Dynamic | Active when `controlMode == 'TEMP_RISE'` |
| `heatLossPct` | Heat Loss | Float | `%` | YES | Ambient thermal loss (% of gross heat) |
