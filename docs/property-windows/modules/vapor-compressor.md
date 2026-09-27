# Vapor Compressor (MVR) Station Property Window Specification
## Component Code: `PW-CMP-01`
### SUGARS Station Type Code: `9` | Object Tag Prefix: `CMP`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CMP-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/vapor-compressor.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Compressor/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [CMP] MECHANICAL VAPOR COMPRESSOR (MVR) PROPERTY WORKSPACE      [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [1st Vapor Compressor] Station No [ 09 ] Equip Tag [CMP-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Pressure & Power]  [Efficiencies]  [Thermal & Superheat]  [Balances]  │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISCHARGE PRESSURE SPECIFICATION (MAROON EXCLUSIVE) ──────────────┐ │
│ │ Select Pressure Control Mode:                                        │ │
│ │  (o) Fixed Discharge Pressure:  [ 200.0 ] kPa                        │ │
│ │  ( ) Pressure Feedback:         [ DOWNSTREAM RECEIVER ] [ ] Active   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ THERMAL & COMPRESSION EFFICIENCY ─────────────────────────────────┐ │
│ │ Mode: (o) Specify Efficiencies     ( ) Specify Discharge Temp        │ │
│ │ Isentropic Efficiency (eta_s):  [ 75.00 ] %                          │ │
│ │ Mechanical Drive Efficiency:    [ 95.00 ] %                          │ │
│ │ Target Discharge Temp:          [ 135.0 ] °C (Sat: 120.2 °C, SH:+14.8K│
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ COMPRESSION WORK & STREAM RESULTS (READ-ONLY) ────────────────────┐ │
│ │ Vapor Throughput:       [ 15.000 ] TPH   Pressure Ratio: [  2.35 ] 🔒│
│ │ Enthalpy Rise (dh):     [ 185.4  ] kJ/kg Saturation Temp:[ 120.2 ] °C│
│ │ Gas Power Required:     [ 772.5  ] kW    Shaft Power:    [ 813.2 ] kW│
│ │ Outlet Vapor Enthalpy:  [ 2,745.2] kJ/kg Superheat Margin:[+14.8 ] K │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Superheat Valid: PASS] [✓ Isentropic: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `pressureMode` | Pressure Mode | Radio | — | YES | Maroon mutually exclusive selector: `SPECIFIED` vs `FEEDBACK`. |
| `dischargePressure`| Discharge Pressure | Float | `kPa` | Dynamic | Active when `pressureMode == SPECIFIED`. Range: $10.0 \text{ to } 2500.0\text{ kPa}$. |
| `useFeedback` | Feedback Active | Checkbox | — | Dynamic | Active when `pressureMode == FEEDBACK`. Inherits discharge $P$ from receiver/downstream. |
| `isentropicEff` | Isentropic Efficiency| Float | `%` | Dynamic | Percentage of theoretical isentropic work to actual gas work. Range: $50.0 \text{ to } 95.0\%$. |
| `dischargeTemp` | Discharge Temp | Float | `°C` | Dynamic | Superheated discharge vapor temperature. Sugar's Help Book mandates $T_{\text{out}} \ge T_{\text{sat}}(P_{\text{out}})$. |
| `mechanicalEff` | Mechanical Efficiency| Float | `%` | YES | Shaft coupling & bearing transmission efficiency. Range: $80.0 \text{ to } 99.5\%$. |

---

## 3. UI Reactive Logic & Superheat Safety
1. **Saturation Temperature Interlock**: When $P_{\text{out}}$ changes, the UI calculates $T_{\text{sat}}(P_{\text{out}})$ via CoolProp / Steam Tables in real-time. If user inputs $T_{\text{out}} < T_{\text{sat}}$, the property window marks the field in red with:
   `❌ PHYSICAL VIOLATION: Discharge temperature cannot be below saturation temperature (Condensation forbidden in MVR).`
2. **Pressure Ratio Display**: Automatically computes and displays $r_p = P_{\text{out}} / P_{\text{in}}$.

---

## 4. Engineering Closure Badges
- **Mass Closure Badge**: Green when $|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}| = 0.0$.
- **Superheat Badge**: Green when $T_{\text{out}} \ge T_{\text{sat}}(P_{\text{out}})$.
- **Thermodynamic Direction Badge**: Green when $P_{\text{out}} > P_{\text{in}}$ and $h_{\text{out}} > h_{\text{in}}$.
