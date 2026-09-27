# Sugar Engineering & Thermodynamic Rules (RULES v5.0)

Authoritative Reference: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`) & `RULES_v5.md`.

## 1. 15-Component Flow Stream Model
All internal flow states use weight fractions ($0.0 \le w_i \le 1.0$), where $\sum_{i=1}^{15} w_i \le 1.0$:

| # | Phase | Name | Internal Key |
|---|---|---|---|
| 1 | Liquid | Water | `water` |
| 2 | Liquid | Dissolved Sucrose | `dissolved_sucrose` |
| 3 | Liquid | Non-Sucrose #1 (Ash & general impurities) | `non_sucrose_1` |
| 4 | Liquid | Non-Sucrose #2 (Invert sugar) | `non_sucrose_2` |
| 5 | Liquid | Component #5 (Ethanol, etc.) | `component_5` |
| 6 | Solid | Sucrose Crystals | `sucrose_crystals` |
| 7 | Solid | Fiber / Insoluble Non-Sucrose (ISNS) | `fiber_isns` |
| 8 | Solid | Calcium Oxide (CaO) | `cao` |
| 9 | Solid | Calcium Carbonate (CaCO3) | `caco3` |
| 10 | Solid | Component #10 | `component_10` |
| 11 | Gas | Water Vapor | `water_vapor` |
| 12 | Gas | Carbon Dioxide (CO2) | `co2` |
| 13 | Gas | Ammonia (NH3) | `nh3` |
| 14 | Gas | Non-Condensable Gas | `non_condensable` |
| 15 | Gas | Component #15 | `component_15` |

### Derived Stream Quantities
```
TDM (Total Dry Matter) = 1.0 - water - water_vapor
DS (Dry Substance)     = TDM  (for soluble streams: 1.0 - water - water_vapor)
Purity                 = (dissolved_sucrose + sucrose_crystals) / DS
NSW                    = non_sucrose_1 / water   [when water > 0]
Sugar%                 = (dissolved_sucrose + sucrose_crystals) * 100
Gas%                   = (water_vapor + co2 + nh3 + non_condensable) * 100
```

---

## 2. Sucrose Solubility & Supersaturation

### 2.1 Vavrinecz Pure Sucrose Saturation (ICUMSA Official)
```
S(t) = 64.397 + 0.07251·t + 0.0002057·t² + 0.000000344·t³  [% sucrose in saturated solution, t in °C]
```

### 2.2 Saturation Coefficient ($S_c$)
- **Vavrinecz Function (when $c \ne 0$):**
  $$S_c = \exp(a \cdot \text{NSW} + b \cdot \text{NSW}^2 + c \cdot \text{NSW}^3)$$
  - Typical Cane: $a = 0.04, b = 0.71, c = -2.1$
  - Beet (Grut): $a = 0.178, b = 0.82, c = -2.1$
  - Beet (Polish): $a = 0.27, b = 0.71, c = -1.4$
- **Wagnerowski Equation (when $c = 0$):**
  $$S_c = 1 + 0.036 \cdot \text{NSW}$$
  *CRITICAL CONSTRAINT*: Valid ONLY for $1.6 \le \text{NSW} \le 3.5$. If $\text{NSW} < 1.6$, fall back to Vavrinecz. If $\text{NSW} > 3.5$, issue warning `NSW_OUT_OF_RANGE`.

### 2.3 Supersaturation ($S_s$) — Van Hook (ICUMSA Official)
$$S_s = \frac{(\text{sucrose} / \text{water})_{\text{sample}}}{(\text{sucrose} / \text{water})_{\text{sat}}}$$
$$(\text{sucrose} / \text{water})_{\text{sat}} = \frac{S(t) \cdot S_c}{100 - S(t) \cdot S_c}$$

---

## 3. Crystal Content Calculations

### 3.1 Forward Calculation ($DS_{mc}, PU_{mc}, T, S_s \rightarrow \text{Crystals}$)
1. $S = \text{sucrose\_saturation\_pct}(T)$
2. $\text{NSW} = (1 - PU_{mc}) \cdot DS_{mc} / (1 - DS_{mc})$
3. $S_c = \text{saturation\_coefficient}(\text{NSW}, a, b, c)$
4. Mother liquor balance:
   $$\frac{DS_{ml} \cdot PU_{ml}}{1 - DS_{ml}} = S_s \cdot \frac{S \cdot S_c}{100 - S \cdot S_c}$$
   $$\frac{(1 - PU_{ml}) \cdot DS_{ml}}{1 - DS_{ml}} = \text{NSW}$$
5. Crystal fraction:
   $$\text{Crystals} = \frac{DS_{mc} - DS_{ml}}{1 - DS_{ml}}$$

*Standard Benchmark Verification Case*:
$DS_{mc} = 0.9300, PU_{mc} = 0.8644, T = 81^\circ\text{C}, S_s = 1.100$, Grut coefficients:
$\rightarrow \text{Crystals} = 0.4744$ (47.44%), $DS_{ml} = 0.8668$, $PU_{ml} = 0.7232$.

### 3.2 Inverse Calculation ($\text{Crystals known} \rightarrow DS_{ml}, PU_{ml}$)
$$DS_{ml} = \frac{DS_{mc} - \text{Cry}}{1 - \text{Cry}}, \quad PU_{ml} = \frac{PU_{mc} \cdot DS_{mc} - \text{Cry}}{DS_{mc} - \text{Cry}}$$

---

## 4. Specific Heat Capacity ($C_p$)

1. **Syrup** (Sugar Tech Manual 8th ed, eq 341/3):
   $$C_{p,\text{syrup}} = (4.187 - 2.884 \cdot DS) + (0.00604 - 0.00382 \cdot DS) \cdot t \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
2. **Sucrose Crystal** (eq 311/2):
   $$C_{p,\text{crystal}} = 1.2473 + 0.002096 \cdot t - 3.9 \times 10^{-6} \cdot t^2 \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
3. **Limestone & Lime** (Boynton):
   $$C_{p,\text{CaCO3}} = 0.819 + 0.000234 \cdot t - \frac{20700}{T_K^2}, \quad C_{p,\text{CaO}} = 0.753 + 0.000117 \cdot t - \frac{11700}{T_K^2}$$
4. **Beet Marc / Fiber** (Vukov):
   $$C_{p,\text{fiber}} = 1.25 + 0.0034 \cdot w_{\text{moisture}}$$
5. **Water & Steam**: Always sourced from **CoolProp + NIST WATER.FLD** (no approximations).

---

## 5. Boiling Point Elevation (BPE)
Kadlec, Bretschneider and Dandor (KBD 1978):
$$\text{BPE} = f(DS, \text{Purity}, P_{\text{abs}}) \quad [^\circ\text{C}]$$
$$T_{\text{boil}} = T_{\text{sat}}(P) + \text{BPE} \cdot \text{BPEFactor}$$
- **Vapor exits at $T_{\text{sat}}(P)$**, NOT at $T_{\text{boil}}$.
- Juice/liquor exits at $T_{\text{boil}}$.

---

## 6. Total Enthalpy & Phase Change
$$H = \sum (w_i \cdot C_{p,i} \cdot t) + w_{\text{steam}} \cdot h_{fg} + w_{\text{crystal}} \cdot \Delta H_{\text{cryst}}$$
- Reference: $0^\circ\text{C}$.
- **Heat of Crystallization**: $+54.9\text{ kJ/kg}$ (exothermic).
- **Heat of Dissolution**: $-54.9\text{ kJ/kg}$ (endothermic).

---

## 7. Conservation Laws at Stations
1. **Total Mass Balance**: $|\sum \dot{m}_{\text{in}} - \sum \dot{m}_{\text{out}}| / \sum \dot{m}_{\text{in}} < 10^{-6}$
2. **15 Components Balance**: Conserved except in reacting/crystallizing stations.
3. **Energy Balance**: $\sum (\dot{m}_{\text{in}} H_{\text{in}}) = \sum (\dot{m}_{\text{out}} H_{\text{out}}) + Q_{\text{loss}} + W_{\text{mech}}$.
