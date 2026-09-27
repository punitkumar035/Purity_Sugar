# STENCIL SPECIFICATION: Sugar Melter Station
## Module Identifier: `STENCIL-MELT-01`
### Station Type Code: `16` | SUGARS Classification: Melter

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Melter/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Endothermic Heat of Sucrose Dissolution ($-54.9\text{ kJ/kg}$), Atmospheric Pressure Discharge  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Melter station dissolves sucrose crystals (from raw sugar affination, low-grade magma, seed sugar, or recovery massecuites) into an aqueous solvent (water, sweetwater, or thin juice) to produce clear, unsaturated melt liquor (typically 65.0–70.0 °Brix).

Governing Process Principles:
1. **Complete Crystal Dissolution**: All solid sucrose crystals are melted into solution ($\text{Crystal Content}_{out} = 0.0\%$).
2. **Dissolution Energetics**: Sucrose crystal dissolution is an endothermic physical reaction absorbing approximately $54.9\text{ kJ/kg}$ of dissolved crystalline sucrose, which causes liquid cooling unless heat is supplied.
3. **Atmospheric Operating Pressure**: Regardless of inlet pressures or steam pressure, the outlet melt liquor is strictly discharged at atmospheric pressure ($101.325\text{ kPa}$ or site barometric pressure).
4. **Heating Technology Options**:
   - **Injection Heating**: Motive steam or process vapour condenses directly inside the liquor, diluting the dry substance and increasing liquid mass.
   - **Coil Heating**: Steam condenses inside internal closed heating tubes/coils, discharging as clean, separate calandria condensate without diluting the melt liquor.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Ports 0–8** | **Sugar Feeds** (1 to 9 inputs) | IN | `material` | Sugar / Magma / Remelt | Crystalline sucrose streams | Normally known process streams |
| **Port 9** | **Diluent Solvent Feed** | IN | `material` | Water / Sweetwater / Juice | Aqueous diluent stream | **Conditionally Required [R]** when `holdTdmPct` is specified ($> 0$) |
| **Port 10** | **Heating Medium (Steam/Vapour)**| IN | `thermal` | Steam / Vapour | Heating steam / vapour | **Conditionally Required [R]** when `temperatureOut` is specified |
| **Port 11** | **Melt Liquor Outlet** | OUT | `material` | Melt Liquor | Completely dissolved sucrose syrup | Standard atmospheric process outlet |
| **Port 12** | **Coil Condensate** (Coil mode only)| OUT | `condensate` | Condensate | Saturated condensate | Active only when Heating Type = Coil |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Physical Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station identifier |
| `equipmentTag` | `string` | — | `MELT-01` | Up to 11 chars | Equipment asset tag |
| `holdTdmPct` | `float` | `%` | 65.0 | 0.0 – 85.0 | Total dry matter target. If $> 0$, Port 9 solvent is adjusted automatically as Required [R]. If 0, solvent flow is fixed. |
| `temperatureOut`| `float` | `°C` | 75.0 | 20.0 – 100.0 | Desired melt liquor discharge temperature. Causes Port 10 heating flow to be Required [R]. |
| `heatingType` | `enum` | — | `INJECTION` | `INJECTION` / `COIL` | `INJECTION` condenses steam into liquor; `COIL` produces separate clean condensate. |
| `heatLossPct` | `float` | `%` | 1.0 | 0.0 – 10.0 | Loss of heat to ambient (% of transferred thermal duty). |
| `colorRise` | `float` | `%` or `CU`| 0.0 | 0.0 – 50.0 | Color increase due to thermal exposure in melter vessel. |
| `requiredFlowInletId`| `string` | — | `AUTO` | Port ID | When melter outlet flow is required by a downstream unit, selects which inlet flow is varied to balance output. |

---

## 4. Governing Thermodynamic Equations

### 4.1 Dry Substance & Solvent Balance
Let $\dot{M}_{sugar} = \sum_{i=0}^8 \dot{M}_{i}$ and $\dot{M}_{DS,sugar} = \sum_{i=0}^8 \dot{M}_{i} \cdot DS_i$.
For diluent at Port 9 with dry substance $DS_9$:
$$\dot{M}_{DS,total} = \dot{M}_{DS,sugar} + \dot{M}_{9} \cdot DS_9$$

To achieve target $DS_{target} = \text{holdTdmPct} / 100.0$:
$$\dot{M}_{9,required} = \frac{\dot{M}_{DS,sugar} - DS_{target} \cdot \dot{M}_{sugar}}{DS_{target} - DS_9}$$

### 4.2 Complete Crystal Dissolution
$$\text{Crystal Content}_{out} = 0.0\%$$
$$\dot{M}_{dissolved,out} = \dot{M}_{dissolved,in} + \dot{M}_{crystals,in}$$

### 4.3 Thermal Duty & Energy Balance
The net heat absorbed includes sensible heating of process liquid and solvent plus the endothermic heat of crystal dissolution:
$$Q_{dissolution} = \dot{M}_{crystals,in} \cdot |\Delta h_{dissolution}| \quad \text{where } |\Delta h_{dissolution}| = 54.9\text{ kJ/kg}$$
$$Q_{sensible} = \dot{M}_{liquor} \cdot C_{p,liquor} \cdot (T_{out} - T_{mix})$$
$$Q_{net} = Q_{sensible} + Q_{dissolution}$$
$$Q_{gross} = \frac{Q_{net}}{1.0 - \text{heatLossPct} / 100.0}$$

**Heating Steam Requirement**:
- Under **Injection Heating**:
  $$\dot{M}_{steam} = \frac{Q_{gross}}{h_{steam,in} - h_{water}(T_{out}, P_{atm})}$$
  Dilution effect: $\dot{M}_{out} = \dot{M}_{sugar} + \dot{M}_{9} + \dot{M}_{steam}$.
- Under **Coil Heating**:
  $$\dot{M}_{steam} = \frac{Q_{gross}}{h_{steam,in} - h_{condensate}(T_{sat})}$$
  Condensate discharged separately: $\dot{M}_{out} = \dot{M}_{sugar} + \dot{M}_{9}$, and $\dot{M}_{cond} = \dot{M}_{steam}$.

---

## 5. Independent Physical Balance Cross-Checks

1. **Total Mass Balance Closure**:
   $$\epsilon_{mass} = \frac{|\sum \dot{M}_{in} - \sum \dot{M}_{out}|}{\sum \dot{M}_{in}} \times 100\% \le 0.01\%$$
2. **Dry Substance Conservation Closure**:
   $$\epsilon_{DS} = \frac{|\sum \dot{M}_{DS,in} - \sum \dot{M}_{DS,out}|}{\sum \dot{M}_{DS,in}} \times 100\% \le 0.01\%$$
3. **Crystal Extinction Verification**:
   $$\text{Crystals}_{out} \equiv 0.000\text{ kg/h} \quad (\text{Zero tolerance})$$
4. **Thermal Enthalpy Closure**:
   $$\epsilon_{enthalpy} = \frac{|\sum (\dot{M}_{in} h_{in}) + Q_{dissolution} - \sum (\dot{M}_{out} h_{out}) - Q_{loss}|}{\sum (\dot{M}_{in} h_{in})} \times 100\% \le 0.1\%$$
