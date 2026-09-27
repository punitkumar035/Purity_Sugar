# Process Pump Station Property Window Specification
## Component Code: `PW-PMP-01`
### SUGARS Station Type Code: `11` | Object Tag Prefix: `PMP`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-PMP-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/process-pump.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Pump/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [PMP] PROCESS PUMP & HYDRAULIC DRIVE PROPERTY WORKSPACE         [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Juice Feed Pump_____] Station No [ 11 ] Equip Tag [PMP-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Pressure & Head]  [Efficiencies]  [Motor & Power]  [Balances]         │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISCHARGE PRESSURE SPECIFICATION (MAGENTA MUTUALLY EXCLUSIVE) ────┐ │
│ │ Select Pressure Mode:                                                │ │
│ │  (o) Discharge Pressure:    [ 350.0 ] kPa                            │ │
│ │  ( ) Pressure Rise (Delta P):[250.0 ] kPa                            │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ HYDRAULIC & MOTOR EFFICIENCIES ───────────────────────────────────┐ │
│ │ Hydraulic / Impeller Eff:   [ 72.00 ] %                              │ │
│ │ Electric Motor Efficiency:  [ 92.00 ] %                              │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ PUMPING HYDRAULICS & POWER CONSUMPTION (READ-ONLY) ───────────────┐ │
│ │ Suction Pressure:       [ 101.3 ] kPa    Discharge Press:[ 350.0 ]kPa│
│ │ Differential Head:      [  23.8 ] m LC   Liquid Density: [1,065.0]kg/m³
│ │ Volumetric Flow Rate:   [  93.9 ] m³/h   Mass Flow Rate: [100.00 ]TPH│
│ │ Hydraulic Power (Whyd): [   6.48] kW     Shaft Power (BHP):[ 9.00] kW│
│ │ Electric Motor Demand:  [   9.78] kW     Fluid Temp Rise:[ +0.07 ] K │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Pressure Boost: PASS] [✓ NPSH Adequate: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `pressureMode` | Pressure Mode | Radio | — | YES | Magenta mutually exclusive selector: `PRESSURE_OUT` vs `PRESSURE_RISE`. |
| `dischargePressure`| Discharge Pressure | Float | `kPa` | Dynamic | Active when `pressureMode == PRESSURE_OUT`. Must satisfy $P_{\text{out}} > P_{\text{in}}$. |
| `pressureRise` | Pressure Rise | Float | `kPa` | Dynamic | Active when `pressureMode == PRESSURE_RISE`. Differential boost $\Delta P$. |
| `hydraulicEff` | Hydraulic Efficiency | Float | `%` | YES | Impeller fluid efficiency $\eta_{\text{hyd}}$ ($30.0 \text{ to } 90.0\%$). |
| `motorEff` | Motor Efficiency | Float | `%` | YES | Electric motor efficiency $\eta_{\text{motor}}$ ($70.0 \text{ to } 98.0\%$). |

---

## 3. Physical State & Flashing Prevention
1. **Dynamic Head Conversion**:
   $$\text{Head } H = \frac{\Delta P \times 1000}{\rho_{\text{mix}} \times g} \quad [\text{m of liquid column}]$$
2. **Flash Prevention**: Ensures fluid discharge pressure exceeds vapor saturation pressure at process temperature ($P_{\text{out}} > P_{\text{sat}}(T)$), suppressing boiling in downstream tubular heaters.

---

## 4. Engineering Closure Badges
- **Mass Closure Badge**: Green when $|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}| = 0.0$.
- **Pressure Boost Badge**: Green when $P_{\text{out}} > P_{\text{in}}$.
- **Power Validity Badge**: Green when $\dot{W}_{\text{elec}} > 0.0\text{ kW}$.
