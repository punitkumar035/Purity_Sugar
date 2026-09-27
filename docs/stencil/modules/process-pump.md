# STENCIL SPECIFICATION: Process Pump Station
## Module Identifier: `STENCIL-PMP-01`
### Station Type Code: `11` | SUGARS Classification: Centrifugal & Positive Displacement Pump

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Pump/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Hydrodynamic Pumping Work, Bubble Collapse / Vapor Condensation Under Compression  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Process Pump station models centrifugal, progressive cavity, and positive displacement pumps across the sugar factory (e.g., mixed juice pumps, imbibition pumps, limed juice booster pumps, evaporator transfer pumps, condensate return pumps, and massecuite/magma pumps).

### Key Operating Principles from Sugar's Help Book:
1. **Discharge Pressure Control Modes (Magenta Border)**:
   Exactly one of the following two options can be selected:
   - **Mode 1: Pressure Out ($P_{\text{out}}$, $kPa$)**: Direct discharge pressure held during simulation ($P_{\text{out}} > P_{\text{in}}$).
   - **Mode 2: Pressure Rise ($\Delta P$, $kPa$)**: Differential pressure boost ($P_{\text{out}} = P_{\text{in}} + \Delta P$).
2. **Flash Prevention & Vapor Bubble Collapse**:
   - Pumping increases stream pressure above saturation pressure, preventing flashing inside downstream heaters and piping.
   - Any entrained vapor in the liquid stream undergoes complete or partial condensation due to the pressure rise.
3. **Hydraulic Work & Motor Sizing**:
   - Power required is computed from volumetric flow rate, differential head ($\Delta P$), slurry density ($\rho$), and hydraulic/motor efficiencies.
   - Minor hydraulic friction dissipation is added to the fluid enthalpy, producing a small temperature rise ($\approx 0.05 \text{ to } 0.3\text{ K}$).

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Suction Feed In** | IN | `liquid` / `slurry` | Process Liquid | Juice, syrup, liquor, magma, or condensate | Known upstream stream |
| **Port 0 Out**| **Discharge Flow Out** | OUT | `liquid` / `slurry` | Pressurized Liquid | Higher pressure liquid or slurry | Equal mass flow rate |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `PMP-01` | Up to 11 chars | Plant equipment asset tag |
| `pressureMode` | `enum` | — | `PRESSURE_OUT`| `PRESSURE_OUT`, `PRESSURE_RISE` | Magenta mutual exclusion selector |
| `dischargePressureKPa`| `float` | `kPa` | 350.0 | 50.0 – 5000.0 | Active when `pressureMode == PRESSURE_OUT`. Must satisfy $P_{\text{out}} > P_{\text{in}}$. |
| `pressureRiseKPa` | `float` | `kPa` | 250.0 | 10.0 – 5000.0 | Active when `pressureMode == PRESSURE_RISE`. |
| `hydraulicEfficiency`| `float` | `%` | 72.0 | 30.0 – 90.0 | Pump hydraulic/impeller efficiency $\eta_{\text{hyd}}$. |
| `motorEfficiency` | `float` | `%` | 92.0 | 70.0 – 98.0 | Electric drive motor efficiency $\eta_{\text{motor}}$. |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Pressure Determination
- **If `pressureMode == PRESSURE_OUT`**:
  $$P_{\text{out}} = \text{dischargePressureKPa}$$
  $$\Delta P = P_{\text{out}} - P_{\text{in}}$$
- **If `pressureMode == PRESSURE_RISE`**:
  $$\Delta P = \text{pressureRiseKPa}$$
  $$P_{\text{out}} = P_{\text{in}} + \Delta P$$

### 4.2 Mass Conservation
$$\dot{m}_{\text{out}} = \dot{m}_{\text{in}}$$
$$\dot{m}_{i,\text{out}} = \dot{m}_{i,\text{in}} \quad \forall i \in \{0, \dots, 14\}$$

### 4.3 Hydrodynamic Power & Motor Rating
Using mixture density $\rho_{\text{mix}}$ ($kg/m^3$):
$$\dot{V} = \frac{\dot{m}_{\text{in}}}{\rho_{\text{mix}}} \times \left(\frac{1}{3600}\right) \quad [m^3/s]$$
$$\text{Hydraulic Power } \dot{W}_{\text{hyd}} = \dot{V} \times (\Delta P \times 1000) \times 10^{-3} = \frac{\dot{m}_{\text{in}} \times \Delta P}{3600 \times \rho_{\text{mix}}} \quad [\text{kW}]$$
$$\text{Shaft Brake Power } \dot{W}_{\text{brake}} = \frac{\dot{W}_{\text{hyd}}}{\eta_{\text{hyd}} / 100.0} \quad [\text{kW}]$$
$$\text{Electrical Motor Power } \dot{W}_{\text{elec}} = \frac{\dot{W}_{\text{brake}}}{\eta_{\text{motor}} / 100.0} \quad [\text{kW}]$$

### 4.4 Fluid Temperature Rise
$$\Delta T_{\text{fluid}} = \frac{\Delta P}{\rho_{\text{mix}} C_p} \times \left(\frac{1.0}{\eta_{\text{hyd}} / 100.0} - 1.0\right) \quad [K]$$
$$T_{\text{out}} = T_{\text{in}} + \Delta T_{\text{fluid}}$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}|}{\dot{m}_{\text{in}}} = 0.0$$
2. **Pressure Boost Validity**:
   $$P_{\text{out}} > P_{\text{in}}$$
3. **Power Non-Negativity**:
   $$\dot{W}_{\text{elec}} \ge \dot{W}_{\text{brake}} \ge \dot{W}_{\text{hyd}} > 0.0$$
