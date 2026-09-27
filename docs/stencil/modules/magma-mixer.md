# STENCIL SPECIFICATION: Blender & Magma Mixer Station
## Module Identifier: `STENCIL-BLND-01`
### Station Type Code: `1` | SUGARS Classification: Blender, Mingler & Magma Mixer

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Blender/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Multi-Stream Mixing, Controlled Blending via Component Ratio, Target Brix, Target Purity, or Target Temperature  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Blender station models proportional mixing, chemical addition, minglers, and magma mixers across the sugar factory (e.g., lime milk addition to raw juice, B/C sugar minglers producing crystal magma, syrup blending, and molasses conditioning). 

Unlike a Melter, a Magma Mixer / Blender **does not dissolve crystals**; it incorporates liquid (syrup, liquor, or water) with crystalline sugar or primary process liquor to yield a pumpable mixture with a controlled property target.

### Key Operating Principles from Sugar's Help Book:
1. **Two Distinct Inlet Streams**:
   - **Port 0: Primary Inflow ($\dot{m}_{\text{prim}}$)**: The main process stream (e.g., raw sugar, raw juice, B-sugar crystals).
   - **Port 1: Blend Inflow ($\dot{m}_{\text{blend}}$)**: The modulating stream added to adjust properties (e.g., lime saccharate, affination syrup, water).
2. **Seven Mutually Exclusive Governing Control Modes (Magenta Border)**:
   Exactly one of the following control modes determines the blend flow rate $\dot{m}_{\text{blend}}$:
   - **Mode 1: Ratio to Component / Total**: Blend flow is a fixed ratio $R$ to total primary flow or a specific component (e.g., $CaO$, sucrose, dry solids).
   - **Mode 2: Explicit Blend Quantity ($\dot{m}_{\text{fixed}}$, $kg/h$)**: Fixed addition rate.
   - **Mode 3: Target Output Quantity ($\dot{m}_{\text{out}}$, $kg/h$)**: Blend flow modulates so total discharge hits target rate.
   - **Mode 4: Target Dry Substance ($DS_{\text{target}}$, $\%$)**: Blend flow modulates to achieve target Brix/DS.
   - **Mode 5: Target Purity ($P_{\text{target}}$, $\%$)**: Blend flow modulates to achieve target purity.
   - **Mode 6: Target Output Temperature ($T_{\text{target}}$, $°C$)**: Enthalpy balance modulates blend flow to achieve target temperature.
   - **Mode 7: Target Non-Sugar/Water Ratio ($NSW_{\text{target}}$)**: Modulates to maintain specific solubility ratio.
3. **Crystal Conservation**:
   - Sucrose crystal mass entering via Port 0 and Port 1 is conserved into the outlet stream ($\dot{m}_{\text{cryst,out}} = \dot{m}_{\text{cryst,prim}} + \dot{m}_{\text{cryst,blend}}$).

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Primary Flow In** | IN | `any` | Primary Feed | Main process material or sugar crystals | Upstream supply |
| **Port 1 In** | **Blend Flow In** | IN | `any` | Blending Medium | Diluent, syrup, reagent, or water | Modulated Required Flow |
| **Port 0 Out**| **Blended Mixture Out**| OUT | `any` | Blended Slurry | Uniform mixture of Port 0 + Port 1 | Consequence of mixing |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station ID |
| `equipmentTag` | `string` | — | `MIX-01` | Up to 11 chars | Plant equipment asset tag |
| `controlMode` | `enum` | — | `RATIO_TOTAL`| `RATIO_COMPONENT`, `RATIO_TOTAL`, `BLEND_QUANTITY`, `TARGET_QUANTITY`, `TARGET_DS`, `TARGET_PURITY`, `TARGET_TEMP`, `TARGET_NSW` | Magenta mutual exclusion selector |
| `ratioValue` | `float` | — | 0.25 | 0.0 – 50.0 | Active for `RATIO_COMPONENT` / `RATIO_TOTAL` |
| `targetComponent` | `string` | — | `TOTAL` | `TOTAL`, `SUCROSE`, `CAO`, `WATER`, `NON_SUGAR` | Component for ratio calculation |
| `blendQuantityKgH`| `float` | `kg/h` | 5000.0 | 0.0 – 1,000,000 | Active when `controlMode == BLEND_QUANTITY` |
| `targetQuantityKgH`| `float` | `kg/h` | 50000.0| 0.0 – 2,000,000 | Active when `controlMode == TARGET_QUANTITY` |
| `targetDrySubstancePct`| `float`| `%` | 88.0 | 5.0 – 99.0 | Active when `controlMode == TARGET_DS` |
| `targetPurityPct` | `float` | `%` | 85.0 | 10.0 – 99.9 | Active when `controlMode == TARGET_PURITY` |
| `targetTemperatureC`| `float` | `°C` | 65.0 | 10.0 – 110.0 | Active when `controlMode == TARGET_TEMP` |
| `targetNSWRatio` | `float` | — | 2.50 | 0.1 – 15.0 | Active when `controlMode == TARGET_NSW` |

