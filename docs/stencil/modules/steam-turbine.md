# STENCIL SPECIFICATION: Steam Turbine & Turbo Alternator Stations
## Module Identifier: `STENCIL-TRB-01` / `STENCIL-GEN-01`
### Station Type Codes: `17` (Turbine) & `18` (Turbo Alternator) | SUGARS Classification: Cogeneration Steam Turbines

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Turbine/`, `Turbo_Alternator/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), CoolProp / ASME Formulation, Isentropic Expansion, Mechanical & Electrical Generator Losses, Reverse Power Demand Solving  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Steam Turbine and Turbo Alternator stations model mechanical prime movers (cane knife drives, shredders, mill tandem drives, boiler feed pump drives) and back-pressure / condensing cogeneration turbogenerators that expand high-pressure boiler superheated steam ($1500 \text{ to } 10000\text{ kPa}$) to low-pressure exhaust steam ($120 \text{ to } 250\text{ kPa}$) or vacuum condenser pressure ($10 \text{ to } 25\text{ kPa}$).

### Key Operating Principles from Sugar's Help Book:
1. **Thermal Mode (Maroon Mutually Exclusive Border)**:
   Exactly one of the following two options is specified:
   - **Option 1: Exhaust Temperature ($T_{\text{out}}$, $°C$)**: Direct measurement of discharge steam temperature; solver calculates isentropic efficiency.
   - **Option 2: Isentropic Efficiency ($\eta_s$, $\%$ internal turbine efficiency)**: Solver calculates enthalpy drop and exhaust temperature.
2. **Pressure Mode (Magenta Mutually Exclusive Border)**:
   Exactly one of the following three options is specified:
   - **Option A: Discharge Pressure ($P_{\text{out}}$, $kPa$)**: Constant backpressure held during simulation.
   - **Option B: Pressure Drop ($\Delta P$, $kPa$)**: Fixed expansion pressure drop across stages ($P_{\text{out}} = P_{\text{in}} - \Delta P$).
   - **Option C: Pressure Feedback**: Exhaust pressure dynamically inherited from downstream exhaust steam header or receiver.
3. **Power Demand vs. Known Throughput Dynamics**:
   - **Target Power Specified ($P_{\text{target}} > 0.0\text{ kW}$)**: Throttle steam into the turbine becomes an automatic **Required Flow [R]**; solver computes exact steam flow needed to generate requested mechanical/electrical power.
   - **Target Power = 0.0 kW**: Steam throughput is determined by upstream boiler generation or downstream exhaust demand; solver calculates resulting generated shaft power and electrical megawatts.
4. **Efficiencies**:
   - `Mechanical Efficiency (%)`: Accounts for bearing friction and reduction gear losses (typically $97\% \text{ to } 99\%$).
   - `Generator Efficiency (%)`: (Turbo Alternator only) Accounts for copper, iron, and windage losses in the alternator ($95\% \text{ to } 98\%$).

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Throttle Steam In** | IN | `vapor` | High-Pressure Steam | Superheated steam from boiler or header | Known supply or Required Flow |
| **Port 0 Out**| **Exhaust Steam Out** | OUT | `vapor` | Low-Pressure Steam | Saturated or low-superheat exhaust steam | Equal mass flow rate |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `TRB-01` | Up to 11 chars | Plant equipment asset tag |
| `stationClass` | `enum` | — | `TURBO_ALTERNATOR`| `MECHANICAL_DRIVE`, `TURBO_ALTERNATOR` | Mechanical shaft work vs electrical power |
| `thermalMode` | `enum` | — | `ISENTROPIC_EFF` | `TEMPERATURE_OUT`, `ISENTROPIC_EFF` | Maroon thermal selection |
| `exhaustTemperatureC`| `float`| `°C` | 135.0 | 40.0 – 400.0 | Active when `thermalMode == TEMPERATURE_OUT` |
| `isentropicEfficiency`| `float`| `%` | 72.0 | 40.0 – 92.0 | Active when `thermalMode == ISENTROPIC_EFF` |
| `pressureMode` | `enum` | — | `DISCHARGE_PRESS` | `DISCHARGE_PRESS`, `PRESSURE_DROP`, `FEEDBACK` | Magenta pressure selection |
| `dischargePressureKPa`| `float`| `kPa` | 200.0 | 5.0 – 4000.0 | Active when `pressureMode == DISCHARGE_PRESS` |
| `pressureDropKPa` | `float` | `kPa` | 2300.0 | 10.0 – 9000.0 | Active when `pressureMode == PRESSURE_DROP` |
| `targetPowerKW` | `float` | `kW` | 0.0 | 0.0 – 100,000.0| $0.0 \implies$ calculate power; $>0.0 \implies$ steam is Required Flow |
| `mechanicalEfficiency`| `float`| `%` | 98.5 | 85.0 – 99.5 | Mechanical shaft / gearbox efficiency |
| `generatorEfficiency` | `float`| `%` | 96.5 | 85.0 – 99.0 | Active for Turbo Alternator |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Exhaust Pressure Determination
$$P_{\text{out}} = \begin{cases} 
\text{dischargePressureKPa} & \text{if `DISCHARGE_PRESS`} \\ 
P_{\text{in}} - \text{pressureDropKPa} & \text{if `PRESSURE_DROP`} \\ 
P_{\text{header,feedback}} & \text{if `FEEDBACK`} 
\end{cases}$$

