# Sugar Engineering Formula Registry

> **Authoritative Basis**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Agent 9: Sugar Stencil Architect**  
> **Standard Units**: Flow in `kg/h` (display `t/h`), Temperature in `°C`, Pressure in `kPa abs`, Brix/Purity in `%` (internal fractions `0.0–1.0`), Enthalpy in `kJ/kg`.

---

## 1. Physical Chemistry & Thermodynamics

### FORMULA-SOL-001: Pure Sucrose Solubility (ICUMSA / Vavrinecz 1962)
- **Topic**: Sucrose Solubility in Water
- **Equation**:
  $$S = 64.397 + 0.07251 \cdot t + 0.0028818 \cdot t^2 - 0.5844 \times 10^{-6} \cdot t^3$$
- **Variables**:
  - $S$: Sucrose solubility in pure water, mass % sucrose ($g$ sucrose / $100\,g$ solution)
  - $t$: Solution temperature, $^\circ\text{C}$
- **Pure Sucrose-to-Water Ratio at Saturation**:
  $$\left(\frac{S}{W}\right)_{pure} = \frac{S}{100 - S}$$
- **Applicability & Conditions**: Valid from $0^\circ\text{C} \le t \le 100^\circ\text{C}$. Official ICUMSA equation.
- **Source**: `Theory/Theory.md`, section "Sucrose Solubility", citing ICUMSA.
- **Software Implementation**: Strict polynomial evaluation; clamps $t$ between $0$ and $100^\circ\text{C}$; raises error if $t < -5^\circ\text{C}$.

---

### FORMULA-SOL-002: Saturation Coefficient — Vavrinecz Function
- **Topic**: Sucrose Solubility in Impure Solutions
- **Equation**:
  $$S_c = 1 - b \cdot \text{NSW} + a \cdot \left(1 - e^{-c \cdot \text{NSW}}\right)$$
- **Variables**:
  - $S_c$: Saturation coefficient (ratio of solubility in impure solution to pure water solubility), dimensionless
  - $\text{NSW}$: Non-sucrose to water ratio ($g$ non-sucrose / $g$ water)
  - $a, b, c$: Molasses solubility coefficients depending on nature of non-sugars
- **Applicability & Conditions**: General sugar solutions. Independent of temperature. If $c = 0$, falls back to Wagnerowski equation.
- **Default Coefficients**:
  - Cane typical: $a = 0.0400, b = 0.7100, c = -2.1000$ (or custom approved)
  - Beet typical: $a = 0.333, b = 0.000, c = 0.000$
- **Source**: `Theory/Theory.md`, section "Sucrose Solubility".

---

### FORMULA-SOL-003: Saturation Coefficient — Wagnerowski Equation
- **Topic**: Sucrose Solubility in Factory Molasses ($c = 0$)
- **Equation**:
  $$S_c = a + b \cdot \text{NSW}$$
- **Variables**:
  - $S_c$: Saturation coefficient, dimensionless
  - $\text{NSW}$: Non-sucrose to water ratio
  - $a, b$: Empirical constants
- **Applicability & Conditions**: Valid strictly for $1.6 \le \text{NSW} \le 3.5$. Outside this range, Vavrinecz function must be used.
- **Source**: `Theory/Theory.md`, section "Sucrose Solubility".

---

### FORMULA-SOL-004: Sucrose Supersaturation (Van Hook / ICUMSA)
- **Topic**: Supersaturation Evaluation
- **Equation**:
  $$S_s = \frac{(S/W)_{ml}}{(S/W)_{sat}} = \frac{(S/W)_{ml}}{S_c \cdot (S/W)_{pure}}$$
- **Variables**:
  - $S_s$: Supersaturation coefficient of mother liquor, dimensionless
  - $(S/W)_{ml}$: Actual sucrose to water mass ratio in mother liquor ($g$ sucrose / $g$ water)
  - $(S/W)_{sat}$: Saturated sucrose to water mass ratio at the same temperature and NSW
