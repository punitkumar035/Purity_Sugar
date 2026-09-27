# STENCIL-PAN-01: Vacuum Pan Evaporative Crystallization

## 1. Metadata
- **Stencil ID**: `STENCIL-PAN-01`
- **Module Name**: Vacuum Pan (Batch & Continuous Boiling)
- **Equipment Type**: Type 14 Massecuite Pan
- **Version**: `1.0.0`
- **Domain Source**: `Sugar's Help Book` (`Pan/`, `Theory/Theory.md`, `Sucrose_Supersaturation/`)
- **Status**: `ENGINEERING-VALIDATED`

---

## 2. Purpose & Physical Boundary
Crystallizes sucrose from syrup, remelt liquor, or molasses feeds by controlled vacuum boiling. Operates at low temperature ($60–75^\circ\text{C}$) to avoid sucrose inversion and caramelization. Produces commercial massecuite consisting of mother liquor and pure sucrose crystals, calandria condensate, and evaporated pan vapour.

---

## 3. Engineering Basis & Citations
- **Sucrose Solubility & Saturation**: Vavrinecz pure sucrose solubility polynomial; Vavrinecz/Wagnerowski non-sucrose saturation coefficient $S_c$.
- **Supersaturation**: Van Hook / ICUMSA definition $S_s = (S/W)_{ml} / [S_c \cdot (S/W)_{sat}]$.
- **Crystal Content Balance**: Simultaneous solution of mother liquor mass conservation and purity exhaustion.
- **Boiling Point Elevation**: Bubník-Kadlec (1995) / KBD (1978) taking into account high Brix ($88–95^\circ\text{Brix}$) and purity ($50–99\%$).
- **Thermal Balance**: Calandria condensing steam latent heat satisfies evaporation and sensible massecuite heating minus exothermic crystallization heat of sucrose ($Q_{cryst} \approx 20\text{ kJ/kg crystal}$).

---

## 4. Port Architecture
- **Inlets**:
  - `syrup`: Syrup / Molasses / Process Feed (Category: `material`). Required.
  - `steam`: Heating Steam / Evaporator Bleed Vapour (Category: `thermal`). Required.
- **Outlets**:
  - `mc`: Massecuite Out (Category: `material`).
  - `vapour`: Pan Vapour Out (Category: `thermal`).
  - `condensate`: Calandria Condensate Out (Category: `condensate`).

---

## 5. Input Field Classification

### A. Required User Inputs
| Field ID | Label | Unit | Type | Default | Expected Range | Description |
|---|---|---|---|---|---|---|
| `feed_flow` | Feed Liquor Flow Rate | `kg/h` | Number | — | $5,000–150,000$ | Inflow mass rate of syrup or runoff |
| `feed_ds` | Feed Dry Substance (DS) | `%` | Number | 65.0 | $55.0–75.0$ | Feed dry solids fraction |
| `feed_purity` | Feed True Purity | `%` | Number | 85.0 | $50.0–99.5$ | Feed sucrose / dry solids |
| `feed_temp` | Feed Temperature | `°C` | Number | 70.0 | $55.0–85.0$ | Temperature of feed entering pan |

### B. Controlled Operational Dropdowns & Mode Switches
| Field ID | Label | Control Type | Allowed Options | Default | Description |
|---|---|---|---|---|---|
| `operation_mode` | Pan Operation Mode | Dropdown | `CONTINUOUS`, `BATCH` | `CONTINUOUS` | Steady-state continuous vs batch cycle |
| `solids_control` | Solids Control Mode | Dropdown | `MASSECUITE_DS`, `SUPERSATURATION`, `ML_PURITY` | `MASSECUITE_DS` | Governing setpoint selection |
| `pressure_mode` | Operating Pressure Mode | Dropdown | `VAPOUR_PRESSURE`, `VAPOUR_TEMP` | `VAPOUR_PRESSURE` | Governing pan vacuum setpoint |
| `solubility_basis` | Solubility Model Basis | Dropdown | `CANE_TYPICAL`, `BEET_TYPICAL`, `CUSTOM` | `CANE_TYPICAL` | Defines Vavrinecz constants $a, b, c$ |

### C. Optional & Equipment Design Inputs
| Field ID | Label | Unit | Type | Default | Description |
|---|---|---|---|---|---|
| `target_massecuite_ds` | Target Massecuite DS | `% DS` | Number | 90.0 | High-brix final strike dry substance |
| `output_supersaturation`| Mother Liquor Target SS | Dimensionless | Number | 1.10 | Target metastate driving crystallization |
| `pan_vapour_pressure` | Operating Vapour Pressure | `kPa abs` | Number | 16.0 | Typically 14–22 kPa abs ($60–65^\circ\text{C}$ sat) |
| `heat_loss_pct` | Pan Body Radiation Loss | `%` | Number | 2.0 | Heat lost from calandria transfer |
| `condensate_subcooling`| Condensate Subcooling | `°C` | Number | 0.0 | Calandria drain subcooling |
| `entrainment_ppm` | Vapour Sugar Entrainment | `ppm` | Number | 50.0 | Sugar droplets carried into vapour pipe |