### 4.2 Isentropic Expansion
From throttle state $(P_{\text{in}}, T_{\text{in}}, h_{\text{in}}, s_{\text{in}})$:
$$s_{\text{isen,out}} = s_{\text{in}}$$
$$h_{\text{isen,out}} = h_{\text{steam}}(P_{\text{out}}, s_{\text{isen,out}})$$
$$\Delta h_{\text{isen}} = h_{\text{in}} - h_{\text{isen,out}}$$

### 4.3 Actual Expansion Enthalpy & Exhaust State
- **If `thermalMode == ISENTROPIC_EFF`**:
  $$\Delta h_{\text{actual}} = \Delta h_{\text{isen}} \times \left(\frac{\eta_s}{100.0}\right)$$
  $$h_{\text{out}} = h_{\text{in}} - \Delta h_{\text{actual}}$$
  $$T_{\text{out}} = T(P_{\text{out}}, h_{\text{out}})$$
- **If `thermalMode == TEMPERATURE_OUT`**:
  $$h_{\text{out}} = h_{\text{steam}}(P_{\text{out}}, T_{\text{out}})$$
  $$\Delta h_{\text{actual}} = h_{\text{in}} - h_{\text{out}}$$
  $$\eta_s = \frac{\Delta h_{\text{actual}}}{\Delta h_{\text{isen}}} \times 100.0$$

### 4.4 Power Generation & Steam Consumption
- **Shaft Mechanical Power**:
  $$\dot{W}_{\text{shaft}} = \dot{m}_{\text{steam}} \times \Delta h_{\text{actual}} \times \left(\frac{\eta_m}{100.0}\right) \times \left(\frac{1}{3600}\right) \quad [\text{kW}]$$
- **Electrical Power Generation**:
  $$\dot{W}_{\text{elec}} = \dot{W}_{\text{shaft}} \times \left(\frac{\eta_g}{100.0}\right) \quad [\text{kW}]$$
- **Specific Steam Consumption (SSC)**:
  $$\text{SSC} = \frac{\dot{m}_{\text{steam}}}{\dot{W}_{\text{elec}} \text{ (or } \dot{W}_{\text{shaft}})} \quad \left[\frac{\text{kg}}{\text{kWh}}\right]$$

### 4.5 Inverse Required Steam Solving (When Target Power > 0.0)
$$\dot{m}_{\text{steam,req}} = \frac{3600 \times \text{targetPowerKW}}{\Delta h_{\text{actual}} \times (\eta_m / 100.0) \times (\eta_g / 100.0)} \quad \left[\frac{\text{kg}}{\text{h}}\right]$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}|}{\dot{m}_{\text{in}}} = 0.0$$
2. **Expansion Direction Validity**:
   $$P_{\text{out}} < P_{\text{in}}, \quad h_{\text{out}} < h_{\text{in}}$$
3. **Efficiency Bounds**:
   $$0.0 < \eta_s \le 100.0\%$$
