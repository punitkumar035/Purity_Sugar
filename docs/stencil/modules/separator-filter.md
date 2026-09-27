# STENCIL SPECIFICATION: Separator / Filter Station (Centrifugal Runoff & Filtration)
## Module Identifier: `STENCIL-SEP-01`
### Station Type Code: `20` | SUGARS Classification: Separator/Filter

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Separator_Filter/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8, §A9), Selective Component Separation, Diluent Ratio Balance, Energy Conservation  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Separator/Filter station splits an incoming process flow stream into two distinct output flow streams with different compositions and physical characteristics:
- **Centrifugal Sections**: Models wash molasses separation (separating high-grade wash runoff from green mother liquor), sugar crystal separation from mother liquor, magma separation, and screen runoff classification.
- **Filtration & Clarification Sections**: Models rotary vacuum mud filters (separating clear filtrate from filter cake mud), juice clarifier underflow separation, presses, membrane separators, and ion exchange.

### Key Operating Principles from Sugar's Help Book:
1. **Selective Component Separation**: Unlike a distributor/splitter which divides a stream into identical fractions, a separator selectively directs specified percentages of individual components (sucrose crystals, dissolved sucrose, water, non-sucrose, insolubles) to Output #1 vs Output #2.
2. **Diluent / Wash Flow (Port 1)**:
   - Can be operated **with or without diluent/wash**.
   - Diluent ratio options (Magenta mutually exclusive borders):
     - **No Ratio**: Diluent flow is fixed and independent (e.g. from upstream sweetwater or external wash).
     - **Ratio to Component**: Diluent flow is automatically calculated as a ratio to Total Feed, Sucrose, Dry Substance, or Water.
   - User specifies the percentage of diluent that leaves in Output #1 (with remainder leaving in Output #2).
3. **Color Agent Splitting**: Allows selective shift of color agents (e.g. 100% normal split; <100% sends more color to Output #2 and less to Output #1).
4. **Thermal Energy Conservation**: Conserves total enthalpy; excess energy is applied to output streams, or external thermal duty is evaluated.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Process Feed In** | IN | `material` | Massecuite / Juice / Mud | Any multi-component process feed | Known upstream flow |
| **Port 1 In** | **Diluent / Wash In** (Opt)| IN | `material` | Water / Sweetwater / Wash | Wash or diluent solvent | **Conditionally Required [R]** when `Ratio to Component` is active |
| **Port 0 Out**| **Primary Separated Out (Out 1)**| OUT | `material` | Sugar / Filtrate / Runoff 1| Primary separated fraction | Flow determined by component matrix |
| **Port 1 Out**| **Secondary Separated Out (Out 2)**| OUT | `material` | Molasses / Mud Cake / Runoff 2| Residual separated fraction | Balance of feed and diluent |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique station identifier across flowsheet |
| `equipmentTag` | `string` | — | `SEP-01` | Up to 11 chars | Plant equipment asset identifier |
| `diluentMode` | `enum` | — | `NO_RATIO` | `NO_RATIO` / `RATIO_COMPONENT` | Magenta mutually exclusive control |
| `diluentRatio` | `float` | — | 0.100 | 0.0 – 5.0 | Multiplier on chosen input component when `RATIO_COMPONENT` is active |
| `diluentRatioBasis`| `enum` | — | `TOTAL` | `TOTAL`, `SUCROSE`, `DS`, `WATER` | Basis stream component for diluent ratio calculation |
| `diluentOut1Pct` | `float` | `%` | 30.0 | 0.0 – 100.0 | Percentage of diluent stream exiting in Out Flow #1 |
| `comp1Name` | `string` | — | `SUCROSE_CRYSTALS`| Component ID | Component 1 selector |
| `comp1Out1Pct` | `float` | `%` | 100.0 | 0.0 – 100.0 | % of Component 1 entering Out Flow #1 |
| `comp2Name` | `string` | — | `DISSOLVED_SUCROSE`| Component ID | Component 2 selector |
| `comp2Out1Pct` | `float` | `%` | 50.0 | 0.0 – 100.0 | % of Component 2 entering Out Flow #1 |
| `comp3Name` | `string` | — | `WATER` | Component ID | Component 3 selector |
| `comp3Out1Pct` | `float` | `%` | 40.0 | 0.0 – 100.0 | % of Component 3 entering Out Flow #1 |
| `comp4Name` | `string` | — | `NON_SUCROSE_1` | Component ID | Component 4 selector |
| `comp4Out1Pct` | `float` | `%` | 30.0 | 0.0 – 100.0 | % of Component 4 entering Out Flow #1 |
| `otherCompOut1Pct`| `float` | `%` | 0.0 | 0.0 – 100.0 | % of all other remaining components entering Out Flow #1 |
| `colorOut1Pct` | `float` | `%` | 100.0 | 0.0 – 100.0 | Color split to Out Flow #1 (<100% shifts color to Out Flow #2) |

---

## 4. Governing Equations

### 4.1 Diluent Demand
If `diluentMode == 'RATIO_COMPONENT'`:
$$\dot{M}_{dil,req} = \text{diluentRatio} \times \dot{M}_{basis,in}$$

### 4.2 Component Mass Distribution
For any component $c$ in the 15-component ledger:
$$\dot{m}_{c,1} = \dot{m}_{c,feed} \cdot f_{c,1} + \dot{m}_{c,dil} \cdot \left(\frac{\text{diluentOut1Pct}}{100}\right)$$
$$\dot{m}_{c,2} = \dot{m}_{c,feed} \cdot (1 - f_{c,1}) + \dot{m}_{c,dil} \cdot \left(1 - \frac{\text{diluentOut1Pct}}{100}\right)$$

### 4.3 Total Mass & Dry Substance
$$\dot{M}_1 = \sum_{c} \dot{m}_{c,1}, \quad \dot{M}_2 = \sum_{c} \dot{m}_{c,2}$$
$$DS_1 = \frac{\sum_{solids} \dot{m}_{c,1}}{\dot{M}_1}, \quad DS_2 = \frac{\sum_{solids} \dot{m}_{c,2}}{\dot{M}_2}$$

---

## 5. Independent Physical Balance Cross-Checks

1. **Overall Mass Balance**: $\dot{M}_{feed} + \dot{M}_{dil} = \dot{M}_1 + \dot{M}_2 \pm 0.001\%$
2. **Dry Substance Conservation**: $\dot{M}_{DS,feed} + \dot{M}_{DS,dil} = \dot{M}_{DS,1} + \dot{M}_{DS,2} \pm 0.0001\%$
3. **Every Component Conservation**: $\dot{m}_{c,in} = \dot{m}_{c,1} + \dot{m}_{c,2} \pm 10^{-6}\text{ kg/h}$
4. **Thermal Enthalpy Conservation**: $H_{in} = H_1 + H_2 \pm 0.05\%$
