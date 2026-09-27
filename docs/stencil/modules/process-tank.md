# STENCIL SPECIFICATION: Process Tank Station
## Module Identifier: `STENCIL-TNK-01`
### Station Type Code: `14` | SUGARS Classification: Storage, Mixing & Heated Process Tank

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Tank/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Multi-Inlet Mixing, Controlled Dilution (Port 9 TDM Hold), Thermal Balancing (Port 10 Steam), Injection vs Coil Heating  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Process Tank station models storage tanks, buffer vessels, reaction/holding tanks, and heated mixing vessels across the factory (e.g., mixed juice tanks, limed juice tanks, syrup buffer tanks, remelt tanks, and molasses storage tanks).

### Key Operating Principles from Sugar's Help Book:
1. **Accumulation & Depletion (Magenta Border)**:
   Exactly one of the following two options may be active:
   - **Flow to Storage ($\dot{V}_{\text{to}}$, $m^3/h$)**: Tank liquid level rises as fluid accumulates in storage; net outlet flow is reduced by this volumetric storage rate.
   - **Flow from Storage ($\dot{V}_{\text{from}}$, $m^3/h$)**: Tank liquid level falls as inventory is withdrawn to supplement inlet streams; net outlet flow is increased by this volumetric rate.
2. **Dedicated Control Port Architecture**:
   - **Ports 0–8**: General multi-component process inflows (blended uniformly).
   - **Port 9**: Solvent / Diluent inflow (side port). When `Hold TDM at (%)` $> 0.0\%$, the solver dynamically modulates Port 9 flow as a **Required Flow** to maintain the outlet stream at the exact specified dry substance.
   - **Port 10**: Heating steam inflow. When `Output Flow Temperature (°C)` is specified, Port 10 flow is dynamically modulated as a **Required Flow** to satisfy the thermal duty.
3. **Heating Configuration (Injection vs. Coil)**:
   - **Direct Steam Injection**: Steam mixes directly with process fluid, condensing, diluting Brix, and discharging via Port 0 Out.
   - **Internal Coil Heating**: Steam condenses inside closed internal coils; pure condensate is discharged via a dedicated condensate port (Port 1 Out) without process dilution.
4. **Color Formation & Heat Loss**:
   - Color rise specified as % increase or absolute Color Units (CU).
   - Heat loss expressed as % of heat transferred from utility steam to process liquid.
5. **Required Flow Selection Box**:
   - If downstream operations demand a specific required flow from the tank, a selection dialog enables the engineer to select which upstream inlet stream modulates to balance mass.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Ports 0–8 In**| **Process Inflows In** | IN | `any` | Process Fluids | Any liquid, slurry, or syrup streams | Upstream supply or selectable required flow |
| **Port 9 In** | **Diluent Solvent In** | IN | `liquid` | Water / Sweetwater | Side diluent port | Dynamically calculated required flow if TDM Hold active |
| **Port 10 In** | **Heating Medium In** | IN | `vapor` | Steam / Condensate | Heating utility | Dynamically calculated required flow if Target Temp active |
| **Port 0 Out** | **Process Stream Out** | OUT | `material` | Process Mixture | Combined process liquor | Primary outlet |
| **Port 1 Out** | **Condensate Out** | OUT | `liquid` | Hot Condensate | Active only when `heatingType == COIL` | Pure condensed heating medium |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `TNK-01` | Up to 11 chars | Plant equipment asset tag |
| `storageMode` | `enum` | — | `NONE` | `NONE`, `TO_STORAGE`, `FROM_STORAGE` | Magenta storage selection |
| `flowToStorageM3H`| `float` | `m³/h` | 0.0 | 0.0 – 500.0 | Active when `storageMode == TO_STORAGE` |
| `flowFromStorageM3H`| `float`| `m³/h` | 0.0 | 0.0 – 500.0 | Active when `storageMode == FROM_STORAGE` |
| `holdTdmPct` | `float` | `%` | 0.0 | 0.0 – 90.0 | Active if Port 9 connected. Modulates Port 9 diluent flow. |
| `outputTemperatureC`| `float`| `°C` | 0.0 | 0.0 – 110.0 | Active if Port 10 connected. Modulates Port 10 heating flow. |
| `heatingType` | `enum` | — | `INJECTION`| `INJECTION`, `COIL` | Governs heating medium phase path |
| `heatLossPct` | `float` | `%` | 1.5 | 0.0 – 25.0 | % loss of transferred thermal duty |
| `colorRise` | `float` | `%` / `CU`| 0.0 | 0.0 – 1000.0 | Thermal color formation across residence time |
| `requiredFlowInlet`| `integer`| — | 0 | 0 – 8 | Inlet port selected to balance downstream required demand |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Storage Correction
Using liquid mixture density $\rho_{\text{mix}}$ ($kg/m^3$):
$$\dot{m}_{\text{storage}} = \begin{cases} 
+\dot{V}_{\text{to}} \times \rho_{\text{mix}} & \text{if `TO_STORAGE`} \\ 
-\dot{V}_{\text{from}} \times \rho_{\text{mix}} & \text{if `FROM_STORAGE`} \\ 
0.0 & \text{if `NONE`} 
\end{cases}$$

