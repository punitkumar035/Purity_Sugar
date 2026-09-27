# STENCIL SPECIFICATION: Contact & Surface Condenser Stations
## Module Identifier: `STENCIL-CND-01`
### Station Type Codes: `21` (Contact Condenser) & `22` (Surface Condenser) | SUGARS Classification: Vacuum Condensers

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Contact_Condenser/`, `Surface_Condenser/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Vacuum Phase Equilibrium, Direct Contact Condensation, Indirect LMTD / NTU Surface Heat Transfer  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

Condensers create and maintain the process vacuum on vacuum pans, multi-effect evaporator last effects, and turbine exhausts. Sugar's Help Book defines two distinct engineering classes:

### 1.1 Contact Condenser (Barometric Condenser)
Cold injection water mixes directly with incoming process vapor inside spray or tray baffles, collapsing the vapor into liquid.
- **Tail Water Mixture**: Condensed vapor and cooling water combine and exit together via the barometric leg to the hotwell.
- **Magenta Cooling Water Controls (5 Options)**:
  1. *Minimum Water to Condense All Vapor*: Calculates absolute minimum cooling water needed to achieve complete condensation.
  2. *Temperature Out ($T_{\text{out}}$, $°C$)*: Maintains hotwell discharge at a set target temperature.
  3. *Approach Temperature ($\Delta T_{\text{app}}$, $K$)*: Controls cooling water so $T_{\text{out}} = T_{\text{sat}}(P_{\text{vac}}) - \Delta T_{\text{app}}$ (typical approach $3 \text{ to } 5\text{ K}$).
  4. *Explicit Quantity ($\dot{m}_{\text{cw}}$, $kg/h$)*: Known cooling water flow rate.
  5. *Ratio to Vapor ($R_{\text{cw}}$, $kg\text{ water}/kg\text{ vapor}$)*: Typical ratio $20 \text{ to } 35\text{ kg/kg}$.

### 1.2 Surface Condenser
Process vapor condenses on the exterior of tube bundles or plate packs while cooling water circulates through closed channels without mixing.
- **Condensate Segregation**: Pure distilled condensate is discharged separately via Port 0 Out, while warmed cooling water exits via Port 1 Out.
- **Governing Thermal Modes (Maroon Border)**:
  - *Option 1*: Heat Transfer Coefficient ($U$, $W/m^2\cdot K$) + Surface Area ($A$, $m^2$).
  - *Option 2*: Effectiveness ($\epsilon$, $\%$ via NTU method).
- **Subcooling & Flow Arrangement**:
  - Condensate subcooling drop ($K$).
  - Countercurrent vs. Parallel (co-current) flow orientation.
  - Heat loss to ambient ($\%$).

---

## 2. Port Architecture & Topological Connectivity

### Contact Condenser (Direct Contact)
| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Vapor In** | IN | `vapor` | Vacuum Vapor | Saturated/superheated process vapor | Upstream supply |
| **Port 1 In** | **Cooling Water In** | IN | `liquid` | Cold Water | Injection cooling water | Known supply or Required Flow |
| **Port 0 Out**| **Tail Water Out** | OUT | `liquid` | Combined Water | Mixture of water + condensed vapor | Sum of Port 0 + Port 1 |

