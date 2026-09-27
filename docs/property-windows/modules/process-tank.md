# Process Tank Station Property Window Specification
## Component Code: `PW-TNK-01`
### SUGARS Station Type Code: `14` | Object Tag Prefix: `TNK`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-TNK-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/process-tank.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Tank/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [TNK] PROCESS TANK & MIXING BUFFER PROPERTY WORKSPACE           [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Syrup Buffer Tank___] Station No [ 14 ] Equip Tag [TNK-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Storage & Flow]  [Dilution (Port 9)]  [Heating (Port 10)]  [Balances] │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ STORAGE ACCUMULATION / DEPLETION (MAGENTA MUTUALLY EXCLUSIVE) ─────┐ │
│ │ Select Storage Mode:                                                 │ │
│ │  ( ) Flow to Storage:       [   0.00 ] m³/h (Tank level rising)      │ │
│ │  ( ) Flow from Storage:     [   0.00 ] m³/h (Tank level falling)     │ │
│ │  (o) Steady State (Zero Accumulation)                                │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ DILUTION & HEATING CONTROL INTERFACE ─────────────────────────────┐ │
│ │ Hold TDM at (%):            [ 65.00 ] % (Controls Port 9 Diluent)    │ │
│ │ Target Out Temperature:     [ 85.00 ] °C (Controls Port 10 Steam)    │ │
│ │ Heating Type:               (o) Injection (steam dilutes liquor)     │ │
│ │                             ( ) Coil (condensate leaves via Port 1)  │ │
│ │ Color Rise:                 [  2.50 ] %    Heat Loss: [ 1.50 ] %     │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ REQUIRED FLOW SELECTION (ACTIVE WHEN TANK OUTLET IS REQUIRED) ─────┐ │
│ │ Downstream Demand: 120.000 TPH                                       │ │
│ │ Select inlet to balance: (o) Port 0: Raw Juice   ( ) Port 1: Filtrate│ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ TANK STREAM RESULTS & BALANCES (READ-ONLY) ───────────────────────┐ │
│ │ Combined Inflow:        [115.000 ] TPH   Storage Rate:   [  0.00 ]TPH│
│ │ Diluent Water (Port 9): [  3.450 ] TPH   Heating Steam:  [  1.55 ]TPH│
│ │ Process Liquor Out:     [120.000 ] TPH   Discharge Brix: [ 65.00 ]°Bx│
│ │ Condensate Out (Coil):  [  0.000 ] TPH   Discharge Temp: [ 85.00 ] °C│
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Brix Match: PASS] [✓ Thermal Closure: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `storageMode` | Storage Mode | Radio | — | YES | Magenta mutually exclusive selector: `TO_STORAGE`, `FROM_STORAGE`, `NONE`. |
| `flowToStorage`| Flow to Storage | Float | `m³/h` | Dynamic | Active when `storageMode == TO_STORAGE`. |
| `flowFromStorage`| Flow from Storage | Float | `m³/h` | Dynamic | Active when `storageMode == FROM_STORAGE`. |
| `holdTdmPct` | Hold TDM at (%) | Float | `%` | Dynamic | Modulates Port 9 diluent flow rate. Dimmed if Port 9 is disconnected. |
| `temperatureOut`| Target Out Temp | Float | `°C` | Dynamic | Modulates Port 10 heating flow rate. Dimmed if Port 10 is disconnected. |
| `heatingType` | Heating Type | Enum | — | YES | `INJECTION` (diluting steam) vs `COIL` (indirect heating with condensate discharge). |
| `colorRise` | Color Rise | Float | `%` / `CU` | YES | Color formation across residence time. |
| `heatLossPct` | Heat Loss | Float | `%` | YES | % loss of transferred thermal duty. |
| `requiredInlet` | Required Flow Inlet| Port ID | — | Dynamic | Active only when tank outlet is demanded downstream. Selects balancing inlet stream. |

---

## 3. Port Activation & Gating Rules
1. **Port 9 Interlock**: If no stream is attached to Port 9, `holdTdmPct` is disabled and greyed out with label `[Port 9 Unconnected]`.
2. **Port 10 Interlock**: If no steam stream is attached to Port 10, `temperatureOut` is disabled and greyed out with label `[Port 10 Unconnected]`.
3. **Required Flow Dialog**: Automatically surfaces when `outflow.isRequired == true`, enumerating all connected input ports from which the balancing fluid can be drawn.

---

## 4. Engineering Closure Badges
- **Mass Balance Badge**: Green when $|\sum \dot{m}_{\text{in}} - (\dot{m}_{\text{out}} + \dot{m}_{\text{cond}} + \dot{m}_{\text{storage}})| < 10^{-4}$.
- **Brix Match Badge**: Green when $|\text{TDM}_{\text{out}} - \text{holdTdmPct}| < 0.001\%$.
- **Energy Conservation Badge**: Green when enthalpy balance closes within $0.01\%$.
