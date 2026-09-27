# STENCIL SPECIFICATION: Sugar Dryer Station
## Module Identifier: `STENCIL-DRY-01`
### Station Type Code: `8` | SUGARS Classification: Sugar Dryer

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Dryer/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Psychrometric Enthalpy Balance, Free Moisture Evaporation, Bound Moisture Equilibrium  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Sugar Dryer station reduces the moisture content of wet crystalline sugar discharged from centrifugals (typically $0.5\% \text{ to } 2.0\%$ moisture) down to conditioned commercial sugar standards ($0.02\% \text{ to } 0.05\%$ moisture, corresponding to $99.95\% \text{ to } 99.98\%$ Dry Substance).

### Key Operating Principles from Sugar's Help Book:
1. **Evaporation Mechanism**: Water in the incoming wet sugar is vaporized into an air stream, or flashed due to sensible heat.
2. **Dry Matter Loss (PPM)**: Accounts for dust entrainment and fine crystal carryover in exhaust air (expressed in parts per million, $mg/kg$ of total dry matter entering the dryer; typical values $30 \text{ to } 100\text{ PPM}$).
3. **Heat Loss (%)**: Significant heat loss occurs to the surroundings and exhaust air (typically $15\% \text{ to } 45\%$ of total heat transfer).
4. **Condensate / Liquid Heating Effectiveness**: When liquid hot water or condensate is used for indirect air heating, effectiveness $\epsilon$ ($10\% \text{ to } 50\%$) governs heat exchange. For steam, $\epsilon = 0.0$ (latent condensation governs).
5. **Output Temperature & Flashing**: If output sugar temperature is lower than input temperature, sensible heat release contributes to moisture vaporization.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Wet Sugar Feed In** | IN | `material` | Crystalline Sugar | Multi-component wet sugar | Known upstream flow |
| **Port 1 In** | **Drying Air / Heating In** | IN | `any` / `thermal` | Air / Steam | Conditioning air or heating medium | Independent inlet flow |
| **Port 0 Out**| **Dried Product Sugar Out** | OUT | `material` | Dry Sugar | Commercial sugar ($DS \ge 99.9\%$) | Calculated consequence |
| **Port 1 Out**| **Exhaust Air / Vapour Out**| OUT | `any` / `thermal` | Exhaust Air | Moist exhaust air carrying evaporated water | Consequence of evaporation |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `DRY-01` | Up to 11 chars | Plant equipment asset tag |
| `targetDryMatterPct`| `float` | `%` | 99.97 | 95.0 – 99.99 | Output sugar dry substance ($100 - \% \text{moisture}$) |
| `outputTemperatureC`| `float` | `°C` | 45.0 | 25.0 – 90.0 | Output sugar temperature |
| `dryMatterLossPPM` | `float` | `mg/kg`| 50.0 | 0.0 – 500.0 | Dust loss in exhaust air per unit dry matter |
| `heatLossPercent` | `float` | `%` | 25.0 | 0.0 – 60.0 | Heat lost to surroundings (% of transferred heat) |
| `heatingEffectiveness`| `float`| `%` | 0.0 | 0.0 – 90.0 | Active only when heating medium is liquid condensate |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Dry Matter & Water Balances
$$\dot{m}_{\text{DS,in}} = \dot{m}_{\text{sugar,in}} \times \left(\frac{\text{DS}_{\text{in}}}{100}\right)$$
$$\dot{m}_{\text{DS,lost}} = \dot{m}_{\text{DS,in}} \times \left(\frac{\text{dryMatterLossPPM}}{10^6}\right)$$
$$\dot{m}_{\text{DS,out}} = \dot{m}_{\text{DS,in}} - \dot{m}_{\text{DS,lost}}$$
$$\dot{m}_{\text{sugar,out}} = \frac{\dot{m}_{\text{DS,out}}}{\text{targetDryMatterPct} / 100}$$
$$\dot{m}_{\text{evaporated}} = \dot{m}_{\text{sugar,in}} - \dot{m}_{\text{sugar,out}} - \dot{m}_{\text{DS,lost}}$$

### 4.2 Enthalpy & Thermal Duty
$$\dot{Q}_{\text{sugar}} = \dot{m}_{\text{sugar,out}} h_{\text{sugar}}(T_{\text{out}}) - \dot{m}_{\text{sugar,in}} h_{\text{sugar}}(T_{\text{in}})$$
$$\dot{Q}_{\text{evap}} = \dot{m}_{\text{evaporated}} \times \Delta h_{\text{vap}}(T_{\text{out}})$$
$$\dot{Q}_{\text{net}} = \dot{Q}_{\text{sugar}} + \dot{Q}_{\text{evap}}$$
$$\dot{Q}_{\text{gross}} = \frac{\dot{Q}_{\text{net}}}{1.0 - \text{heatLossPercent}/100}$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|(\dot{m}_{\text{sugar,in}} + \dot{m}_{\text{air,in}}) - (\dot{m}_{\text{sugar,out}} + \dot{m}_{\text{exhaust,out}})|}{\dot{m}_{\text{sugar,in}} + \dot{m}_{\text{air,in}}} < 0.0001$$
2. **Dry Substance Conservation**:
   $$\epsilon_{\text{DS}} = \frac{|\dot{m}_{\text{DS,in}} - (\dot{m}_{\text{DS,out}} + \dot{m}_{\text{DS,lost}})|}{\dot{m}_{\text{DS,in}}} < 0.00001$$
