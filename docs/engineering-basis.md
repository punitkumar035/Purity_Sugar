# Engineering Basis & Thermodynamic Formulations

Authoritative Source: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`) and `RULES_v5.md`.

## 1. Pure Sucrose Solubility (Vavrinecz / ICUMSA)

The solubility of pure sucrose in water as a function of temperature ($t$ in $^\circ\text{C}$):
$$S(t) = 64.397 + 0.07251 \cdot t + 0.0002057 \cdot t^2 + 0.000000344 \cdot t^3$$
- Output: $S(t) = \text{weight percent sucrose in saturated solution}$ (0–100%).
- Standard Values:
  - $t = 20^\circ\text{C} \implies S = 67.09\%$
  - $t = 80^\circ\text{C} \implies S = 74.18\%$

---

## 2. Saturation Coefficient ($S_c$)

Quantifies the effect of non-sucrose impurities on sucrose solubility.

### 2.1 Vavrinecz Exponential Equation (when $c \ne 0$)
$$S_c = \exp\left(a \cdot \text{NSW} + b \cdot \text{NSW}^2 + c \cdot \text{NSW}^3\right)$$
Where $\text{NSW} = \text{Non-Sucrose} / \text{Water}$ ratio by weight.

**Reference Coefficients**:
| Origin / Authority | $a$ | $b$ | $c$ |
|---|---|---|---|
| Cane (Typical) | 0.04 | 0.71 | -2.1 |
| Beet (Grut) | 0.178 | 0.82 | -2.1 |
| Beet (Polish) | 0.27 | 0.71 | -1.4 |

### 2.2 Wagnerowski Equation (when $c = 0$)
$$S_c = 1 + 0.036 \cdot \text{NSW}$$
*Validity Limit*: $1.6 \le \text{NSW} \le 3.5$.

---

## 3. Supersaturation ($S_s$) — Van Hook Definition

$$S_s = \frac{(\text{sucrose} / \text{water})_{\text{sample}}}{(\text{sucrose} / \text{water})_{\text{sat}}}$$
$$(\text{sucrose} / \text{water})_{\text{sat}} = \frac{S(t) \cdot S_c}{100 - S(t) \cdot S_c}$$

---

## 4. Crystal Content Equations

### 4.1 Forward Mode (Given $DS_{mc}, PU_{mc}, T, S_s$)
$$\text{NSW} = \frac{(1 - PU_{mc}) \cdot DS_{mc}}{1 - DS_{mc}}$$
Mother liquor dry substance ($DS_{ml}$) and purity ($PU_{ml}$) are solved simultaneously from:
$$\frac{DS_{ml} \cdot PU_{ml}}{1 - DS_{ml}} = S_s \cdot \frac{S(T) \cdot S_c}{100 - S(T) \cdot S_c}$$
$$\frac{(1 - PU_{ml}) \cdot DS_{ml}}{1 - DS_{ml}} = \text{NSW}$$

Crystal fraction:
$$\text{Crystal Fraction} = \frac{DS_{mc} - DS_{ml}}{1 - DS_{ml}}$$

### 4.2 Benchmark Case
- Input: $DS_{mc} = 0.9300, PU_{mc} = 0.8644, T = 81^\circ\text{C}, S_s = 1.100$, Grut coefficients ($a=0.178, b=0.82, c=-2.1$).
- Output: $\text{Crystals} = 47.44\%$, $DS_{ml} = 86.68\%$, $PU_{ml} = 72.32\%$.

---

## 5. Specific Heat Capacity ($C_p$)

1. **Syrup** (Sugar Technologists Manual 8th ed, eq 341/3):
   $$C_p = (4.187 - 2.884 \cdot DS) + (0.00604 - 0.00382 \cdot DS) \cdot t \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
2. **Sucrose Crystal** (eq 311/2):
   $$C_p = 1.2473 + 0.002096 \cdot t - 3.9 \times 10^{-6} \cdot t^2 \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
3. **Limestone & Lime** (Boynton):
   $$C_{p,\text{CaCO3}} = 0.819 + 0.000234 \cdot t - \frac{20700}{T_K^2}$$
   $$C_{p,\text{CaO}} = 0.753 + 0.000117 \cdot t - \frac{11700}{T_K^2}$$
4. **Beet Marc / Fiber** (Vukov):
   $$C_{p,\text{fiber}} = 1.25 + 0.0034 \cdot w_{\text{moisture}}$$
5. **Water and Steam**: Evaluated from **CoolProp + NIST WATER.FLD**.

---

## 6. Boiling Point Elevation (BPE)
Evaluated via Kadlec, Bretschneider and Dandor (KBD 1978).
- Solution boiling temperature: $T_{\text{boil}} = T_{\text{sat}}(P) + \text{BPE} \cdot \text{BPEFactor}$.
- **Vapor exits at $T_{\text{sat}}(P)$**, not at $T_{\text{boil}}$.