### Surface Condenser (Indirect Heat Transfer)
| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Vapor In** | IN | `vapor` | Vacuum Vapor | Saturated vapor to be condensed | Upstream supply |
| **Port 1 In** | **Cooling Water In** | IN | `liquid` | Cooling Utility | Cold cooling water | Known supply or Required Flow |
| **Port 0 Out**| **Pure Condensate Out**| OUT | `liquid` | Distillate | Pure condensed vapor | Equal to Port 0 In mass |
| **Port 1 Out**| **Warm Cooling Water Out**| OUT | `liquid`| Spent Water | Warmed cooling water | Equal to Port 1 In mass |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `CND-01` | Up to 11 chars | Plant equipment asset tag |
| `condenserType` | `enum` | — | `CONTACT` | `CONTACT`, `SURFACE` | Governs port routing and mixing behavior |
| `internalPressureKPa`| `float`| `kPa` | 16.0 | 5.0 – 101.3 | Vacuum pressure held for upstream pressure feedback |
| `waterControlMode`| `enum` | — | `APPROACH` | `MIN_WATER`, `TEMP_OUT`, `APPROACH`, `QUANTITY`, `RATIO` | Magenta selection for Contact Condenser |
| `targetTempOutC` | `float` | `°C` | 45.0 | 20.0 – 80.0 | Active when `waterControlMode == TEMP_OUT` |
| `approachTempK` | `float` | `K` | 4.0 | 1.0 – 20.0 | Active when `waterControlMode == APPROACH` |
| `fixedWaterRateTPH`| `float`| `TPH` | 100.0 | 1.0 – 5000.0 | Active when `waterControlMode == QUANTITY` |
| `waterToVaporRatio`| `float`| `kg/kg`| 25.0 | 5.0 – 80.0 | Active when `waterControlMode == RATIO` |
| `surfaceHTC` | `float` | `W/(m²·K)`| 1800.0 | 200.0 – 4000.0| Active for Surface Condenser with Area |
| `surfaceAreaM2` | `float` | `m²` | 250.0 | 10.0 – 5000.0 | Heating surface area for Surface Condenser |
| `effectivenessPct`| `float`| `%` | 75.0 | 20.0 – 95.0 | Maroon option for Surface Condenser |
| `condensateDropK`| `float` | `K` | 2.0 | 0.0 – 15.0 | Subcooling of condensate below saturation |
| `flowDirection` | `enum` | — | `COUNTERCURRENT`| `COUNTERCURRENT`, `PARALLEL` | Flow configuration across bundle |
| `heatLossPct` | `float` | `%` | 0.5 | 0.0 – 10.0 | Ambient radiation loss |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Contact Condenser Balances
Saturation temperature at internal vacuum pressure:
$$T_{\text{sat}} = T_{\text{sat}}(P_{\text{vac}})$$

- **If `waterControlMode == APPROACH`**:
  $$T_{\text{tail,target}} = T_{\text{sat}} - \Delta T_{\text{app}}$$
  $$\dot{m}_{\text{cw,req}} = \dot{m}_{\text{vap}} \times \frac{h_{\text{vap}}(P_{\text{vac}}, T_{\text{vap}}) - h_f(T_{\text{tail,target}})}{h_f(T_{\text{tail,target}}) - h_{\text{cw,in}}}$$
- **If `waterControlMode == MIN_WATER`**:
  $$T_{\text{tail}} = T_{\text{sat}} - 0.5\text{ K}$$
  $$\dot{m}_{\text{cw,req}} = \dot{m}_{\text{vap}} \times \frac{h_{\text{vap}} - h_f(T_{\text{sat}})}{h_f(T_{\text{sat}}) - h_{\text{cw,in}}}$$
- **Tail Water Mass**:
  $$\dot{m}_{\text{tail,out}} = \dot{m}_{\text{vap}} + \dot{m}_{\text{cw}}$$

### 4.2 Surface Condenser Balances
Condensate rate is exactly equal to condensable vapor rate:
$$\dot{m}_{\text{condensate,out}} = \dot{m}_{\text{vap,in}}$$
$$T_{\text{condensate}} = T_{\text{sat}}(P_{\text{vac}}) - \text{condensateDropK}$$
$$\dot{Q}_{\text{duty}} = \dot{m}_{\text{vap}} [h_{\text{vap}} - h_f(T_{\text{condensate}})]$$

Cooling water heat pickup:
$$\dot{Q}_{\text{water}} = \dot{Q}_{\text{duty}} \times \left(1.0 - \frac{\text{heatLossPct}}{100.0}\right)$$
$$\dot{m}_{\text{cw}} C_{p, w} (T_{\text{cw,out}} - T_{\text{cw,in}}) = \dot{Q}_{\text{water}}$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\sum \dot{m}_{\text{in}} - \sum \dot{m}_{\text{out}}|}{\sum \dot{m}_{\text{in}}} = 0.0$$
2. **Vacuum Thermodynamic Consistency**:
   $$T_{\text{tail}} \le T_{\text{sat}}(P_{\text{vac}})$$
3. **Approach Temperature Non-Negativity**:
   $$\Delta T_{\text{app}} = T_{\text{sat}}(P_{\text{vac}}) - T_{\text{tail}} \ge 0.0\text{ K}$$
