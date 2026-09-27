# Calculation Register

This register catalogs all engineering and thermodynamic calculations in Purity for Sugar, their governing equations, reference sources, and validation tests.

| Calc ID | Description | Source / Reference | Inputs | Outputs | Validation Criteria / Tests |
|---|---|---|---|---|---|
| **CALC-SOL-01** | Pure Sucrose Saturation | ICUMSA / Vavrinecz | Temperature ($^\circ\text{C}$) | Saturation wt% (0–100%) | $S(20^\circ\text{C}) = 66.72 \pm 0.05\%$; $S(80^\circ\text{C}) = 78.68 \pm 0.05\%$ |
| **CALC-SOL-02** | Saturation Coefficient (Vavrinecz) | `Sugar's Help Book` (Theory.htm) | $\text{NSW}, a, b, c$ | $S_c$ (dimensionless) | $\text{NSW}=2.0$, Grut: $S_c \approx 1.18 \pm 0.05$ |
| **CALC-SOL-03** | Saturation Coefficient (Wagnerowski) | `Sugar's Help Book` (Theory.htm) | $\text{NSW}$ ($1.6 \le \text{NSW} \le 3.5$) | $S_c$ (dimensionless) | $\text{NSW}=2.0, c=0 \implies S_c = 1.072 \pm 0.001$ |
| **CALC-SOL-04** | Supersaturation ($S_s$) | Van Hook (ICUMSA) | $DS_{ml}, PU_{ml}, T, a, b, c$ | $S_s$ (dimensionless) | $DS=0.8668, PU=0.7232, T=81^\circ\text{C} \implies S_s = 1.100 \pm 0.005$ |
| **CALC-CRY-01** | Forward Crystal Content | `Sugar's Help Book` (Theory.htm) | $DS_{mc}, PU_{mc}, T, S_s, a, b, c$ | Crystal fraction, $DS_{ml}, PU_{ml}$ | Benchmark: $0.9300, 0.8644, 81^\circ\text{C}, 1.100 \implies \text{Cry}=0.4744 \pm 0.005$ |
| **CALC-CRY-02** | Inverse Crystal Content | Mass balance ($DS_{cs}=PU_{cs}=1$) | $DS_{mc}, PU_{mc}, \text{Cry}$ | $DS_{ml}, PU_{ml}$ | Round-trip matches forward calculation within $\pm 0.005$ |
| **CALC-BPE-01** | Boiling Point Elevation | KBD 1978 | $DS, \text{Purity}, P_{\text{abs}}$ | $\text{BPE}$ ($^\circ\text{C}$) | Pure water ($DS=0$) has $\text{BPE}=0.0^\circ\text{C}$; typical evap $0.5 < \text{BPE} < 3.0^\circ\text{C}$ |
| **CALC-CP-01** | Syrup Specific Heat | Sugar Tech Manual eq 341/3 | $DS$ fraction, $t$ ($^\circ\text{C}$) | $C_p$ ($\text{kJ}/(\text{kg}\cdot\text{K})$) | $DS=0, t=20^\circ\text{C} \implies C_p = 4.187 \pm 0.01$ |
| **CALC-CP-02** | Sucrose Crystal Specific Heat | Sugar Tech Manual eq 311/2 | $t$ ($^\circ\text{C}$) | $C_p$ ($\text{kJ}/(\text{kg}\cdot\text{K})$) | $t=20^\circ\text{C} \implies C_p = 1.288 \pm 0.005$ |
| **CALC-ENT-01** | Total Stream Enthalpy | Summation over 15 components | Fractions, $T, P$ | $H$ ($\text{kJ}/\text{kg}$) | Saturated steam at $100^\circ\text{C} \implies H = 2675.6 \pm 1.0\text{ kJ}/\text{kg}$ |
| **CALC-DEN-01** | Syrup & Massecuite Density | Bubník-Kadlec | $DS, T$ ($^\circ\text{C}$) | $\rho$ ($\text{kg}/\text{m}^3$) | $DS=82.3\%, T=73^\circ\text{C} \implies \rho \approx 1350 \pm 50\text{ kg}/\text{m}^3$ |
| **CALC-CEN-01** | Centrifugal 2-Output Balance | `Sugar's Help Book` (Centrifugal) | $W_{mc}, DS_{mc}, PU_{mc}, R, P_w, P_l, Z$ | $W_g, W_s, DS_g, PU_g, DS_s, PU_s$ | Weight, DS, and sucrose closures within $< 10^{-6}$ |
| **CALC-EVP-01** | Evaporator Effect Balance | `Sugar's Help Book` (Evaporator) & IF-97 | $M_{j}, \text{Bx}_{j}, T_j, P_{vap}, \text{Target Bx}, P_{steam}$ | $M_{syrup}, M_{vap}, M_{steam}, T_{boil}, \text{BPE}$ | Wet mass, dry solids, and energy closures $< 10^{-5}$ |
| **CALC-HTR-01** | Juice / Process Heater Balance | `Sugar's Help Book` (Heat Exchanger) & IF-97 | $M_{j}, \text{Bx}_{j}, T_{in}, T_{out}, P_{steam}$ | $M_{steam}, M_{cond}, Q_{duty}$ | Heat duty and mass closure $< 10^{-5}$ |
| **CALC-FLT-01** | Flash Tank Balance | `Sugar's Help Book` (Flash Tank) & IF-97 | $M_{in}, \text{Bx}_{in}, T_{in}, P_{flash}$ | $M_{out}, M_{vap}, \text{Bx}_{out}, T_{out}$ | Sensible heat release to vapour conversion, solids closure $< 10^{-6}$ |
| **CALC-MLT-01** | Sugar Melter Dissolution | `Sugar's Help Book` (Melter) | $M_{s}, \text{Bx}_{s}, \text{Target Bx}, \text{Bx}_{m}, T_{target}$ | $M_{m}, M_{melt}, M_{steam}, T_{melt}$ | Crystal dissolution to liquid sucrose, solids closure $< 10^{-6}$ |
| **CALC-MGM-01** | Magma Mixer Balance | `Sugar's Help Book` (Melter / Mixer) | $M_{s}, M_{d}, \text{Crystals}_{s}, T_s, T_d$ | $M_{magma}, \text{Bx}, \text{Crystals}, T_{magma}$ | Crystal content preservation, mass closure $< 10^{-6}$ |
| **CALC-BAL-01** | Consolidated Factory Mass & DS Closure | Master Protocol & RULES v5 | Global external streams $\&$ station ledgers | Total In, Total Out, $\Delta \text{Mass}, \Delta \text{DS}$, Closure % | Global closure reporting and CSV/PDF export |

