# STENCIL SPECIFICATION: Evaporator Station (Multiple-Effect Body)
## Module Identifier: `STENCIL-EVAP-01`
### Station Type Code: `9` | SUGARS Classification: Evaporator

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Evaporator/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §B6), Bubnik-Kadlec (1995) / Peacock (1995) BPE Models, CoolProp IAPWS-95 Steam Formulations  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Evaporator station concentrates clarified or thin juice into concentrated syrup (typically 65.0–70.0 °Brix) by vaporizing water using thermal energy transferred from condensing steam or lower-effect process vapour across heating surfaces.

In multi-effect evaporation trains:
- Motive steam flows into the calandria of the **1st effect**.
- Vapour generated from boiling juice in effect $i$ serves as the heating medium for the calandria of effect $i+1$.
- Bleed vapours are extracted from intermediate effects to supply vacuum pans, raw juice heaters, and deaerators.
- Boiling point elevation (BPE) occurs in each body due to dissolved sucrose and non-sucrose solids, reducing the effective driving temperature difference $\Delta T_{eff}$.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0** | **Process Juice Feed** | IN | `material` | Juice / Syrup | Liquid stream with $\text{DS} > 0$ | Never required; driven by upstream extraction/clarification |
| **Port 1** | **Calandria Motive Steam / Vapour** | IN | `thermal` | Steam / Vapour | Saturated or superheated steam / vapour | **Conditionally Required [R]** when `totalSolidsPct` is specified on 1st effect |
| **Port 2** | **Condensate Return / Flash** (Opt) | IN | `condensate` | Condensate | Upstream effect calandria condensate | Optional flash steam contribution |
| **Port 3** | **Evaporated Process Vapour** | OUT | `thermal` | Process Vapour | Saturated vapour + entrained droplets | **Never Required [R]**; determined strictly by evaporation mass balance |
| **Port 4** | **Calandria Condensate** | OUT | `condensate` | Condensate | Saturated or subcooled liquid water | **Never Required [R]**; strictly equals condensed calandria steam |
| **Port 5** | **Concentrated Syrup / Outlet Juice**| OUT | `material` | Concentrated Juice| Concentrated sugar solution | Forwarded to next effect or syrup receiver |
| **Port 6** | **Process Vapour Bleed** (Opt) | OUT | `thermal` | Bleed Vapour | Extracted vapour to heaters/pans | Specified as rate or downstream required flow |

---

## 3. Engineering Parameter Schema & Mutually Exclusive Control Modes

### 3.1 Mutually Exclusive Operating Modes (Magenta Border Enforcements)
Under Sugar's Help Book rules, **exactly one** of the following four operating specifications may be active. Selecting one disables and dims the remaining three:

1. **Option A: Heat Transfer Coefficient & Heating Surface**:
   - `heatTransferCoefficient` ($W/m^2\cdot K$): Thermal conductance across heating tubes.
   - `heatingSurfaceArea` ($m^2$): Installed heat transfer area.
   - *Governing Equation*: $\dot{Q} = U \cdot A \cdot (T_{steam,sat} - T_{juice,boil})$.
2. **Option B: Vapour Out Pressure & Saturation Temperature**:
   - `vaporPressure` ($kPa\text{ abs}$) OR `vaporSaturationTemp` ($°C$): Directly fixes the boiling vapor equilibrium.
   - If pressure is entered, saturation temperature is computed via $T_{sat}(P)$; if temperature is entered, pressure is computed via $P_{sat}(T)$.
3. **Option C: Juice Flow Out Temperature**:
   - `flowOutTemperature` ($°C$): Directly fixes the outlet juice boiling temperature.
4. **Option D: Pressure Feedback**:
   - `pressureFeedbackEnabled` (Boolean): Vapour space pressure is dynamically determined by downstream condenser vacuum or barometric back-pressure.

### 3.2 Global & Station Parameters