### 4.2 Dilution Control (Port 9 TDM Balance)
When `holdTdmPct` ($w_{\text{target}} \in (0, 1)$) is specified:
$$\sum_{j=0}^{8} \dot{m}_{\text{DS}, j} + \dot{m}_{9} \times w_{\text{DS}, 9} = w_{\text{target}} \times \left(\sum_{j=0}^{8} \dot{m}_{j} + \dot{m}_{9} - \dot{m}_{\text{storage}}\right)$$
Solving for required Port 9 flow:
$$\dot{m}_{9} = \frac{w_{\text{target}} \left(\sum_{j=0}^8 \dot{m}_j - \dot{m}_{\text{storage}}\right) - \sum_{j=0}^8 \dot{m}_{\text{DS}, j}}{w_{\text{DS}, 9} - w_{\text{target}}}$$

### 4.3 Thermal Duty & Steam Demand (Port 10)
When `outputTemperatureC` ($T_{\text{target}}$) is specified:
$$\dot{Q}_{\text{net}} = \dot{m}_{\text{process,out}} h(T_{\text{target}}, \vec{z}) - \left(\sum_{j=0}^9 \dot{m}_j h_j - \dot{m}_{\text{storage}} h_{\text{storage}}\right)$$
$$\dot{Q}_{\text{gross}} = \frac{\dot{Q}_{\text{net}}}{1.0 - \text{heatLossPct}/100.0}$$
- **If `heatingType == INJECTION`**:
  $$\dot{m}_{10} = \frac{\dot{Q}_{\text{gross}}}{h_{10} - h(T_{\text{target}}, \vec{z})}$$
  $$\dot{m}_{\text{process,out}} = \sum_{j=0}^9 \dot{m}_j - \dot{m}_{\text{storage}} + \dot{m}_{10}$$
- **If `heatingType == COIL`**:
  $$\dot{m}_{10} = \frac{\dot{Q}_{\text{gross}}}{h_{10,\text{vap}} - h_{10,\text{cond}}}$$
  $$\dot{m}_{\text{condensate,out}} = \dot{m}_{10}$$
  $$\dot{m}_{\text{process,out}} = \sum_{j=0}^9 \dot{m}_j - \dot{m}_{\text{storage}}$$

---

## 5. Independent Cross-Checks

1. **Overall Mass Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\sum \dot{m}_{\text{in}} - (\dot{m}_{\text{out}} + \dot{m}_{\text{condensate}} + \dot{m}_{\text{storage}})|}{\sum \dot{m}_{\text{in}}} < 10^{-4}$$
2. **Dry Substance Closure**:
   $$\epsilon_{\text{DS}} = \frac{|\sum \dot{m}_{\text{DS,in}} - (\dot{m}_{\text{DS,out}} + \dot{m}_{\text{DS,storage}})|}{\sum \dot{m}_{\text{DS,in}}} < 10^{-5}$$
3. **Target Brix Accuracy**:
   $$|\text{TDM}_{\text{out}} - \text{holdTdmPct}| < 0.001\%$$