- **Operating Zones**:
  - $S_s < 1.0$: Under-saturated (crystal dissolution zone)
  - $1.0 \le S_s \le 1.15$: Metastable zone (existing crystals grow, no spontaneous nucleation)
  - $1.15 < S_s \le 1.30$: Intermediate zone (false graining possible if disturbed)
  - $S_s > 1.30$: Labile zone (spontaneous spontaneous nucleation occurs)
- **Source**: `Theory/Theory.md`, `Sucrose_Supersaturation/Supersaturation.md`.

---

### FORMULA-CRY-001: Crystal Content Mass Balance
- **Topic**: Massecuite Crystal Content & Mother Liquor Exhaustion
- **Equation**:
  $$X_c = \frac{DS_{mc} - DS_{ml}}{1 - DS_{ml}} = \frac{DS_{mc} \cdot (PU_{mc} - PU_{ml})}{1 - PU_{ml}}$$
- **Variables**:
  - $X_c$: Crystal content fraction ($g$ pure crystal sucrose / $g$ wet massecuite)
  - $DS_{mc}$: Massecuite total dry substance fraction ($0.0–1.0$)
  - $PU_{mc}$: Massecuite true purity fraction ($0.0–1.0$)
  - $DS_{ml}$: Mother liquor dry substance fraction ($0.0–1.0$)
  - $PU_{ml}$: Mother liquor true purity fraction ($0.0–1.0$)
- **Inverse Form (Mother Liquor Dry Substance from Purity)**:
  $$DS_{ml} = \frac{DS_{mc} \cdot (1 - PU_{mc})}{1 - PU_{ml}}$$
- **Applicability**: Assumes dry substance of pure sucrose crystal $DS_{cs} = 1.00$ and purity $PU_{cs} = 1.00$.
- **Source**: `Theory/Theory.md`, section "Crystal Content".

---

### FORMULA-CP-001: Specific Heat Capacity of Sugar Syrups (Bartens Eq 341/3)
- **Topic**: Syrup & Mother Liquor Thermal Properties
- **Equation**:
  $$C_p = 4.1868 - DS \cdot (0.0297 - 4.6 \times 10^{-3}) + 7.5 \times 10^{-5} \cdot DS \cdot t \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
- **Variables**:
  - $C_p$: Specific heat capacity, $\text{kJ}/(\text{kg}\cdot\text{K})$
  - $DS$: Dry substance, mass % ($0–100$)
  - $t$: Temperature, $^\circ\text{C}$
- **Applicability**: Sugar solutions from $0$ to $90\%$ Brix and $20^\circ\text{C}$ to $120^\circ\text{C}$. For pure water ($DS=0$), returns $4.1868\text{ kJ}/(\text{kg}\cdot\text{K})$.
- **Source**: `Theory/Theory.md`, citing Sugar Technologists Manual (Bartens 8th Ed., Eq. 341/3).

---

### FORMULA-CP-002: Specific Heat Capacity of Sucrose Crystals (Bartens Eq 311/2)
- **Topic**: Sucrose Crystal Thermal Properties
- **Equation**:
  $$C_{p,cryst} = 1.256 + 1.6 \times 10^{-3} \cdot t \quad [\text{kJ}/(\text{kg}\cdot\text{K})]$$
- **Variables**:
  - $C_{p,cryst}$: Specific heat capacity of crystalline sugar, $\text{kJ}/(\text{kg}\cdot\text{K})$
  - $t$: Crystal temperature, $^\circ\text{C}$
- **Source**: `Theory/Theory.md`, citing Sugar Technologists Manual (Bartens 8th Ed., Eq. 311/2).

---

### FORMULA-BPE-001: Boiling Point Elevation (Kadlec, Bretschneider & Dandor 1978 / Bubník-Kadlec 1995)
- **Topic**: Evaporator & Vacuum Pan Boiling Elevation
- **Equation**:
  $$\text{BPE} = f(DS, PU, P_{abs})$$
  $$\text{BPE} = \Delta T_{pure}(DS, P_{abs}) \cdot \left[1 + \beta(PU, DS)\right]$$