| Parameter Name | Data Type | Units | Default | Physical Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique station identifier across flowsheet |
| `equipmentTag` | `string` | — | `EVAP-01` | Up to 11 chars | Plant equipment asset identifier |
| `effectNumber` | `integer` | — | 1 | 1 – 10 | Sequential position in multiple-effect train. Motive steam must feed effect 1. |
| `totalSolidsPct` | `float` | `%` | 65.0 | 10.0 – 85.0 | Target dry substance of outlet syrup. Causes motive steam to be Required [R]. |
| `heatLossPct` | `float` | `%` | 1.5 | 0.0 – 10.0 | Loss of heat to ambient (% of gross calandria duty). |
| `condensateDropK` | `float` | `K` | 0.0 | 0.0 – 20.0 | Subcooling of condensate below calandria steam saturation temperature. |
| `entrainmentLossPpm`| `float` | `mg/kg` | 0.0 | 0.0 – 2000.0 | Sugar entrained in vapor. Carries droplets at outlet syrup DS% and purity. |
| `bpeFactor` | `float` | — | 1.0 | 0.5 – 2.0 | Multiplier on calculated boiling point elevation. |
| `colorRise` | `float` | `%` or `CU`| 0.0 | 0.0 – 50.0 | Thermal degradation color increase across effect. |
| `vaporBleedFlow` | `float` | `kg/h` | 0.0 | $\ge 0.0$ | Vapour extracted to external juice heaters or vacuum pans. |

---

## 4. Governing Thermodynamic Equations

### 4.1 Dry Substance Conservation
$$\dot{M}_{juice,in} \cdot DS_{juice,in} = \dot{M}_{syrup,out} \cdot DS_{syrup,out} + \dot{M}_{entrained} \cdot DS_{syrup,out}$$

When entrainment is negligible:
$$\dot{M}_{syrup,out} = \dot{M}_{juice,in} \cdot \frac{DS_{juice,in}}{DS_{syrup,out}}$$

### 4.2 Evaporation Rate
$$\dot{M}_{evap} = \dot{M}_{juice,in} - \dot{M}_{syrup,out}$$

### 4.3 Boiling Point Elevation (BPE)
$$T_{juice,boil} = T_{sat}(P_{vap}) + \text{bpeFactor} \cdot \Delta T_{BPE}(DS_{syrup}, \text{Purity}, P_{vap})$$
Where $\Delta T_{BPE}$ is calculated using the authoritative Bubnik-Kadlec (1995) formulation.

### 4.4 Calandria Thermal Duty & Steam Consumption
$$Q_{absorbed} = \dot{M}_{evap} \cdot \Delta h_{vap}(T_{juice,boil}, P_{vap}) + \dot{M}_{juice,in} \cdot C_{p,juice} \cdot (T_{juice,boil} - T_{juice,in})$$
$$Q_{gross} = \frac{Q_{absorbed}}{1.0 - \text{heatLossPct} / 100.0}$$
$$\dot{M}_{steam} = \frac{Q_{gross}}{h_{steam,in} - h_{condensate}(T_{sat,steam} - \text{condensateDropK})}$$

### 4.5 Steam Economy
$$\text{Economy} = \frac{\dot{M}_{evap}}{\dot{M}_{steam}} \quad [kg\text{ evaporated} / kg\text{ steam}]$$

---

## 5. Independent Physical Balance Cross-Checks

1. **Total Mass Balance Closure**:
   $$\epsilon_{mass} = \frac{|\dot{M}_{in} - \dot{M}_{out}|}{\dot{M}_{in}} \times 100\% \le 0.05\%$$
2. **Dry Substance Conservation Closure**:
   $$\epsilon_{DS} = \frac{|\dot{M}_{DS,in} - \dot{M}_{DS,out}|}{\dot{M}_{DS,in}} \times 100\% \le 0.01\%$$
3. **Calandria Energy Balance Closure**:
   $$\epsilon_{heat} = \frac{|Q_{steam,released} \cdot (1 - \text{Loss}) - Q_{absorbed}|}{Q_{steam,released}} \times 100\% \le 0.1\%$$
