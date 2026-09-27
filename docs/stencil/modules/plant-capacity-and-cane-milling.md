# STENCIL-MILL-01: Plant Capacity & Cane Milling Tandem

## 1. Metadata
- **Stencil ID**: `STENCIL-MILL-01`
- **Module Name**: Plant Capacity, Cane Preparation & Milling Tandem
- **Version**: `1.0.0`
- **Domain Source**: `Sugar's Help Book` (`Examples/Cane_Factory-Milling.md`, `Overview/`)
- **Status**: `ENGINEERING-VALIDATED`

---

## 2. Purpose & Physical Boundary
Governs factory nominal crushing rate, mechanical cane preparation (knives, shredder), and multiple-mill counter-current extraction tandem (typically 4, 5, or 6 three-roller mills). Imbibition water is added before the last mill to extract sucrose from shredded cane, producing final bagasse fuel and mixed juice for clarification.

---

## 3. Governing Equations
- **Mass Balance**:
  $$M_{cane} + M_{imbibition} = M_{mixed\\_juice} + M_{bagasse}$$
- **Fiber Balance**:
  $$M_{bagasse} = M_{cane} \cdot \frac{\text{Fiber}_{cane}}{\text{Fiber}_{bagasse}}$$
- **Pol Extraction**:
  $$\text{Extraction} = \frac{\text{Pol in Mixed Juice}}{\text{Pol in Cane}} \times 100\% \quad (95–97.5\% \text{ standard})$$

---

## 4. Validation & Cross-Checks
- **CHK-MASS-01**: Cane + Imbibition = Mixed Juice + Bagasse ($< 0.001\%$).
- **CHK-FIBER-01**: Total fiber in cane = total fiber in bagasse ($< 10^{-5}\text{ kg/h}$).
