# STENCIL-CENT-01: Centrifugal Separation Station

## 1. Metadata
- **Stencil ID**: `STENCIL-CENT-01`
- **Module Name**: Centrifugal Station (2-Output Continuous & 3-Output Batch)
- **Equipment Type**: Type 2A (2-Output) & Type 2B (3-Output) Centrifugals
- **Version**: `1.0.0`
- **Domain Source**: `Sugar's Help Book` (`Centrifugal/`, `Theory/Theory.md`)
- **Status**: `ENGINEERING-VALIDATED`

---

## 2. Purpose & Physical Boundary
Separates sucrose crystals from massecuite mother liquor under centrifugal force ($1,000–2,500\times g$). Applies wash water and/or steam to displace residual mother liquor film adhering to crystal surfaces. Produces purged commercial sugar and runoff molasses (green molasses and optional wash molasses).

---

## 3. Engineering Basis & Citations
- **Purge Factors**:
  - $Z_g$: Fraction of massecuite mother liquor purged into green molasses stream.
  - $P_w$: Purge efficiency of wash water into molasses.
  - $P_l$: Residual mother liquor retained per unit mass of crystal sugar.
- **Crystal Dissolution Mechanics**: If wash water or molasses film is undersaturated ($S_s < 1.0$), sucrose crystals dissolve until thermodynamic saturation ($S_s = 1.0$) is reached or wash is saturated.
- **Batch vs Continuous Differentiation**:
  - Continuous (2-Output): Low-grade massecuites (C-massecuite). Runoff combined as final molasses.
  - Batch (3-Output): High-grade massecuites (A/B-massecuite). Separate collection of heavy green molasses and light wash molasses.

---

## 4. Port Architecture
- **Inlets**:
  - `mc`: Massecuite In (Category: `massecuite`). Required.
  - `wash`: Wash Water / Steam In (Category: `water`). Required.
- **Outlets**:
  - `sugar`: Purged Sugar Out (Category: `material`).
  - `green`: Green / Heavy Molasses Out (Category: `material`).
  - `light`: Wash / Light Molasses Out (Category: `material`, Batch 3-Output only).

---

## 5. Input Field Classification

### A. Required User Inputs
| Field ID | Label | Unit | Type | Default | Expected Range |
|---|---|---|---|---|---|
| `mc_flow` | Massecuite Inflow Rate | `kg/h` | Number | — | $1,000–100,000$ |
| `mc_ds` | Massecuite Dry Substance | `%` | Number | 90.0 | $85.0–96.0$ |
| `mc_purity` | Massecuite True Purity | `%` | Number | 85.0 | $50.0–99.0$ |
| `mc_temp` | Massecuite Inflow Temp | `°C` | Number | 55.0 | $40.0–75.0$ |
| `wash_water_ratio` | Wash Water / Massecuite Ratio | `kg/kg` | Number | 0.030 | $0.00–0.12$ |
| `wash_temp` | Wash Water Temperature | `°C` | Number | 85.0 | $60.0–98.0$ |

### B. Machine Performance & Purge Selection
| Field ID | Label | Control Type | Default | Description |
|---|---|---|---|---|
| `cent_mode` | Machine Evaluation Mode | Dropdown | `HELPBOOK_EVAL` | `HELPBOOK_EVAL`, `PRESCRIBED_PURGE`, `FIXED_YIELD` |
| `machine_type` | Centrifugal Machine Type | Dropdown | `BATCH` (3-out) / `CONT` (2-out) | Physical basket type |
| `purge_zg` | Mother Liquor Purge Fraction ($Z_g$) | Number | 0.85 | Fraction mother liquor purged to green |
| `purge_pw` | Wash Water Purge Fraction ($P_w$) | Number | 0.90 | Fraction wash water purged to molasses |

---

## 6. Mathematical Formulations
- **Crystal Mass in Feed**:
  $$M_{cryst,mc} = M_{mc} \cdot X_{c,mc}$$
- **Sugar Mass Output**:
  $$M_{sugar} = M_{cryst,mc} \cdot (1 - f_{diss}) + M_{ml,sugar} + M_{wash,sugar}$$
- **Green Molasses Output**:
  $$M_{green} = M_{ml,mc} \cdot Z_g + M_{wash} \cdot (1 - P_w) + M_{cryst,lost}$$

---

## 7. Validation & Cross-Checks
- **VAL-CENT-001**: Sugar purity must exceed massecuite purity ($PU_{sugar} > PU_{mc}$).
- **CHK-MASS-01**: $M_{sugar} + M_{green} (+ M_{wash\\_mol}) = M_{mc} + M_{wash\\_in}$ ($< 10^{-6}\text{ kg/h}$).
- **CHK-DS-01**: Total dry solids in sugar + molasses = total solids in massecuite + wash solids.

---

## 8. Wireframe / UI Layout Stencil
```text
┌────────────────────────────────────────────────────────────────────────┐
│ CENTRIFUGAL STATION [CEN-01]                                           │
├────────────────────────────────────────────────────────────────────────┤
│ SPECIFICATIONS                                                         │
│ Machine Type            [ 3-Output Batch Centrifugal ▼ ]               │
│ Wash Water Ratio        [ 0.0300                     ] kg/kg mc        │
│ Wash Water Temperature  [ 85.0                       ] °C              │
│ Mother Liquor Purge Zg  [ 0.8500                     ] Fraction        │
│ Wash Water Purge Pw     [ 0.9000                     ] Fraction        │
├────────────────────────────────────────────────────────────────────────┤
│ SEPARATION RESULTS                                                     │
│ Purged Sugar Flow       [ 24,150.20                  ] kg/h (24.2 t/h) │
│ Sugar Pol / Purity      [ 99.65                      ] % True Purity   │
│ Sugar Moisture          [ 0.85                       ] % Moisture      │
│ Green Molasses Flow     [ 27,412.50                  ] kg/h (27.4 t/h) │
│ Green Molasses Purity   [ 72.40                      ] % True Purity   │
│ Wash Molasses Flow      [ 4,037.30                   ] kg/h (4.0 t/h)  │
│ Wash Molasses Purity    [ 81.15                      ] % True Purity   │
├────────────────────────────────────────────────────────────────────────┤
│ CLOSURE STATUS                                                         │
│ Wet Mass Residual       [ 0.000000                   ] kg/h (PASS)     │
│ Dry Substance Residual  [ 0.000000                   ] kg/h (PASS)     │
└────────────────────────────────────────────────────────────────────────┘
```