- **Variables**:
  - $\text{BPE}$: Boiling point elevation above pure water boiling point at same absolute pressure, $^\circ\text{C}$
  - $DS$: Dry substance percentage ($0–90\%$)
  - $PU$: True purity percentage ($0–100\%$)
  - $P_{abs}$: Operating absolute pressure, $\text{kPa}$
- **Physical Boundary**: Pure water ($DS = 0$) has $\text{BPE} = 0.0^\circ\text{C}$. For standard cane syrup at $65^\circ\text{Brix}$, $\text{BPE} \approx 3.0$–$3.5^\circ\text{C}$.
- **Source**: `Theory/Theory.md`, section "Boiling Point Elevation" (La Sucrerie Belge Vol. 97).

---

## 2. Extraction & Milling Calculations

### FORMULA-MILL-001: Cane Mass Balance
- **Topic**: Mill Tandem Flow Balance
- **Equation**:
  $$M_{cane} + M_{imbibition} = M_{mixed\_juice} + M_{bagasse}$$
- **Variables**:
  - $M_{cane}$: Cane crushing rate, $\text{kg/h}$
  - $M_{imbibition}$: Imbibition water flow rate, $\text{kg/h}$
  - $M_{mixed\_juice}$: Mixed juice mass flow rate, $\text{kg/h}$
  - $M_{bagasse}$: Final bagasse mass flow rate, $\text{kg/h}$
- **Source**: `Examples/Cane_Factory-Milling.md`.

---

### FORMULA-MILL-002: Fiber Balance & Bagasse Production
- **Topic**: Bagasse Quantity Determination
- **Equation**:
  $$M_{bagasse} = \frac{M_{cane} \cdot \text{Fiber}_{cane}}{\text{Fiber}_{bagasse}}$$
- **Variables**:
  - $\text{Fiber}_{cane}$: Fiber fraction in cane (typically $0.12–0.16$)
  - $\text{Fiber}_{bagasse}$: Fiber fraction in bagasse (typically $0.46–0.50$)
- **Assumption**: Zero fiber loss in mixed juice (screened by juice strainer/cush-cush).
- **Source**: `Examples/Cane_Factory-Milling.md`.

---

### FORMULA-MILL-003: Pol Extraction & Milling Loss
- **Topic**: Milling Tandem Efficiency
- **Equations**:
  $$\text{Pol Extraction} = \frac{\text{Pol in Mixed Juice}}{\text{Pol in Cane}} \times 100\%$$
  $$\text{Milling Loss} = \frac{\text{Pol in Bagasse} \cdot 100}{\text{Fiber in Bagasse} \cdot \text{Brix of Absolute Juice}}$$
- **Source**: `Examples/Cane_Factory-Milling.md`.

---

## 3. Evaporation & Heating Calculations

### FORMULA-EVAP-001: Evaporator Mass & Solids Conservation
- **Topic**: Multi-Effect Evaporator Body
- **Equations**:
  $$M_{juice\_in} = M_{syrup\_out} + M_{vapour\_out}$$
  $$M_{juice\_in} \cdot \text{Brix}_{in} = M_{syrup\_out} \cdot \text{Brix}_{out}$$
  $$M_{vapour\_out} = M_{juice\_in} \cdot \left(1 - \frac{\text{Brix}_{in}}{\text{Brix}_{out}}\right)$$
- **Variables**:
  - $M_{juice\_in}$: Inflow juice mass rate, $\text{kg/h}$
  - $M_{syrup\_out}$: Outflow syrup mass rate, $\text{kg/h}$
  - $M_{vapour\_out}$: Evaporated vapour mass rate, $\text{kg/h}$
  - $\text{Brix}_{in}, \text{Brix}_{out}$: Juice in / syrup out dry substance %
- **Source**: `Evaporator/Evaporator_Features.md`.

---

