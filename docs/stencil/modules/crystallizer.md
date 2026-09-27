# STENCIL SPECIFICATION: Massecuite Crystallizer Station
## Module Identifier: `STENCIL-CRYS-01`
### Station Type Code: `6` | SUGARS Classification: Cooling Crystallizer

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Crystallizer/`, `Theory/Sucrose_Supersaturation/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Vavrinecz Sucrose Solubility, Schneider/Wagnerowski Saturation Coefficients, Exothermic Crystal Growth ($\Delta h = +54.9\text{ kJ/kg}$)  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Crystallizer station models continuous and batch cooling crystallizers (e.g., A, B, and C massecuite crystallizer batteries). Hot massecuite discharged from vacuum pans ($65 \text{ to } 80\text{ °C}$) is slowly cooled down to $40 \text{ to } 50\text{ °C}$. The temperature drop lowers the equilibrium solubility of sucrose, creating a driving force for dissolved sucrose to desupersaturate and deposit onto existing sugar crystal surfaces, maximizing sugar extraction prior to centrifugal separation.

### Key Operating Principles from Sugar's Help Book:
1. **Governing Control Parameters**:
   - **Target Supersaturation ($SS$)**: Dimensionless ratio of actual dissolved sucrose to saturation solubility at exit temperature and non-sucrose/water ratio. Typical target range: $1.05 \text{ to } 1.20$.
   - **Output Temperature ($T_{\text{out}}$, $°C$)**: Discharge temperature of massecuite. Cooling is strictly required ($T_{\text{out}} < T_{\text{in}}$).
   - **Color Rise**: Color formation across residence time (specified in % or absolute ICUMSA Color Units).
2. **Mother Liquor Interactive Calculator**:
   - Sugars provides a specialized calculator dialog allowing the user to solve the required supersaturation from measured mother liquor %DS and Purity, using adjustable saturation coefficients ($a, b, c$).
3. **Exothermic Heat of Crystallization**:
   - Sucrose crystal growth releases latent heat of crystallization ($\Delta h_{\text{cryst}} = +54.9\text{ kJ/kg}$). This internal heat release counteracts sensible cooling and must be absorbed by cooling water/air.
4. **Metastable Zone & False Grain Prevention**:
   - The cooling trajectory must maintain supersaturation below the critical nucleation threshold ($SS < 1.25$) to prevent spontaneous nucleation of fine unrecoverable crystals.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Hot Massecuite In** | IN | `slurry` | Massecuite | Hot pan discharge slurry containing crystals | Upstream supply |
| **Port 0 Out**| **Cooled Massecuite Out**| OUT | `slurry` | Conditioned Massecuite| Cooled slurry with increased crystal content | Consequence of cooling & growth |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `CRYS-01` | Up to 11 chars | Plant equipment asset tag |
| `supersaturation` | `float` | — | 1.15 | 1.00 – 1.35 | Exit mother liquor supersaturation ratio |
| `temperatureOutC` | `float` | `°C` | 45.0 | 30.0 – 75.0 | Massecuite exit temperature ($T_{\text{out}} < T_{\text{in}}$) |
| `colorRise` | `float` | `%` / `CU`| 2.0 | 0.0 – 500.0 | Color formation during crystallizer cooling |
| `coeffA` | `float` | — | 0.08222 | 0.0 – 1.0 | Vavrinecz / Wagnerowski solubility coefficient |
| `coeffB` | `float` | — | 0.0016169| 0.0 – 0.01 | Vavrinecz / Wagnerowski solubility coefficient |
| `coeffC` | `float` | — | -1.558e-6| -0.001 – 0.0 | Vavrinecz / Wagnerowski solubility coefficient |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Sucrose Solubility & Saturation Coefficient
Pure water sucrose solubility at $T_{\text{out}}$ (Vavrinecz equation):
$$S_0(T) = 64.447 + 0.08222 T + 0.0016169 T^2 - 1.558 \times 10^{-6} T^3 - 4.63 \times 10^{-8} T^4 \quad [\%]$$
$$H_0(T) = \frac{S_0(T)}{100.0 - S_0(T)} \quad \left[\frac{\text{g sucrose}}{\text{g water}}\right]$$

Influence of non-sucrose impurities:
$$\text{NSW} = \frac{C_{\text{NS}}}{C_{\text{water}}}$$
$$\text{SatCoeff} = 1.0 - a \cdot \text{NSW} + b \cdot \text{NSW}^2$$
$$H_{\text{sat}} = H_0(T_{\text{out}}) \times \text{SatCoeff}$$

### 4.2 Mother Liquor Desupersaturation & Crystal Growth
At target supersaturation $SS$:
$$H_{\text{actual}} = SS \times H_{\text{sat}} \quad \left[\frac{\text{g dissolved sucrose}}{\text{g water}}\right]$$
$$M_{\text{sucrose,dissolved,out}} = M_{\text{water,in}} \times H_{\text{actual}}$$

Sucrose crystal mass growth:
$$\Delta \dot{m}_{\text{cryst}} = \dot{m}_{\text{sucrose,dissolved,in}} - M_{\text{sucrose,dissolved,out}}$$
$$\dot{m}_{\text{cryst,out}} = \dot{m}_{\text{cryst,in}} + \Delta \dot{m}_{\text{cryst}}$$

Total massecuite mass is strictly conserved:
$$\dot{m}_{\text{mc,out}} = \dot{m}_{\text{mc,in}}$$

### 4.3 Thermal Duty
Sensible cooling duty plus exothermic crystallization release:
$$\dot{Q}_{\text{net}} = \dot{m}_{\text{mc}} C_p (T_{\text{in}} - T_{\text{out}}) + \Delta \dot{m}_{\text{cryst}} \times (+54.9\text{ kJ/kg})$$

---

## 5. Independent Cross-Checks

1. **Mass Balance Closure**:
   $$\epsilon_{\text{mass}} = \frac{|\dot{m}_{\text{mc,in}} - \dot{m}_{\text{mc,out}}|}{\dot{m}_{\text{mc,in}}} = 0.0$$
2. **Sucrose Total Conservation**:
   $$(\dot{m}_{\text{cryst,in}} + \dot{m}_{\text{dissolved,in}}) - (\dot{m}_{\text{cryst,out}} + \dot{m}_{\text{dissolved,out}}) = 0.0$$
3. **Cooling Temperature Verification**:
   $$T_{\text{out}} < T_{\text{in}}$$
4. **Positive Crystal Growth**:
   $$\Delta \dot{m}_{\text{cryst}} \ge 0.0\text{ kg/h}$$
