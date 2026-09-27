# STENCIL SPECIFICATION: Thermocompressor Station
## Module Identifier: `STENCIL-TCM-01`
### Station Type Code: `10` | SUGARS Classification: Steam Jet Thermocompressor (Ejector)

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Thermocompressor/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Truffault Formula for Steam Ejectors with 5% Nozzle Wear Allowance, Momentum & Enthalpy Balances  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Thermocompressor (steam jet ejector) uses high-pressure motive steam (typically live boiler steam or exhaust steam at $300 \text{ to } 2000\text{ kPa}$) expanding through a supersonic converging-diverging nozzle to entrain and recompress low-pressure suction vapor (typically from the last evaporator effect or vacuum pan at $15 \text{ to } 100\text{ kPa}$), discharging an intermediate-pressure mixture ($70 \text{ to } 250\text{ kPa}$) suitable for evaporator heating or pan boiling.

### Key Operating Principles from Sugar's Help Book:
1. **Pressure Specification Modes (Maroon Border)**:
   - **Mode A: Explicit Pressure Out ($P_{\text{out}}$, $kPa$)**: Constant discharge pressure held during simulation.
   - **Mode B: Pressure Feedback**: Pressure inherited from downstream destination vessel or receiver.
2. **Three Mutually Exclusive Performance Modes (Magenta Border)**:
   Exactly one of the following three options must be selected:
   - **Option 1: Efficiency (%) via Truffault Formula**:
     Calculates the entrained suction vapor rate using the empirical Truffault relationship, which is a function of:
     - Output mixed pressure ($P_{\text{out}}$) and saturation temperature ($T_{\text{out}}$)
     - Suction vapor temperature ($T_{\text{suct}}$) and pressure ($P_{\text{suct}}$)
     - Motive steam pressure ($P_{\text{mot}}$)
     - A built-in **5% allowance for nozzle wear/degradation**.
   - **Option 2: Entrainment Ratio ($\mu = \dot{m}_{\text{suct}} / \dot{m}_{\text{mot}}$)**:
     Specified directly from equipment manufacturer performance curves or empirical test data.
   - **Option 3: Discharge Temperature ($T_{\text{out}}$, $°C$)**:
     Specified mixed discharge temperature. Heat balance directly determines the required entrainment ratio.
3. **Phase Changes**:
   Water/vapor phase changes (superheat dissipation or slight condensation) are fully modeled across the mixing chamber and diffuser.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Motive Steam In** | IN | `vapor` | High-Pressure Steam | Saturated or superheated high-pressure steam | Known supply or required flow |
| **Port 1 In** | **Suction Vapor In** | IN | `vapor` | Low-Pressure Vapor | Evaporator/pan low-pressure vapor | Entrained consequence |
| **Port 0 Out**| **Discharge Steam Out**| OUT | `vapor` | Recompressed Steam | Mixed intermediate-pressure steam | Sum of motive + suction |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `TCM-01` | Up to 11 chars | Plant equipment asset tag |
| `pressureMode` | `enum` | — | `SPECIFIED` | `SPECIFIED`, `FEEDBACK` | Maroon pressure control selector |
| `pressureOutKPa` | `float` | `kPa` | 145.0 | 20.0 – 1000.0 | Active when `pressureMode == SPECIFIED`. Must satisfy $P_{\text{suct}} < P_{\text{out}} < P_{\text{mot}}$. |
| `performanceMode`| `enum` | — | `EFFICIENCY`| `EFFICIENCY`, `ENTRAINMENT_RATIO`, `TEMPERATURE_OUT` | Magenta performance selector |
| `efficiencyPct` | `float` | `%` | 85.0 | 40.0 – 100.0 | Active when `performanceMode == EFFICIENCY`. Evaluated via Truffault equation. |
| `entrainmentRatio`| `float` | `kg/kg`| 0.45 | 0.05 – 3.00 | Ratio of suction vapor to motive steam ($\dot{m}_{\text{suct}} / \dot{m}_{\text{mot}}$). |
| `dischargeTemperatureC`| `float`| `°C` | 115.0 | 50.0 – 250.0 | Active when `performanceMode == TEMPERATURE_OUT`. |
| `nozzleWearFactor`| `float` | `%` | 5.0 | 0.0 – 20.0 | Default 5% nozzle wear degradation per Sugar's Help Book. |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Truffault Formulation for Steam Jet Ejectors
The theoretical entrainment capacity $\mu_{\text{theoretical}}$ is derived from the expansion and compression pressure ratios:
$$r_e = \frac{P_{\text{mot}}}{P_{\text{suct}}}, \quad r_c = \frac{P_{\text{out}}}{P_{\text{suct}}}$$

Accounting for the 5% nozzle wear allowance:
$$\mu_{\text{actual}} = \mu_{\text{theoretical}}(P_{\text{mot}}, P_{\text{suct}}, P_{\text{out}}, T_{\text{suct}}, T_{\text{out}}) \times \left(\frac{\text{efficiencyPct}}{100.0}\right) \times (1.0 - 0.05)$$

### 4.2 Mass Balance
$$\dot{m}_{\text{suct}} = \dot{m}_{\text{mot}} \times \mu$$
$$\dot{m}_{\text{out}} = \dot{m}_{\text{mot}} + \dot{m}_{\text{suct}} = \dot{m}_{\text{mot}} (1 + \mu)$$

### 4.3 Energy Balance
Assuming adiabatic mixing across the thermocompressor:
$$h_{\text{out}} = \frac{\dot{m}_{\text{mot}} h_{\text{mot}} + \dot{m}_{\text{suct}} h_{\text{suct}}}{\dot{m}_{\text{out}}}$$
$$T_{\text{out}} = T(P_{\text{out}}, h_{\text{out}})$$

If `performanceMode == TEMPERATURE_OUT`, $h_{\text{out}} = h(P_{\text{out}}, T_{\text{out}})$, and the required entrainment ratio is inverted:
$$\mu = \frac{h_{\text{mot}} - h_{\text{out}}}{h_{\text{out}} - h_{\text{suct}}}$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|(\dot{m}_{\text{mot}} + \dot{m}_{\text{suct}}) - \dot{m}_{\text{out}}|}{\dot{m}_{\text{mot}} + \dot{m}_{\text{suct}}} = 0.0$$
2. **Pressure Hierarchy Verification**:
   $$P_{\text{mot}} > P_{\text{out}} > P_{\text{suct}}$$
3. **First Law Adiabatic Closure**:
   $$|\dot{m}_{\text{mot}} h_{\text{mot}} + \dot{m}_{\text{suct}} h_{\text{suct}} - \dot{m}_{\text{out}} h_{\text{out}}| = 0.0$$