### FORMULA-EVAP-002: Evaporator Calandria Steam Heat Balance
- **Topic**: Steam Demand & Thermal Transfer
- **Equation**:
  $$Q_{process} = M_{juice\_in} \cdot C_{p,in} \cdot (T_{boil} - T_{in}) + M_{vapour\_out} \cdot \Delta h_{vap}$$
  $$Q_{gross} = \frac{Q_{process}}{1 - f_{loss}}$$
  $$M_{steam} = \frac{Q_{gross}}{h_{steam,in} - h_{cond,out}}$$
- **Variables**:
  - $Q_{process}$: Net process thermal requirement, $\text{kJ/h}$
  - $f_{loss}$: Radiation and venting heat loss fraction ($0.01–0.02$)
  - $\Delta h_{vap}$: Latent heat of water vaporization at vapour body pressure, $\text{kJ/kg}$
  - $h_{steam,in}$: Enthalpy of motive steam/vapour, $\text{kJ/kg}$
  - $h_{cond,out}$: Enthalpy of condensate leaving calandria, $\text{kJ/kg}$
- **Source**: `Evaporator/Evaporator_Properties.md`.

---

### FORMULA-HEAT-001: Juice Heater Thermal Duty
- **Topic**: Shell & Tube / Plate Juice Heating
- **Equation**:
  $$Q_{juice} = M_{juice} \cdot C_{p,avg} \cdot (T_{out} - T_{in})$$
  $$M_{steam} = \frac{Q_{juice}}{(1 - f_{loss}) \cdot (h_{vap,in} - h_{cond,out})}$$
- **Variables**:
  - $M_{juice}$: Juice flow, $\text{kg/h}$
  - $C_{p,avg}$: Mean specific heat between $T_{in}$ and $T_{out}$, $\text{kJ}/(\text{kg}\cdot\text{K})$
- **Source**: `Heat_Exchanger/Heat_Exchanger_Properties.md`.

---

## 4. Centrifugal Purging & Separation

### FORMULA-CENT-001: Continuous Centrifugal (2-Output) Purge Model
- **Topic**: Mother Liquor & Wash Purging
- **Governing Equations**:
  $$W_{sugar} = W_{cryst,mc} \cdot (1 - f_{diss}) + W_{ml,sugar} + W_{wash,sugar}$$
  $$W_{green} = W_{ml,green} + W_{wash,green} + W_{cryst,lost}$$
- **Purge Fractions**:
  - $Z_g$: Fraction of massecuite mother liquor purged to green molasses
  - $P_w$: Wash water purge efficiency
- **Source**: `Centrifugal/2-Output_Centrifugal_Evaluation.md`, `Theory/Theory.md`.

---

### FORMULA-CENT-002: Batch Centrifugal (3-Output) Split Model
- **Topic**: Green and Wash Molasses Separation
- **Governing Split**:
  $$W_{green} + W_{wash\_mol} + W_{sugar} = W_{mc} + W_{wash\_water}$$
  - Green molasses: receives bulk of concentrated mother liquor ($Z_g \approx 75–85\%$)
  - Wash molasses: receives washed-off mother liquor, dissolved sugar, and bulk of wash water
- **Source**: `Centrifugal/3-Output_Centrifugal_Evaluation.md`.

---

## 5. Vacuum & Condensing

### FORMULA-COND-001: Barometric Direct Contact Condenser Water Demand
- **Topic**: Pan & Evaporator Vapour Condensing
- **Equation**:
  $$M_{water} = \frac{M_{vap} \cdot (h_{vap} - h_{water,out}) + M_{vap} \cdot f_{nc}}{h_{water,out} - h_{water,in}}$$
- **Variables**:
  - $M_{water}$: Cooling injection water mass rate, $\text{kg/h}$
  - $M_{vap}$: Condensing vapour mass rate, $\text{kg/h}$
  - $h_{water,in}, h_{water,out}$: Water enthalpy in / out (tail pipe), $\text{kJ/kg}$
- **Source**: `Contact_Condenser/Contact_Condenser_Properties.md`.
