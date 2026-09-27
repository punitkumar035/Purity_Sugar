# Vacuum Condensers Station Property Window Specification
## Component Code: `PW-CND-01`
### SUGARS Station Type Codes: `21` (Contact) & `22` (Surface) | Object Tag Prefix: `CND`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CND-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/condensers.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Contact_Condenser/`, `Surface_Condenser/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [CND] VACUUM CONDENSER PROPERTY WORKSPACE                       [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Pan Barometric Cond_] Station No [ 21 ] Equip Tag [CND-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Condenser Type]  [Cooling Controls]  [Heat Transfer & Area]  [Balances]│
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ VACUUM & OPERATING CLASSIFICATION ────────────────────────────────┐ │
│ │ Condenser Class:            (o) Barometric Contact  ( ) Surface Cond │ │
│ │ Operating Vacuum Pressure:  [  16.00 ] kPa (Sat Temp: 55.3 °C) 🔒   │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ COOLING WATER FLOW MODES (MAGENTA MUTUALLY EXCLUSIVE) ────────────┐ │
│ │ Select Water Control Option:                                         │ │
│ │  ( ) Minimum Water to Condense All Vapor                             │ │
│ │  ( ) Target Water Out Temperature:  [ 45.00 ] °C                     │ │
│ │  (o) Temperature Approach:          [  4.00 ] K (T_tail = 51.3 °C)   │ │
│ │  ( ) Fixed Cooling Water Rate:      [ 120.00] TPH                    │ │
│ │  ( ) Water to Vapor Ratio:          [  25.0 ] kg/kg                  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ SURFACE CONDENSER CONTROLS (ACTIVE FOR SURFACE TYPE) ─────────────┐ │
│ │ [ ] Cooling Flow Required  Heat Loss: [ 0.50 ] % Cond Drop:[ 2.0 ] K │ │
│ │ Mode: (o) HTC: [1800.0] W/m²K  Area: [250.0] m²   ( ) Eff: [75.0] %  │ │
│ │ Flow Arrangement: (o) Countercurrent   ( ) Parallel                  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ CONDENSATION THERMODYNAMICS & STREAM RESULTS (READ-ONLY) ─────────┐ │
│ │ Process Vapor In:       [ 12.000 ] TPH   Vapor Enthalpy: [2,601.2]kJ/kg
│ │ Cooling Water Demand:   [285.400 ] TPH   Cooling Water In:[ 30.0 ] °C│
│ │ Tail Water Discharge:   [297.400 ] TPH   Tail Water Temp: [ 51.3 ] °C│
│ │ Condensation Heat Duty: [  7,980 ] kW    Approach Margin: [  4.0 ] K │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Complete Condensation: PASS] [✓ Vacuum Stable: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `condenserType` | Condenser Class | Enum | — | YES | `CONTACT` (direct mixing) vs `SURFACE` (segregated distillate). |
| `internalPressure`| Internal Vacuum | Float | `kPa` | YES | Operating vacuum pressure. Governs upstream pressure feedback. |
| `waterControlMode`| Water Mode Selector | Radio | — | YES | Magenta selector: `MIN_WATER`, `TEMP_OUT`, `APPROACH`, `QUANTITY`, `RATIO`. |
| `targetTempOut` | Target Temp Out | Float | `°C` | Dynamic | Active when `waterControlMode == TEMP_OUT`. |
| `approachTemp` | Approach Temp | Float | `K` | Dynamic | Active when `waterControlMode == APPROACH`. Difference $T_{\text{sat}} - T_{\text{tail}}$. |
| `fixedWaterRate`| Fixed Water Rate | Float | `TPH` | Dynamic | Active when `waterControlMode == QUANTITY`. |
| `waterToVaporRatio`| Water/Vapor Ratio | Float | `kg/kg`| Dynamic | Active when `waterControlMode == RATIO`. |
| `surfaceHTC` | Heat Transfer Coeff | Float | `W/(m²·K)`| Dynamic | Active for Surface Condenser. |
| `surfaceArea` | Surface Area | Float | `m²` | Dynamic | Active for Surface Condenser. |
| `effectivenessPct`| Thermal Effectiveness| Float| `%` | Dynamic | Maroon option for Surface Condenser. |
| `condensateDrop`| Condensate Drop | Float | `K` | Dynamic | Subcooling below saturation. |
| `flowDirection` | Flow Direction | Enum | — | Dynamic | `COUNTERCURRENT` vs `PARALLEL`. |
| `heatLossPct` | Heat Loss | Float | `%` | YES | % heat loss to ambient. |

---

## 3. UI Reactive Logic & Subcooling Interlocks
1. **Dynamic Saturation Display**: Whenever `internalPressure` changes, the corresponding saturation temperature $T_{\text{sat}}(P_{\text{vac}})$ is computed and rendered instantly.
2. **Contact vs. Surface Dynamic Tabs**: Switching between `CONTACT` and `SURFACE` automatically shows/hides the respective control panels and adjusts the stream schematic to show direct mixing vs. pure separated distillate.

---

## 4. Engineering Closure Badges
- **Mass Balance Badge**: Green when $|\sum \dot{m}_{\text{in}} - \sum \dot{m}_{\text{out}}| = 0.0$.
- **Complete Condensation Badge**: Green when no uncondensed vapor escapes the condenser.
- **Approach Temperature Badge**: Green when $T_{\text{tail}} < T_{\text{sat}}(P_{\text{vac}})$.
