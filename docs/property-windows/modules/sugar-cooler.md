# Sugar Cooler Station Property Window Specification
## Component Code: `PW-CLR-01`
### SUGARS Station Type Code: `7` | Object Tag Prefix: `CLR`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CLR-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-cooler.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Cooler/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [CLR] PROCESS COOLER & HEAT LOSS PROPERTY WORKSPACE             [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Product Sugar Cooler] Station No [ 07 ] Equip Tag [CLR-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Cooling Modes]  [Thermodynamics]  [Supersaturation]  [Balances]       │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ COOLING & HEAT LOSS SPECIFICATION (MAGENTA MUTUALLY EXCLUSIVE) ───┐ │
│ │ Select exactly ONE cooling method:                                   │ │
│ │  (o) Temperature Drop:      [  5.00 ] °C / K                         │ │
│ │  ( ) Temperature Out:       [ 35.00 ] °C                             │ │
│ │  ( ) Heat Loss in Percent:  [  5.00 ] % of inlet enthalpy            │ │
│ │  ( ) Heat Loss in Enthalpy: [ 20.00 ] kJ/kg                          │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ PROCESS STREAM INTEGRITY & PHYSICAL CONSTRAINTS ──────────────────┐ │
│ │ Sucrose Crystal Growth:     [ DISABLED (Sugar's Help Book Rule) ] 🔒 │
│ │ Crystal In:  [ 45.000 ] TPH ───► Crystal Out: [ 45.000 ] TPH 🔒      │ │
│ │ Vapour Phase Condensation:  [ AUTOMATIC EQUILIBRIUM SOLVER ] 🔒     │ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ DISCHARGE PROPERTIES & CRYSTALLIZATION RISK (READ-ONLY) ──────────┐ │
│ │ Outlet Temperature:     [ 35.00 ] °C     Outlet Pressure:[101.3 ] kPa│
│ │ Enthalpy Out:           [ 142.5 ] kJ/kg  Enthalpy Drop:  [ 21.0 ]kJ/kg│
│ │ Thermal Duty Removed:   [ 262.5 ] kW     Condensate Form:[  0.0 ] TPH│
│ │ Dissolved Brix:         [ 68.20 ] °Bx    Supersaturation:[ 1.18 ] ⚠️ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Crystal Invariant: PASS] [✓ Energy Closure: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `coolingMode` | Cooling Mode Selector | Radio | — | YES | Magenta mutual exclusion selector. Options: `TEMP_DROP`, `TEMP_OUT`, `HEAT_LOSS_PCT`, `HEAT_LOSS_KJ`. |
| `tempDrop` | Temperature Drop | Float | `K` / `°C`| Dynamic | Active when `coolingMode == TEMP_DROP`; grayed out otherwise. Valid: $0.1 \text{ to } 60.0\text{ K}$. |
| `tempOut` | Temperature Out | Float | `°C` | Dynamic | Active when `coolingMode == TEMP_OUT`; grayed out otherwise. Must be strictly lower than inlet temperature. |
| `heatLossPct` | Heat Loss in Percent | Float | `%` | Dynamic | Active when `coolingMode == HEAT_LOSS_PCT`; grayed out otherwise. Valid: $0.1 \text{ to } 100.0\%$. |
| `heatLossKJ` | Heat Loss in Enthalpy| Float | `kJ/kg`| Dynamic | Active when `coolingMode == HEAT_LOSS_KJ`; grayed out otherwise. Valid: $1.0 \text{ to } 2500.0\text{ kJ/kg}$. |

---

## 3. UI Reactive Logic & Magenta Enforcement
1. **Radio Exclusivity**: Selecting any of the 4 radio buttons automatically activates its corresponding numeric input field and dims/disables the other three inputs.
2. **Supersaturation Warning**: If cooling drives the mother liquor supersaturation ratio above $1.15$, a yellow warning badge (`⚠️ HIGH SUPERSATURATION (SS = X.XX)`) is shown, notifying the engineer that spontaneous nucleation or high viscosity may occur in downflow handling.
3. **Crystal Conservation**: The property window displays an explicit locked indicator showing that crystal mass flow is invariant across the cooler.

---

## 4. Engineering Closure Badges
- **Mass Balance Badge**: Green when $|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}| = 0.0$.
- **Crystal Invariant Badge**: Green when $|\dot{m}_{\text{cryst,in}} - \dot{m}_{\text{cryst,out}}| = 0.0$.
- **Thermodynamic Consistency Badge**: Green when $h_{\text{out}} \le h_{\text{in}}$ and $T_{\text{out}} \le T_{\text{in}}$.
