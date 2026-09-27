# STENCIL SPECIFICATION: Surface Heat Exchanger Station
## Module Identifier: `STENCIL-HEX-01`
### Station Type Code: `12` | SUGARS Classification: Heat Exchanger

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Heat_Exchanger/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8), LMTD / $\epsilon$-NTU Formulations, CoolProp IAPWS-95  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Surface Heat Exchanger station transfers thermal energy across an impervious heat transfer surface (shell & tube or plate heat exchanger) between a process juice flow (Port 0) and a heating/cooling utility flow (Port 1). No physical mixing occurs between process juice and utility stream.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Process Stream In** | IN | `material` | Juice / Syrup / Water | Liquid stream being heated/cooled | Normally determined by process upstream |
| **Port 0 Out**| **Process Stream Out**| OUT | `material` | Heated Juice / Syrup | Same mass and dry substance as Port 0 In | Outlet process flow |
| **Port 1 In** | **Utility Stream In** | IN | `thermal`/`material` | Steam / Vapour / Liquid | Motive steam, bleed vapour, or hot water | **Conditionally Required [R]** when `port1InputFlowRequired` is checked |
| **Port 1 Out**| **Utility Stream Out**| OUT | `condensate`/`material` | Condensate / Cooled Liquid | Saturated condensate or cooled liquid | Utility discharge |

---

## 3. Engineering Parameter Schema & Mutually Exclusive Control Modes

### 3.1 Port 0 Temperature Specification Modes (Magenta Borders)
Exactly one of the following three options can be active:
1. **Option A: Out Temperature**:
   - `tempOut` ($°C$): Explicit desired exit temperature of the process liquid (Port 0).
2. **Option B: Temperature Rise**:
   - `tempRise` ($K$): Explicit temperature rise ($\Delta T = T_{0,out} - T_{0,in}$).
3. **Option C: Approach**:
   - `approachK` ($K$): Temperature approach between utility discharge and process discharge ($T_{1,out} - T_{0,out}$).

### 3.2 Port 1 (Utility Flow) Controls
- `port1InputFlowRequired` (`boolean`):
  - When **Checked [TRUE]**: Sugars calculates the exact mass flow of steam, vapour, or hot water required to achieve the specified Port 0 thermal state.
  - When **Unchecked [FALSE]**: The utility flow rate is known and fixed, and Sugars calculates the resulting outlet temperatures.
- `port1TempOut` ($°C$):
  - Outlet temperature of the utility flow (primarily for liquid-liquid heat recovery).

### 3.3 Thermal Rating & Sizing Modes (Magenta Borders)
When calculating output temperatures from known flows:
1. **Option 1: Effectiveness (%)**:
   - `effectivenessPct` (%): Ratio of actual heat transfer to maximum thermodynamically possible heat transfer ($Q / Q_{max}$).
   - Typical values: 30% for shell & tube heaters; 60%–85% for plate heat exchangers.
2. **Option 2: Heat Transfer Coefficient & Heating Surface**:
   - `heatTransferCoefficient` ($W/m^2\cdot K$): Overall heat transfer coefficient ($U$).
   - `heatingSurfaceArea` ($m^2$): Installed thermal barrier area ($A$).
   - Governing Equation: $Q = U \cdot A \cdot \text{LMTD}$.

### 3.4 Additional Heat Exchanger Properties
- `condensateDropK` ($K$): Temperature drop of condensate below utility saturation temperature (subcooling).
- `heatLossPct` (%): Percentage of transferred heat lost to ambient atmosphere (default: 0.5%–1.0%).
- `flowDirection` (`COUNTER_CURRENT` vs `CO_CURRENT`): Flow arrangement affecting LMTD and effectiveness.
- `heatExchangerType` (`CONDENSING` vs `NON_CONDENSING`):
  - `CONDENSING`: Utility stream condenses completely into liquid condensate.
  - `NON_CONDENSING`: Sensible heat exchange between two non-condensing liquids or gases.

---

## 4. Governing Thermodynamic Equations

### 4.1 Process Fluid Duty
$$Q_{process} = \dot{M}_0 \cdot C_{p,0} \cdot (T_{0,out} - T_{0,in})$$

### 4.2 Gross Utility Duty & Loss
$$Q_{gross} = \frac{Q_{process}}{1.0 - \text{heatLossPct} / 100.0}$$

### 4.3 Utility Mass Flow (when Input Flow Required = TRUE)
- If **Condensing Steam/Vapour**:
  $$\dot{M}_{1,req} = \frac{Q_{gross}}{h_{1,in} - h_{condensate}(T_{sat,1} - \text{condensateDropK})}$$
- If **Sensible Liquid**:
  $$\dot{M}_{1,req} = \frac{Q_{gross}}{C_{p,1} \cdot (T_{1,in} - T_{1,out})}$$

### 4.4 Log Mean Temperature Difference (LMTD)
For counter-current flow:
$$\Delta T_1 = T_{1,in} - T_{0,out}, \quad \Delta T_2 = T_{1,out} - T_{0,in}$$
$$\text{LMTD} = \frac{\Delta T_1 - \Delta T_2}{\ln(\Delta T_1 / \Delta T_2)}$$

---

## 5. Independent Physical Balance Cross-Checks

1. **Total Process Mass Balance**: $\dot{M}_{0,in} = \dot{M}_{0,out} \pm 0.001\%$
2. **Total Utility Mass Balance**: $\dot{M}_{1,in} = \dot{M}_{1,out} \pm 0.001\%$
3. **Dry Substance Conservation**: $DS_{0,in} = DS_{0,out} \pm 0.0001\%$
4. **Thermal Enthalpy Closure**: $|Q_{utility,given} \cdot (1 - \text{Loss}) - Q_{process,absorbed}| \le 0.05\%$
