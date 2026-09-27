# STENCIL SPECIFICATION: Pressure Reducer (PRV) Station
## Module Identifier: `STENCIL-PRV-01`
### Station Type Code: `12` | SUGARS Classification: Pressure Reducer & Pipeline Throttling

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Pressure_Reducer/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Isenthalpic Joule-Thomson Expansion ($h = \text{const}$), Adiabatic Flashing, Feedback Pressure Drop Propagation  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Pressure Reducer station models throttling valves, orifices, pressure regulators, and pipeline frictional pressure drops. It handles steam lines, vapor conduits, or liquid streams.

### Key Operating Principles from Sugar's Help Book:
1. **Pressure Specification Modes (Magenta Border)**:
   Exactly one of the following two options can be selected:
   - **Mode 1: Pressure Out ($P_{\text{out}}$, $kPa$)**: Constant discharge pressure held during simulation ($P_{\text{out}} < P_{\text{in}}$).
   - **Mode 2: Pressure Drop ($\Delta P$, $kPa$)**: Fixed differential drop ($P_{\text{out}} = P_{\text{in}} - \Delta P$).
2. **Thermodynamic Throttling & Isenthalpic Expansion**:
   - The throttling process is strictly adiabatic and isenthalpic ($h_{\text{out}} = h_{\text{in}}$).
   - For superheated steam, throttling produces an increase in superheat (temperature drops slightly, but saturation temperature drops faster).
   - For wet steam or subcooled liquid flashing, the vapor fraction changes instantaneously according to two-phase equilibrium at $P_{\text{out}}$.
3. **Pressure Feedback Propagation**:
   - If `Pressure Drop` mode is used, pressure feedback can pass upstream through the reducer: the upstream required pressure is automatically calculated as downstream pressure plus $\Delta P$.
4. **Sucrose Invariance**:
   - Dissolved sucrose and crystal components are strictly preserved without crystallization changes.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **High-Pressure Feed In** | IN | `any` | Steam / Vapor / Liquid | Process steam, vapor line, or process fluid | Known upstream stream |
| **Port 1 In** | **Desuperheating Water In**| IN | `liquid` | Condensate / Pure Water | Optional desuperheating spray | Calculated required flow |
| **Port 0 Out**| **Reduced-Pressure Out** | OUT | `any` | Throttled Stream | Reduced pressure stream | Consequence of throttling |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `PRV-01` | Up to 11 chars | Plant equipment asset tag |
| `pressureMode` | `enum` | — | `PRESSURE_OUT`| `PRESSURE_OUT`, `PRESSURE_DROP` | Magenta mutual exclusion selector |
| `pressureOutKPa` | `float` | `kPa` | 150.0 | 5.0 – 4000.0 | Active when `pressureMode == PRESSURE_OUT`. Must satisfy $P_{\text{out}} < P_{\text{in}}$. |
| `pressureDropKPa`| `float` | `kPa` | 20.0 | 0.5 – 2000.0 | Active when `pressureMode == PRESSURE_DROP`. |
| `enableDesuperheating`| `boolean`| — | `false` | `true`, `false` | Enables quench spray water calculation via Port 1 |
| `targetSuperheatK`| `float` | `K` | 5.0 | 0.0 – 50.0 | Target superheat margin above saturation at $P_{\text{out}}$ |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Pressure Determination
- **If `pressureMode == PRESSURE_OUT`**:
  $$P_{\text{out}} = \text{pressureOutKPa}$$
- **If `pressureMode == PRESSURE_DROP`**:
  $$P_{\text{out}} = P_{\text{in}} - \text{pressureDropKPa}$$

### 4.2 Isenthalpic Throttling (Without Spray Water)
$$\dot{m}_{\text{out}} = \dot{m}_{\text{in}}$$
$$h_{\text{out}} = h_{\text{in}}$$
$$T_{\text{out}} = T(P_{\text{out}}, h_{\text{out}})$$

If fluid is water/steam mixture:
$$x_{\text{out}} = \frac{h_{\text{out}} - h_f(P_{\text{out}})}{h_{fg}(P_{\text{out}})}$$

### 4.3 Desuperheating Water Quench Balance (When Port 1 is Active)
If target discharge temperature $T_{\text{target}} = T_{\text{sat}}(P_{\text{out}}) + \text{targetSuperheatK}$ is specified:
$$h_{\text{target}} = h(P_{\text{out}}, T_{\text{target}})$$
$$\dot{m}_{\text{spray}} = \dot{m}_{\text{in}} \times \frac{h_{\text{in}} - h_{\text{target}}}{h_{\text{target}} - h_{\text{spray}}}$$
$$\dot{m}_{\text{out}} = \dot{m}_{\text{in}} + \dot{m}_{\text{spray}}$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|(\dot{m}_{\text{in}} + \dot{m}_{\text{spray}}) - \dot{m}_{\text{out}}|}{\dot{m}_{\text{in}} + \dot{m}_{\text{spray}}} = 0.0$$
2. **Pressure Reduction Validity**:
   $$P_{\text{out}} < P_{\text{in}}$$
3. **Isenthalpic Conservation (Without Spray)**:
   $$|h_{\text{out}} - h_{\text{in}}| = 0.0 \text{ kJ/kg}$$
4. **Second Law Verification**:
   $$s_{\text{out}} \ge s_{\text{in}}$$
