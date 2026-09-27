# Sugar Dryer Station Property Window Specification
## Component Code: `PW-DRY-01`
### SUGARS Station Type Code: `8` | Object Tag Prefix: `DRY`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-DRY-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-dryer.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Dryer/`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [DRY] SUGAR DRYER PROPERTY WORKSPACE                            [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Station Name [Sugar Drum Dryer____] Station No [ 08 ] Equip Tag [DRY-01]
├────────────────────────────────────────────────────────────────────────┤
│ [Drying Controls]  [Air & Thermal]  [Dust Loss & Evap]  [Balances]     │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ PRODUCT QUALITY & MOISTURE TARGETS ───────────────────────────────┐ │
│ │ Target Dry Substance (TDM): [ 99.97 ] % (Moisture: 0.030 %)        │ │
│ │ Sugar Out Temperature:      [ 45.00 ] °C                           │ │
│ │ Dry Matter Loss (Dust Entr):[ 50.00 ] mg/kg dry matter (PPM)       │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ HEATING MEDIUM & PSYCHROMETRIC BALANCES ──────────────────────────┐ │
│ │ Heating Type:               (o) Saturated Steam (Latent, eps=0.0)  │ │
│ │                             ( ) Hot Condensate / Water             │ │
│ │ Heat Loss to Surroundings:  [ 25.00 ] % of transferred heat        │ │
│ │ Condensate Heating Eff (%): [  0.00 ] % (Active for liquid heating)│ │
│ └────────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ EVAPORATION & MASS BALANCE RESULTS (READ-ONLY) ───────────────────┐ │
│ │ Dried Sugar Flow:       [ 49.520 ] TPH   Final Moisture:[ 0.030 ] % 🔒
│ │ Moisture Evaporated:    [  0.478 ] TPH   Dust Loss:     [ 0.002 ] TPH│
│ │ Net Thermal Duty:       [  328.4 ] kW    Gross Heat Duty:[ 437.9 ] kW│
│ │ Sensible Heat Contrib:  [  -42.5 ] kW    Exhaust Vapour:[  0.480] TPH│
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Mass Balance: PASS] [✓ Dry Substance: PASS] [✓ Moisture Target: PASS]
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `stationName` | Station Name | String | — | YES | Equipment descriptive title (up to 20 chars). |
| `stationNumber` | Station Number | Integer | — | YES | Unique plant station ID. |
| `equipmentTag` | Equipment Tag | String | — | YES | Plant asset tag (up to 11 chars). |
| `targetDryMatterPct`| Target Dry Substance | Float | `%` | YES | Conditioned sugar commercial target ($100 - \% \text{moisture}$). Valid range: $95.00 \text{ to } 99.99\%$. Default: $99.97\%$. |
| `outputTemperatureC`| Sugar Out Temp | Float | `°C` | YES | Conditioned sugar discharge temperature. If lower than inlet, sensible heat aids flashing. Valid: $25.0 \text{ to } 90.0\text{ °C}$. |
| `dryMatterLossPPM` | Dry Matter Loss | Float | `mg/kg`| YES | Fine crystal entrainment in exhaust air per unit dry substance entering. Typical $30 \text{ to } 100\text{ PPM}$. Valid: $0.0 \text{ to } 500.0\text{ PPM}$. |
| `heatLossPercent` | Heat Loss | Float | `%` | YES | Thermal loss to environment as % of total heat transferred. Valid: $0.0 \text{ to } 60.0\%$. Default: $25.0\%$. |
| `heatingType` | Heating Medium Type | Enum | — | YES | `STEAM` (latent heat condensation) vs `LIQUID_CONDENSATE` (sensible liquid-liquid cooling). |
| `heatingEffectiveness`| Heating Effectiveness| Float | `%` | Dynamic | Dimmed and locked to $0.0\%$ when `heatingType == STEAM`. Active when liquid condensate is used ($10.0\% \text{ to } 90.0\%$). |

---

## 3. Reactive State Dependencies & Mathematical Verification

1. **Target Moisture Reciprocal**:
   $$\% \text{Moisture}_{\text{out}} = 100.0 - \text{targetDryMatterPct}$$
   Displays dynamically beside the Dry Substance input field.
2. **Dust Loss Calculation**:
   $$\dot{m}_{\text{dust}} = \dot{m}_{\text{sugar,in}} \times \left(\frac{\text{DS}_{\text{in}}}{100}\right) \times \left(\frac{\text{dryMatterLossPPM}}{10^6}\right)$$
3. **Moisture Evaporated Rate**:
   $$\dot{m}_{\text{evap}} = \dot{m}_{\text{sugar,in}} - \dot{m}_{\text{sugar,out}} - \dot{m}_{\text{dust}}$$
4. **Energy Balance & Duty**:
   $$\dot{Q}_{\text{gross}} = \frac{\dot{m}_{\text{sugar,out}} h_{\text{sugar}}(T_{\text{out}}) - \dot{m}_{\text{sugar,in}} h_{\text{sugar}}(T_{\text{in}}) + \dot{m}_{\text{evap}} \Delta h_{\text{vap}}(T_{\text{out}})}{1.0 - \text{heatLossPercent}/100}$$

---

## 4. Engineering Closure Badges
- **Mass Balance Badge**: Green when $|\sum \dot{m}_{\text{in}} - \sum \dot{m}_{\text{out}}| / \sum \dot{m}_{\text{in}} < 10^{-4}$.
- **Dry Substance Badge**: Green when $|\dot{m}_{\text{DS,in}} - (\dot{m}_{\text{DS,out}} + \dot{m}_{\text{dust}})| < 10^{-5} \text{ kg/h}$.
- **Moisture Target Badge**: Green when $|\text{DS}_{\text{out}} - \text{targetDryMatterPct}| < 0.001\%$.
