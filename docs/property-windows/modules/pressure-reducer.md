# Pressure Reducer (PRV) Station Property Window Specification
## Component Code: `PW-PRV-01`
### SUGARS Station Type Code: `12` | Object Tag Prefix: `PRV`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-PRV-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/pressure-reducer.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Pressure_Reducer/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [PRV] PRESSURE REDUCING VALVE & LINE THROTTLE WORKSPACE         [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [HP to Exhaust PRV___] Station No [ 12 ] Equip Tag [PRV-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Pressure Specs]  [Joule-Thomson Exp]  [Desuperheating]  [Balances]    │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISCHARGE PRESSURE CONTROL (MAGENTA MUTUALLY EXCLUSIVE) ──────────┐ │
│ │ Select Pressure Mode:                                                │ │
│ │  (o) Pressure Out:          [ 150.0 ] kPa                            │ │
│ │  ( ) Pressure Drop:         [  20.0 ] kPa (Allows feedback pass-thru)│ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ DESUPERHEATING WATER CONTROL (OPTIONAL SPRAY QUENCH) ─────────────┐ │
│ │ [X] Enable Desuperheating Spray Water (Port 1 In)                    │ │
│ │ Target Superheat Above Sat: [   5.0 ] K                              │ │
│ │ Quench Water Source:        [ Boiler Feedwater / Condensate @ 90°C ] │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ THROTTLING THERMODYNAMICS & STREAM RESULTS (READ-ONLY) ───────────┐ │
│ │ Inlet Pressure:         [ 350.0 ] kPa    Outlet Pressure:[ 150.0 ]kPa│
│ │ Inlet Temperature:      [ 180.0 ] °C     Outlet Temp:    [ 125.4 ] °C│
│ │ Inlet Enthalpy:         [2,820.5] kJ/kg  Outlet Enthalpy:[2,735.0]kJ/kg
│ │ Motive Steam Flow:      [ 20.000] TPH    Quench Water Req:[ 0.650]TPH│
│ │ Throttled Total Flow:   [ 20.650] TPH    Vapour Quality: [ 1.000 ] 🔒│
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Isenthalpic Expansion: PASS] [✓ Superheat: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `pressureMode` | Pressure Mode | Radio | — | YES | Magenta mutually exclusive selector: `PRESSURE_OUT` vs `PRESSURE_DROP`. |
| `pressureOut` | Pressure Out | Float | `kPa` | Dynamic | Active when `pressureMode == PRESSURE_OUT`. Must satisfy $P_{\text{out}} < P_{\text{in}}$. |
| `pressureDrop` | Pressure Drop | Float | `kPa` | Dynamic | Active when `pressureMode == PRESSURE_DROP`. Allows pressure feedback to pass upstream. |
| `enableDesuperheating`| Desuperheating Spray| Checkbox| — | YES | Activates Port 1 quench spray water mass & energy balance. |
| `targetSuperheatK`| Target Superheat Margin| Float | `K` | Dynamic | Active when desuperheating is enabled. Target temperature $T_{\text{sat}}(P_{\text{out}}) + \Delta T_{\text{sh}}$. |

---

## 3. Reactive State Dependencies & Feedback Pass-Through
1. **Upstream Pressure Feedback**: When `pressureMode == PRESSURE_DROP`, downstream receiver pressure $P_{\text{dest}}$ passes back as:
   $$P_{\text{feed,required}} = P_{\text{dest}} + \text{pressureDrop}$$
2. **Phase Diagram Verification**: The UI evaluates quality $x_{\text{out}}$. If throttling into the wet steam dome occurs ($x < 1.0$), a notification badge indicates the moisture droplet percentage formed.

---

## 4. Engineering Closure Badges
- **Mass Closure Badge**: Green when $|\dot{m}_{\text{in}} + \dot{m}_{\text{spray}} - \dot{m}_{\text{out}}| = 0.0$.
- **Pressure Drop Badge**: Green when $P_{\text{out}} < P_{\text{in}}$.
- **Isenthalpic Conservation Badge**: Green when $|h_{\text{out}} - h_{\text{in}}| < 0.01 \text{ kJ/kg}$ (without spray).
