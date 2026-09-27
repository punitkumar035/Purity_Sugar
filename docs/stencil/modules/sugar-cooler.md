# STENCIL SPECIFICATION: Sugar Cooler Station
## Module Identifier: `STENCIL-CLR-01`
### Station Type Code: `7` | SUGARS Classification: Cooler & Refrigeration Unit

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Cooler/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Saturated/Superheated Vapor Condensation, Non-Crystallizing Supersaturation Rise  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Cooler station is used to remove thermal energy from a flow stream, condense water vapor, or model ambient heat losses from pipelines, vessels, cooling towers, and refrigeration units.

### Key Operating Principles from Sugar's Help Book:
1. **Four Mutually Exclusive Performance Modes (Magenta Border)**:
   Exactly one of the following four governing modes must be selected:
   - **Mode 1: Temperature Drop ($\Delta T$, $K$)**: Specifies an explicit cooling temperature difference.
   - **Mode 2: Temperature Out ($T_{\text{out}}$, $°C$)**: Cools the stream to a precise target temperature ($T_{\text{out}} < T_{\text{in}}$).
   - **Mode 3: Heat Loss Percent ($Q_{\text{loss}}\%$, $\%$ of input enthalpy)**: Calculates temperature reduction or condensation based on a fractional enthalpy loss.
   - **Mode 4: Enthalpy Loss ($\Delta h$, $kJ/kg$)**: Direct reduction of specific enthalpy from inlet stream ($h_{\text{out}} = h_{\text{in}} - \Delta h$).
2. **Phase Change & Condensation**:
   - Liquid-vapor phase equilibrium is always evaluated. If saturated or superheated vapor enters, removal of latent heat causes condensation into liquid water/condensate at saturation temperature.
   - If heat loss is less than total latent heat, the discharge stream remains at saturation temperature and contains a two-phase mixture of vapor and liquid.
3. **Strict Non-Crystallization Rule (Sucrose Preservation)**:
   - **Sucrose crystal growth is strictly disallowed** in the Cooler station.
   - The crystal mass in the outlet stream exactly equals crystal mass in the inlet stream ($\dot{m}_{\text{cryst,out}} = \dot{m}_{\text{cryst,in}}$).
   - When cooling lowers sucrose solubility below dissolved concentration, the dissolved mother liquor becomes **supersaturated** ($SS > 1.0$) rather than forming crystals.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Hot Feed In** | IN | `any` | Any Process Stream | Material, liquor, vapor, or condensate | Known upstream flow |
| **Port 0 Out**| **Cooled Discharge Out** | OUT | `any` | Process Stream | Cooled material, condensate, or two-phase mixture | Calculated consequence |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `CLR-01` | Up to 11 chars | Plant equipment asset tag |
| `coolingMode` | `enum` | — | `TEMP_DROP`| `TEMP_DROP`, `TEMP_OUT`, `HEAT_LOSS_PCT`, `HEAT_LOSS_KJ` | Governs the Magenta mutually exclusive control mode |
| `temperatureDropK`| `float` | `K` / `°C`| 5.0 | 0.0 – 60.0 | Active only when `coolingMode == TEMP_DROP` |
| `temperatureOutC` | `float` | `°C` | 35.0 | 0.0 – 120.0 | Active only when `coolingMode == TEMP_OUT`. Must satisfy $T_{\text{out}} \le T_{\text{in}}$. |
| `heatLossPct` | `float` | `%` | 5.0 | 0.0 – 100.0 | Active only when `coolingMode == HEAT_LOSS_PCT`. % loss of inlet stream enthalpy. |
| `heatLossKJPerKg` | `float` | `kJ/kg`| 20.0 | 0.0 – 2500.0 | Active only when `coolingMode == HEAT_LOSS_KJ`. Specific enthalpy loss. |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Mass Conservation
$$\dot{m}_{\text{out}} = \dot{m}_{\text{in}}$$
$$\dot{m}_{i,\text{out}} = \dot{m}_{i,\text{in}} \quad \forall i \in \{0, \dots, 14\}$$
$$\dot{m}_{\text{cryst,out}} = \dot{m}_{\text{cryst,in}}$$

### 4.2 Enthalpy & Output State Determination
Depending on the active `coolingMode`:

1. **If `coolingMode == TEMP_DROP`**:
   $$T_{\text{out}} = T_{\text{in}} - \text{temperatureDropK}$$
2. **If `coolingMode == TEMP_OUT`**:
   $$T_{\text{out}} = \text{temperatureOutC}$$
3. **If `coolingMode == HEAT_LOSS_PCT`**:
   $$h_{\text{out}} = h_{\text{in}} \times \left(1.0 - \frac{\text{heatLossPct}}{100.0}\right)$$
   $$T_{\text{out}} = T(h_{\text{out}}, P_{\text{out}}, \vec{z})$$
4. **If `coolingMode == HEAT_LOSS_KJ`**:
   $$h_{\text{out}} = h_{\text{in}} - \text{heatLossKJPerKg}$$
   $$T_{\text{out}} = T(h_{\text{out}}, P_{\text{out}}, \vec{z})$$

### 4.3 Vapor Condensation Balance
If inlet contains vapor with latent heat $\Delta h_{\text{vap}}$:
$$\Delta \dot{H}_{\text{removed}} = \dot{m}_{\text{in}} (h_{\text{in}} - h_{\text{out}})$$
- If $\Delta \dot{H}_{\text{removed}} \ge \dot{m}_{\text{vap,in}} \times \Delta h_{\text{vap}}$: Complete condensation occurs.
- If $\Delta \dot{H}_{\text{removed}} < \dot{m}_{\text{vap,in}} \times \Delta h_{\text{vap}}$: Partial condensation occurs at $T_{\text{sat}}(P)$; remaining vapor fraction is discharged.

### 4.4 Supersaturation Assessment
Using the Vavrinecz sucrose solubility equation:
$$S_0(T_{\text{out}}) = 64.447 + 0.08222 T_{\text{out}} + 0.0016169 T_{\text{out}}^2 - 1.558 \times 10^{-6} T_{\text{out}}^3 - 4.63 \times 10^{-8} T_{\text{out}}^4$$
$$\text{Sucrose Solubility in Water} = \frac{S_0(T_{\text{out}})}{100.0 - S_0(T_{\text{out}})} \times \text{SatCoeff}(\text{NS}/W)$$
$$\text{Supersaturation } (SS) = \frac{C_{\text{sucrose,dissolved}} / C_{\text{water}}}{\text{Sucrose Solubility}}$$

---

## 5. Independent Cross-Checks

1. **Total Mass Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{in}} - \dot{m}_{\text{out}}|}{\dot{m}_{\text{in}}} = 0.0$$
2. **Component Mass Closure**:
   $$\epsilon_{\text{comp}, i} = |\dot{m}_{i,\text{in}} - \dot{m}_{i,\text{out}}| = 0.0 \quad \forall i$$
3. **Sucrose Crystal Conservation**:
   $$|\dot{m}_{\text{cryst,in}} - \dot{m}_{\text{cryst,out}}| = 0.0$$
4. **Energy Balance**:
   $$\dot{Q}_{\text{duty}} = \dot{m}_{\text{in}} (h_{\text{in}} - h_{\text{out}}) \ge 0.0$$
