# STENCIL SPECIFICATION: Vapor Compressor (MVR) Station
## Module Identifier: `STENCIL-CMP-01`
### Station Type Code: `9` | SUGARS Classification: Mechanical Vapor Compressor (MVR)

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Compressor/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), CoolProp Real Gas Formulation / ASME Steam Tables, Isentropic Compression, Superheat Prevention of Condensation  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Vapor Compressor station models Mechanical Vapor Recompression (MVR). It boosts low-pressure process vapor (typically from the last evaporator effect, flash tank, or pan) to an elevated pressure and temperature suitable for reuse as heating steam in preceding effects or calandrias, dramatically reducing primary boiler steam demand.

### Key Operating Principles from Sugar's Help Book:
1. **Pressure Specification Modes (Maroon Border)**:
   - **Mode A: Explicit Discharge Pressure ($P_{\text{out}}$, $kPa$)**: The compressor holds a constant discharge pressure throughout simulation iterations (e.g., $320\text{ kPa}$).
   - **Mode B: Pressure Feedback**: Discharge pressure is dynamically inherited from downstream receivers or connected calandrias. If discharged out of model, defaults to $101.325\text{ kPa}$.
2. **Discharge Temperature & Superheat**:
   - The discharge temperature ($T_{\text{out}}$, $°C$) must be specified or calculated via isentropic efficiency.
   - **Strict Non-Condensation Rule**: Sugar's Help Book mandates that $T_{\text{out}} \ge T_{\text{sat}}(P_{\text{out}})$. Condensation inside the compressor is strictly prohibited; the discharge must be saturated or superheated vapor.
3. **Power Consumption & Mechanical Work**:
   - Power required is computed from thermodynamic enthalpy rise across the vapor phase and compressor mechanical/electrical efficiency.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Suction Vapor In** | IN | `vapor` | Low-Pressure Vapor | Saturated or superheated water vapor | Flow dictated by upstream station |
| **Port 0 Out**| **Compressed Vapor Out** | OUT | `vapor` | Recompressed Vapor | Superheated or saturated steam | Discharge flow equals suction flow |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `CMP-01` | Up to 11 chars | Plant equipment asset tag |
| `pressureMode` | `enum` | — | `SPECIFIED` | `SPECIFIED`, `FEEDBACK` | Discharge pressure determination mode |
| `dischargePressureKPa`| `float` | `kPa` | 200.0 | 10.0 – 2500.0 | Active when `pressureMode == SPECIFIED`. Must satisfy $P_{\text{out}} > P_{\text{in}}$. |
| `dischargeTemperatureC`| `float` | `°C` | 135.0 | 40.0 – 350.0 | Vapor discharge temperature. Must satisfy $T_{\text{out}} \ge T_{\text{sat}}(P_{\text{out}})$. |
| `isentropicEfficiency` | `float` | `%` | 75.0 | 50.0 – 95.0 | Isentropic compression efficiency $\eta_s$. |
| `mechanicalEfficiency` | `float` | `%` | 95.0 | 80.0 – 99.5 | Mechanical shaft / drive transmission efficiency $\eta_m$. |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Mass Conservation
$$\dot{m}_{\text{out}} = \dot{m}_{\text{in}}$$
$$\dot{m}_{\text{vap,out}} = \dot{m}_{\text{vap,in}}$$

### 4.2 Isentropic & Actual Enthalpy Calculation
From suction state $(P_{\text{in}}, T_{\text{in}}, h_{\text{in}}, s_{\text{in}})$:
$$s_{\text{isen,out}} = s_{\text{in}}$$
$$h_{\text{isen,out}} = h_{\text{steam}}(P_{\text{out}}, s_{\text{isen,out}})$$
$$\Delta h_{\text{isen}} = h_{\text{isen,out}} - h_{\text{in}}$$

The actual enthalpy rise is given by:
$$\Delta h_{\text{actual}} = \frac{\Delta h_{\text{isen}}}{\eta_s / 100.0}$$
$$h_{\text{out}} = h_{\text{in}} + \Delta h_{\text{actual}}$$

Discharge temperature is then determined from the equation of state:
$$T_{\text{out}} = T(P_{\text{out}}, h_{\text{out}})$$

Verification of non-condensation:
$$T_{\text{sat,out}} = T_{\text{sat}}(P_{\text{out}})$$
$$\text{Superheat } \Delta T_{\text{sh}} = T_{\text{out}} - T_{\text{sat,out}} \ge 0.0\text{ K}$$

### 4.3 Compressor Power Duty
$$\text{Internal Gas Power } \dot{W}_{\text{gas}} = \dot{m}_{\text{in}} \times \Delta h_{\text{actual}} \times \left(\frac{1\text{ h}}{3600\text{ s}}\right) \quad [\text{kW}]$$
$$\text{Shaft Power Required } \dot{W}_{\text{shaft}} = \frac{\dot{W}_{\text{gas}}}{\eta_m / 100.0} \quad [\text{kW}]$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}|}{\dot{m}_{\text{in}}} = 0.0$$
2. **Pressure Boost Validity**:
   $$\Delta P = P_{\text{out}} - P_{\text{in}} > 0.0\text{ kPa}$$
3. **Phase Purity (No Droplets)**:
   $$\text{Vapor Quality } x_{\text{out}} = 1.0$$
4. **Second Law Thermodynamic Closure**:
   $$s_{\text{out}} \ge s_{\text{in}}$$
