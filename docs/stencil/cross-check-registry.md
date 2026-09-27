# Sugar Engineering Cross-Check Registry

> **Authoritative Basis**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Agent 9: Sugar Stencil Architect**  
> **Cross-Check Protocol**: Every calculation module and flowsheet network must execute independent mathematical balance cross-checks to verify thermodynamic closure.

---

## 1. Master Cross-Check Register

| Check ID | Verification Scope | Governing Relationship | Tolerance | PASS Criteria | WARNING Criteria | FAIL Criteria |
|---|---|---|---|---|---|---|
| **CHK-MASS-01** | Overall Global Wet Mass Balance | $\sum M_{in,ext} - \sum M_{out,ext} = 0$ | $0.001\%$ | $|\Delta M| / M_{in} < 10^{-5}$ | $10^{-5} \le |\Delta M| / M_{in} \le 0.05\%$ | $|\Delta M| / M_{in} > 0.05\%$ |
| **CHK-MASS-02** | Station Local Mass Balance | $\sum M_{in} - \sum M_{out} = 0$ | $10^{-6}\text{ kg/h}$ | $|\Delta M| < 0.01\text{ kg/h}$ | $0.01 \le |\Delta M| \le 1.0\text{ kg/h}$ | $|\Delta M| > 1.0\text{ kg/h}$ |
| **CHK-DS-01** | Dry Substance (DS) Balance | $\sum (M_{in} \cdot DS_{in}) - \sum (M_{out} \cdot DS_{out}) = 0$ | $10^{-6}\text{ kg/h}$ | $|\Delta DS| < 0.01\text{ kg/h}$ | $0.01 \le |\Delta DS| \le 0.5\text{ kg/h}$ | $|\Delta DS| > 0.5\text{ kg/h}$ |
| **CHK-SUC-01** | Sucrose Component Conservation | $\sum (M_{in} \cdot \text{Suc}_{in}) - \sum (M_{out} \cdot \text{Suc}_{out}) = 0$ | $10^{-6}\text{ kg/h}$ | $|\Delta \text{Suc}| < 0.01\text{ kg/h}$ | $0.01 \le |\Delta \text{Suc}| \le 0.5\text{ kg/h}$ | $|\Delta \text{Suc}| > 0.5\text{ kg/h}$ |
| **CHK-NS-01** | Non-Sucrose Conservation | $\sum (M_{in} \cdot \text{NS}_{in}) - \sum (M_{out} \cdot \text{NS}_{out}) = 0$ | $10^{-6}\text{ kg/h}$ | $|\Delta \text{NS}| < 0.01\text{ kg/h}$ | $0.01 \le |\Delta \text{NS}| \le 0.5\text{ kg/h}$ | $|\Delta \text{NS}| > 0.5\text{ kg/h}$ |
| **CHK-ENG-01** | Heat & Enthalpy Closure | $\sum H_{in} + Q_{added} - \sum H_{out} - Q_{loss} = 0$ | $0.05\%$ | $|\Delta H| / H_{in} < 10^{-4}$ | $10^{-4} \le |\Delta H| / H_{in} \le 0.1\%$ | $|\Delta H| / H_{in} > 0.1\%$ |
| **CHK-TEMP-01** | Evaporator Temperature Cascade | $T_{effect,i} > T_{effect,i+1}$ | $0.1^\circ\text{C}$ | Strict monotonic drop | Temperature drop $< 2^\circ\text{C}$ | Temperature inversion ($T_{i} \le T_{i+1}$) |
| **CHK-PRESS-01** | Evaporator Pressure Cascade | $P_{effect,i} > P_{effect,i+1}$ | $0.1\text{ kPa}$ | Strict monotonic drop | Pressure drop $< 1.0\text{ kPa}$ | Pressure inversion ($P_i \le P_{i+1}$) |
| **CHK-BRIX-01** | Evaporator Brix Progression | $\text{Brix}_{effect,i} < \text{Brix}_{effect,i+1}$ | $0.1^\circ\text{Bx}$ | Strict monotonic rise | Brix rise $< 1.0^\circ\text{Bx}$ | Brix stagnation / dilution |
| **CHK-CRY-01** | Crystal Content Consistency | $X_c = \frac{DS_{mc} \cdot (PU_{mc} - PU_{ml})}{1 - PU_{ml}}$ | $0.0001$ | $|X_{c,calc} - X_{c,mass}| < 10^{-4}$ | Discrepancy $< 0.005$ | Discrepancy $> 0.005$ |
| **CHK-CENT-01** | Centrifugal Split Consistency | $W_{green} + W_{wash} + W_{sugar} = W_{mc} + W_{wash\_in}$ | $10^{-5}$ | Exact mass closure | Slight residual | Imbalance $> 1\text{ kg/h}$ |
| **CHK-COND-01** | Barometric Water Heat Absorption | $M_{w} \cdot C_{p} \cdot (T_{out} - T_{in}) = M_{vap} \cdot \Delta h$ | $0.5\%$ | Thermal closure $< 0.1\%$ | Thermal closure $< 1.0\%$ | Thermal closure $> 1.0\%$ |

---

## 2. Multi-Pass Closure Validation Procedure

Every simulation cycle executed by the software must pass through this 3-tier acceptance gate:

1. **Station-Level Gate**: Every individual station solver must achieve zero component mass residuals ($|\Delta m_i| < 10^{-6}\text{ kg/h}$) and enthalpy balance closure within defined heat loss fractions.
2. **Topological Network Gate**: All connecting streams must satisfy endpoint continuity: source port output state $\equiv$ destination port inlet state.
3. **Global Factory Gate**: Global external raw inflows (Cane/Beet, Imbibition Water, Motive Steam, Milk of Lime) must equal all global outward products (Bagasse, Raw/Refined Sugar, Final Molasses, Condensates, Vapour Losses, Mud Cake) within $0.001\%$ mass and solids closure.