---

## 4. Governing Equations & Solution Procedure

### 4.1 Blend Flow Determination (By Control Mode)
1. **Ratio to Component / Total**:
   $$\dot{m}_{\text{blend}} = \text{ratioValue} \times (\dot{m}_{\text{prim}} \times z_{\text{comp,prim}})$$
2. **Target Quantity**:
   $$\dot{m}_{\text{blend}} = \text{targetQuantityKgH} - \dot{m}_{\text{prim}}$$
3. **Target Dry Substance ($w_{\text{target}}$)**:
   $$\dot{m}_{\text{blend}} = \frac{w_{\text{target}} \dot{m}_{\text{prim}} - \dot{m}_{\text{DS,prim}}}{w_{\text{DS,blend}} - w_{\text{target}}}$$
4. **Target Purity ($P_{\text{target}}$)**:
   $$\dot{m}_{\text{blend}} = \frac{\dot{m}_{\text{sucrose,prim}} - P_{\text{target}} \dot{m}_{\text{DS,prim}}}{P_{\text{target}} w_{\text{DS,blend}} - w_{\text{sucrose,blend}}}$$
5. **Target Temperature ($T_{\text{target}}$)**:
   $$\dot{m}_{\text{blend}} = \dot{m}_{\text{prim}} \times \frac{h(T_{\text{target}}) - h_{\text{prim}}}{h_{\text{blend}} - h(T_{\text{target}})}$$

### 4.2 Mixture Conservation
$$\dot{m}_{\text{out}} = \dot{m}_{\text{prim}} + \dot{m}_{\text{blend}}$$
$$\dot{m}_{i,\text{out}} = \dot{m}_{i,\text{prim}} + \dot{m}_{i,\text{blend}} \quad \forall i \in \{0, \dots, 14\}$$
$$h_{\text{out}} = \frac{\dot{m}_{\text{prim}} h_{\text{prim}} + \dot{m}_{\text{blend}} h_{\text{blend}}}{\dot{m}_{\text{out}}}$$

---

## 5. Independent Cross-Checks

1. **Total Mass Closure**:
   $$\epsilon_{\text{mass}} = \frac{|(\dot{m}_{\text{prim}} + \dot{m}_{\text{blend}}) - \dot{m}_{\text{out}}|}{\dot{m}_{\text{prim}} + \dot{m}_{\text{blend}}} = 0.0$$
2. **Dry Substance Conservation**:
   $$|(\dot{m}_{\text{DS,prim}} + \dot{m}_{\text{DS,blend}}) - \dot{m}_{\text{DS,out}}| = 0.0$$
3. **Crystal Conservation**:
   $$|(\dot{m}_{\text{cryst,prim}} + \dot{m}_{\text{cryst,blend}}) - \dot{m}_{\text{cryst,out}}| = 0.0$$
