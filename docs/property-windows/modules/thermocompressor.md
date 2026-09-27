# Thermocompressor Station Property Window Specification
## Component Code: `PW-TCM-01`
### SUGARS Station Type Code: `10` | Object Tag Prefix: `TCM`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-TCM-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/thermocompressor.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Thermocompressor/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [TCM] STEAM JET THERMOCOMPRESSOR PROPERTY WORKSPACE             [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Pan Thermocompressor] Station No [ 10 ] Equip Tag [TCM-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Pressure Specs]  [Performance Modes]  [Truffault Model]  [Balances]   │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISCHARGE PRESSURE SPECIFICATION (MAROON EXCLUSIVE) ──────────────┐ │
│ │ Select Pressure Mode:                                                │ │
│ │  (o) Fixed Discharge Pressure:  [ 145.0 ] kPa                        │ │
│ │  ( ) Pressure Feedback:         [ DOWNSTREAM CALANDRIA ] [ ] Active  │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ ENTRAINMENT PERFORMANCE MODE (MAGENTA MUTUALLY EXCLUSIVE) ────────┐ │
│ │ Select exactly ONE governing performance mode:                       │ │
│ │  (o) Efficiency (Truffault):    [ 85.00 ] % (5% nozzle wear included)│ │
│ │  ( ) Entrainment Ratio (mu):    [  0.45 ] kg suction / kg motive     │ │
│ │  ( ) Discharge Temperature:     [ 115.0 ] °C                         │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ THERMODYNAMIC MIXING & STEAM RESULTS (READ-ONLY) ─────────────────┐ │
│ │ Motive Steam (P0):      [  6.000 ] TPH   Motive Pressure:[ 600.0 ]kPa│
│ │ Suction Vapor (P1):     [  2.700 ] TPH   Suction Press:  [  50.0 ]kPa│
│ │ Boosted Discharge (Out):[  8.700 ] TPH   Discharge Press:[ 145.0 ]kPa│
│ │ Calculated Entrainment: [  0.450 ] kg/kg Compression Rat:[  2.90 ] 🔒│
│ │ Discharge Sat Temp:     [ 110.4  ] °C    Discharge Enthal:[2,710 ]kJ/kg
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Pressure Hierarchy: PASS] [✓ Enthalpy Closure: PASS]
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
| `pressureOut` | Discharge Pressure | Float | `kPa` | Dynamic | Active when `pressureMode == SPECIFIED`. Range: $20.0 \text{ to } 1000.0\text{ kPa}$. |
| `useFeedback` | Feedback Active | Checkbox | — | Dynamic | Active when `pressureMode == FEEDBACK`. Inherits discharge $P$ from receiver/calandria. |
| `performanceMode`| Performance Selector | Radio | — | YES | Magenta mutually exclusive selector: `EFFICIENCY`, `ENTRAINMENT_RATIO`, `TEMPERATURE_OUT`. |
| `efficiencyPct` | Efficiency (Truffault)| Float| `%` | Dynamic | Active when `performanceMode == EFFICIENCY`. Evaluates Truffault formula with 5% nozzle wear allowance. |
| `entrainmentRatio`| Entrainment Ratio | Float | `kg/kg`| Dynamic | Active when `performanceMode == ENTRAINMENT_RATIO`. Typical range: $0.10 \text{ to } 1.50$. |
| `dischargeTemp` | Discharge Temp | Float | `°C` | Dynamic | Active when `performanceMode == TEMPERATURE_OUT`. Must be higher than suction temperature. |

---

## 3. UI Reactive Logic & Physics Enforcement
1. **Pressure Hierarchy Verification**: The UI immediately checks:
   $$P_{\text{mot}} > P_{\text{out}} > P_{\text{suct}}$$
   If violated, an alert badge is rendered: `❌ INVALID PRESSURE HIERARCHY: Motive pressure must exceed discharge pressure, which must exceed suction pressure.`
2. **Mutual Exclusion Gating**: Clicking any radio option dims and disables the non-selected fields in the Magenta section.

---

## 4. Engineering Closure Badges
- **Mass Closure Badge**: Green when $|\dot{m}_{\text{mot}} + \dot{m}_{\text{suct}} - \dot{m}_{\text{out}}| = 0.0$.
- **Pressure Hierarchy Badge**: Green when $P_{\text{mot}} > P_{\text{out}} > P_{\text{suct}}$.
- **Energy Conservation Badge**: Green when $|\dot{m}_{\text{mot}} h_{\text{mot}} + \dot{m}_{\text{suct}} h_{\text{suct}} - \dot{m}_{\text{out}} h_{\text{out}}| / (\dot{m}_{\text{out}} h_{\text{out}}) < 10^{-4}$.
