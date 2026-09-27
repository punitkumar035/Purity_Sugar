# STENCIL SPECIFICATION: Flash Tank Station
## Module Identifier: `STENCIL-FLS-01`
### Station Type Code: `13` | SUGARS Classification: Condensate & Liquor Flash Tank

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Flash_Tank/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Isenthalpic Flash Evaporation, Boiling Point Elevation (BPE), Entrainment Sugar Loss in Vapor  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Flash Tank station models adiabatic flash vapor recovery from high-pressure process condensate (e.g., from 1st and 2nd evaporator calandrias, vacuum pans, or juice heaters) or hot process liquor (e.g., flashed clear juice or clarified juice). Flashing occurs without external heating, releasing low-pressure flash vapor that is routed to lower-pressure evaporator effects or preheaters.

### Key Operating Principles from Sugar's Help Book:
1. **Flashing Governing Criteria**:
   - Flashing occurs strictly when the operating vessel pressure corresponds to a saturation/boiling temperature lower than the incoming liquid temperature ($T_{\text{flash}} < T_{\text{in}}$).
   - Inflowing pressure must exceed vessel flash pressure ($P_{\text{in}} > P_{\text{flash}}$).
   - No external heating is supplied ($Q = 0$).
2. **Three Mutually Exclusive Pressure/Thermal Modes (Magenta Border)**:
   Exactly one of the following three options must be selected:
   - **Mode A: Vapor Out Pressure ($P_{\text{vap}}$, $kPa$) / Saturation Temp ($T_{\text{sat}}$, $°C$)**: Direct vessel operating pressure.
   - **Mode B: Pressure Feedback**: Operating pressure inherited dynamically from downstream receiver or heat exchanger. If vented to atmosphere, defaults to model atmospheric pressure ($101.325\text{ kPa}$).
   - **Mode C: Output Flow Temperature ($T_{\text{out}}$, $°C$)**: Target temperature of the flashed liquor leaving the vessel.
3. **Boiling Point Elevation (BPE)**:
   - For pure condensate, $T_{\text{flash}} = T_{\text{sat}}(P_{\text{vap}})$.
   - For sugar solutions/liquor, dissolved dry substance elevates the boiling point ($T_{\text{liq}} = T_{\text{sat}}(P_{\text{vap}}) + \text{BPE}$).
4. **Entrainment Sugar Loss (PPM)**:
   - Droplets carried over with flash vapor are modeled via parts-per-million ($mg/kg$) of condensable vapor.
   - Droplets carry the identical DS% and purity as the liquid leaving the tank, correctly accounting for non-sucrose carryover.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Ports 0–8 In**| **Hot Inflow Streams** | IN | `liquid` / `material` | Hot Condensate/Liquor| High-pressure hot liquid streams | Upstream supply |
| **Port 0 Out** | **Flashed Liquid Out** | OUT | `liquid` / `material` | Cooled Liquid | Concentrated liquor or subcooled condensate | Equal to inlet mass minus vapor |
| **Port 1 Out** | **Flash Vapor Out** | OUT | `vapor` | Low-Pressure Vapor | Saturated water vapor carrying entrained PPM | Flashed consequence |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `FLS-01` | Up to 11 chars | Plant equipment asset tag |
| `flashMode` | `enum` | — | `VAPOR_PRESSURE` | `VAPOR_PRESSURE`, `PRESSURE_FEEDBACK`, `OUTPUT_TEMP` | Magenta mutual exclusion selector |
| `vaporPressureKPa`| `float` | `kPa` | 70.0 | 5.0 – 500.0 | Active when `flashMode == VAPOR_PRESSURE` |
| `vaporSatTempC` | `float` | `°C` | 89.96 | 32.0 – 152.0 | Coupled with `vaporPressureKPa` via CoolProp |
| `outputTemperatureC`| `float` | `°C` | 90.0 | 32.0 – 152.0 | Active when `flashMode == OUTPUT_TEMP`. Must be $< T_{\text{in}}$. |
| `entrainmentLossPPM`| `float`| `mg/kg`| 50.0 | 0.0 – 500.0 | Entrained sugar droplets per unit vapor mass |
| `bpeFactor` | `float` | — | 1.0 | 0.0 – 2.0 | BPE multiplier for sugar liquor solutions |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Liquid Inlet Mixing
$$\dot{m}_{\text{in}} = \sum_{j=0}^8 \dot{m}_j, \quad h_{\text{in}} = \frac{\sum_{j=0}^8 \dot{m}_j h_j}{\dot{m}_{\text{in}}}, \quad \vec{z}_{\text{in}} = \frac{\sum_{j=0}^8 \dot{m}_j \vec{z}_j}{\dot{m}_{\text{in}}}$$

### 4.2 Flash Evaporation Balance
At flash pressure $P_{\text{flash}}$:
$$T_{\text{sat}} = T_{\text{sat}}(P_{\text{flash}})$$
$$\text{BPE} = \text{bpeFactor} \times \Delta T_{\text{BPE}}(w_{\text{DS,out}}, P_{\text{flash}})$$
$$T_{\text{liq,out}} = T_{\text{sat}} + \text{BPE}$$
$$h_{\text{liq,out}} = h_{\text{liq}}(T_{\text{liq,out}}, \vec{z}_{\text{out}}), \quad h_{\text{vap,out}} = h_{\text{steam}}(P_{\text{flash}}, T_{\text{sat}})$$

From adiabatic conservation of energy:
$$\dot{m}_{\text{in}} h_{\text{in}} = \dot{m}_{\text{liq,out}} h_{\text{liq,out}} + \dot{m}_{\text{vap,out}} h_{\text{vap,out}}$$
$$\dot{m}_{\text{vap,out}} = \dot{m}_{\text{in}} \times \frac{h_{\text{in}} - h_{\text{liq,out}}}{h_{\text{vap,out}} - h_{\text{liq,out}}}$$
$$\dot{m}_{\text{liq,out}} = \dot{m}_{\text{in}} - \dot{m}_{\text{vap,out}}$$

### 4.3 Entrainment Droplet Loss
$$\dot{m}_{\text{droplets}} = \dot{m}_{\text{vap,out}} \times \left(\frac{\text{entrainmentLossPPM}}{10^6}\right)$$
Carries identical Dry Substance ($w_{\text{DS}}$) and Purity ($P$) as the discharge liquid.

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{in}} - (\dot{m}_{\text{liq,out}} + \dot{m}_{\text{vap,out}})|}{\dot{m}_{\text{in}}} = 0.0$$
2. **Flash Direction Validity**:
   $$T_{\text{in}} > T_{\text{liq,out}}, \quad P_{\text{in}} > P_{\text{flash}}$$
3. **Dry Substance Conservation**:
   $$|\dot{m}_{\text{DS,in}} - (\dot{m}_{\text{DS,liq}} + \dot{m}_{\text{DS,droplets}})| = 0.0$$