---

## 6. Calculation Sequence & Traceability
1. **Saturation Ratio**: At pan operating vacuum $P_{vap}$, calculate pure water saturation temperature $T_{sat}$.
2. **Mother Liquor & BPE Iteration**: Solve coupled equation pair:
   - $S_{c} = 1 - b \cdot \text{NSW} + a \cdot (1 - e^{-c \cdot \text{NSW}})$
   - $S_{pure} = \text{Vavrinecz}(T_{boil})$
   - $DS_{ml} = \frac{DS_{mc} \cdot (1 - PU_{mc})}{1 - PU_{ml}}$
   - $T_{boil} = T_{sat} + \text{BPE}(DS_{ml}, PU_{ml}, P_{vap})$
3. **Crystal Mass Extraction**:
   $$M_{cryst} = M_{mc} \cdot \frac{DS_{mc} \cdot (PU_{mc} - PU_{ml})}{1 - PU_{ml}}$$
4. **Thermal Balance**: Calandria steam consumption derived from sensible heat of feed, latent heat of evaporation, minus exothermic crystallization heat.

---

## 7. Mathematical Formulations
- **Massecuite Crystal Yield**:
  $$X_c = \frac{DS_{mc} - DS_{ml}}{1 - DS_{ml}}$$
- **Evaporated Vapour**:
  $$V = M_{feed} - M_{mc} = M_{feed} \cdot \left(1 - \frac{DS_{feed}}{DS_{mc}}\right)$$
- **Calandria Steam Demand**:
  $$M_{steam} = \frac{M_{feed} \cdot C_{p} \cdot (T_{boil} - T_{feed}) + V \cdot \Delta h_{vap} - M_{cryst} \cdot \Delta h_{cryst}}{(1 - f_{loss}) \cdot (h_{steam} - h_{cond})}$$

---

## 8. Validation Rules & Limits
- **VAL-PAN-001**: $DS_{mc} > DS_{feed}$ strictly enforced (**FATAL_ERROR**).
- **VAL-PAN-002**: $1.00 \le SS \le 1.25$ operating zone (**WARNING** if outside).
- **VAL-PAN-003**: $PU_{ml} < PU_{mc}$ strictly required (**FATAL_ERROR** if violated).

---

## 9. Independent Engineering Cross-Checks
- **Total Sucrose Conservation**: $(M_{feed} \cdot DS_{feed} \cdot PU_{feed}) = (M_{mc} \cdot DS_{mc} \cdot PU_{mc}) + (V \cdot \text{Entrained Sucrose})$ (PASS $< 0.001\text{ kg/h}$).
- **Non-Sucrose Conservation**: $M_{feed} \cdot DS_{feed} \cdot (1 - PU_{feed}) = M_{mc} \cdot DS_{mc} \cdot (1 - PU_{mc})$ (PASS $< 0.001\text{ kg/h}$).
- **Thermal Closure**: Gross heat supplied = process demand + heat loss (PASS $< 0.01\%$).

---

## 10. Wireframe / UI Layout Stencil
```text
┌────────────────────────────────────────────────────────────────────────┐
│ VACUUM PAN STATION [PAN-01]                                            │
├────────────────────────────────────────────────────────────────────────┤
│ SPECIFICATIONS                                                         │
│ Massecuite Strike Type  [ A-Massecuite               ▼ ]               │
│ Solids Control Mode     [ Massecuite DS              ▼ ]               │
│ Target Massecuite DS    [ 90.00                      ] % DS            │
│ Target Supersaturation  [ 1.100                      ] Dimensionless   │
│ Operating Vacuum Press  [ 16.00                      ] kPa abs         │
│ Calandria Steam Press   [ 120.00                     ] kPa abs         │
├────────────────────────────────────────────────────────────────────────┤
│ SOLVER RESULTS                                                         │
│ Massecuite Flow Rate    [ 54,166.67                  ] kg/h (54.2 t/h) │
│ Crystal Content (Xc)    [ 47.44                      ] % on massecuite │
│ Crystal Production Rate [ 25,697.55                  ] kg/h crystal    │
│ Mother Liquor Purity    [ 72.32                      ] % true purity   │
│ Mother Liquor DS        [ 86.68                      ] % DS            │
│ Massecuite Boiling Temp [ 68.45                      ] °C              │
│ Pan Vapour Evaporation  [ 20,833.33                  ] kg/h (20.8 t/h) │
│ Calandria Steam Demand  [ 22,410.82                  ] kg/h (22.4 t/h) │
├────────────────────────────────────────────────────────────────────────┤
│ CLOSURE STATUS                                                         │
│ Sucrose Balance Closure [ 100.0000                   ] %    (PASS)     │
│ Non-Sucrose Closure     [ 100.0000                   ] %    (PASS)     │
│ Energy Balance Closure  [ 100.0000                   ] %    (PASS)     │
└────────────────────────────────────────────────────────────────────────┘
```
