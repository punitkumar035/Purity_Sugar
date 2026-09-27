# Purity for Sugar — Master Rulebook v5.0
### Covers Phase 01 (LOCKED) + Phase 02 (Python Engine — to build)

> **v5.0 supersedes all previous versions.**
> Every rule traces to a specific documentation file in sugars.zip or
> to a verified Phase 01 implementation decision.
>
> **Phase 01 sections are LOCKED. Do not change them.**
> **Phase 02 sections define exactly what to build next.**

---

## PART A — PHASE 01: VISIO FOUNDATION (LOCKED ✅)

---

## A1. Platform Architecture

| Layer | Technology | Status |
|-------|-----------|--------|
| Diagram canvas | Microsoft Visio — saved as `.vsdm` | LOCKED |
| Stencils | 10 × Sugars `Sug_*.vss` files | LOCKED |
| `ThisDocument.bas` | Event handlers in Visio Objects | LOCKED |
| `StationDialogManager.bas` | Field specs for 24 station types | LOCKED |
| `PurityForSugar.bas` | Main VBA module | LOCKED |
| Python engine | FastAPI on `localhost:8765` | Phase 02/03 |

**File must be `.vsdm`** (Visio Macro-Enabled Drawing). Events do NOT fire from `.vsdx`.

---

## A2. Shape Colour States (LOCKED)
*Source: Program_Overview.htm, Grouped_Stations.htm*

| State | Colour | Trigger |
|-------|--------|---------|
| **RED** `RGB(220,0,0)` | Shape dropped on canvas — awaiting number |
| **BLUE** `RGB(0,100,180)` | Station number assigned |
| **YELLOW** `RGB(255,200,0)` | Properties window OK clicked — data saved |

**Exact quote:** *"The station turns yellow to indicate that data for the station was entered after clicking on the OK button."* — Program_Overview.htm

- Green applies ONLY to the Full Balance ribbon icon (balanced = green, unbalanced = red)
- There is NO green station state
- `RGB()` must NEVER appear inside a `Const` declaration (VBA limitation §A8.4)
- Colours are applied via inline strings: `Shape.CellsU("FillForegnd").FormulaU = "RGB(220,0,0)"`

---

## A3. Shape Drop Behaviour (LOCKED)
*Source: Grouped_Stations.htm, Program_Overview.htm*

```
1. User drops shape from stencil onto canvas
2. IMMEDIATELY: shape turns RED
3. InputBox appears: "Assign Station Number (1–9999)"
4. Validation loop:
   - blank          → warn, loop
   - non-numeric    → warn, loop
   - out of range   → warn, loop
   - duplicate      → warn, loop
   - cancel (StrPtr=0) → DELETE shape, exit
5. Valid number entered → shape turns BLUE, shape.Text = number
6. StationNumber and Type stored in Shape Data
```

---

## A4. Station Numbering Rules (LOCKED)
*Source: Flow_Diagram.htm, Program_Operation.htm*

- Valid range: **1 to 9999** inclusive
- **Unique** across ALL pages
- Station 0 reserved: `StationFromNumber=0` = external flow; `StationToNumber=0` = flow exits model
- **Lower numbers solved FIRST** — this is the calculation sequence
- Recommended spacing: **10 between unrelated stations**; **1 within groups**
- Number in **direction of material flow** for maximum convergence efficiency
- Exception: when required flows propagate backwards, number in required-flow direction
- Exception: evaporator may be numbered last so all vapor loads are known first

---

## A5. Double-Click Behaviour (LOCKED)
*Source: Program_Overview.htm*

- **Station shape** → `OpenStationProperties()` → InputBox sequence for all fields → shape turns **YELLOW**
- **Flow connector** → `ShowFlowProperties()` → MsgBox showing all calculated values
- If shape has no StationNumber → error message, do not open Properties

---

## A6. 15-Component Flow Stream Model (LOCKED)
*Source: External_Flows.htm, Theory.htm*

All values are weight fractions (0–1). Sum of all liquid + solid + gas fractions ≤ 1.

| # | Phase | Name | Shape Data Key |
|---|-------|------|----------------|
| 1 | Liquid | Water | `Water` |
| 2 | Liquid | Dissolved Sucrose | `DissolvedSucrose` |
| 3 | Liquid | Non-Sucrose #1 | `NonSucrose1` |
| 4 | Liquid | Non-Sucrose #2 | `NonSucrose2` |
| 5 | Liquid | Component #5 (ethanol etc.) | `Component5` |
| 6 | Solid | Sucrose Crystals | `SucrosecrystALS` |
| 7 | Solid | Fiber / ISNS | `Fiber` |
| 8 | Solid | CaO | `CaO` |
| 9 | Solid | CaCO₃ | `CaCO3` |
| 10 | Solid | Component #10 | `Component10` |
| 11 | Gas | Water Vapor | `WaterVapor` |
| 12 | Gas | CO₂ | `CO2` |
| 13 | Gas | NH₃ | `NH3` |
| 14 | Gas | Non-Condensable | `NonCondensable` |
| 15 | Gas | Component #15 | `Component15` |

**Derived quantities** (calculated, never entered as fractions):
```
TDM    = 1 - Water - WaterVapor
DS     = TDM  (same as TDM when no ISNS, i.e., DS = 1 - Water - WaterVapor)
Purity = (DissolvedSucrose + SucrosecrystALS) / DS
NSW    = NonSucrose1 / Water           [when Water > 0]
Sugar% = (DissolvedSucrose + SucrosecrystALS) × 100
ISNS%  = Fiber × 100
Gas%   = (WaterVapor + CO2 + NH3 + NonCondensable) × 100
```

**Note:** Air has NO component slot. The 4 gas components are: Water Vapor, CO₂, NH₃, Non-Condensable only.

---

## A7. Required Flows (LOCKED)
*Source: Pan_Features.htm, Blender_Features.htm, Contact_Condenser_Features.htm, Melter_Features.htm*

**Always required (quantity calculated by solver, user cannot specify):**
- Pan steam input (port 1) — ALWAYS
- Blender blend input (port 1) — ALWAYS
- Contact condenser cold water (port 1) — ALWAYS
- Melter heating input (port 10) — ALWAYS when connected AND temperature specified

**Cannot be required (solver error/warning if required):**
- Evaporator vapor out
- Evaporator condensate out
- Pan vapor out
- Pan condensate out
- Dryer vapor out

**Conditionally required** (when specific condition met):
- Evaporator steam in → when Total Solids (%) specified for any effect
- Melter dilution (port 9) → when "Hold TDM at" specified
- Tank dilution (port 9) → when "Hold TDM at" specified
- Heat exchanger port 1 → when Temperature Out/Rise/Approach + "Port 1 Required" checked
- Turbine steam in → when Power Output > 0
- Turbo Alternator steam in → when Electrical Power Output > 0

---

## A8. Pressure Rules (LOCKED)
*Source: Melter_Features.htm, Receiver_Features.htm, Centrifugal_Features.htm*

**Always atmospheric pressure output:**
- Melter (process flow out)
- Tank (process flow out)
- Centrifugal (ALL outputs: green, sugar, wash)
- Contact condenser (output)

**Receiver output pressure = MINIMUM of all input pressures.**
External flows with quantity = 0 are NOT considered for minimum.

**Pressure feedback:** Propagates backward from Receiver → Flash Tank / Compressor / Thermocompressor.
If feedback flow exits model → pressure = atmospheric.

---

## A9. Crystal Behaviour per Station (LOCKED)
*Source: Respective *_Features.htm files*

| Station | Crystal rule |
|---------|-------------|
| Pan | GROW (from DS, Ss, temperature) |
| Crystallizer | GROW (cooling reduces Ss toward 1.0) |
| Centrifugal | Undersaturated out → DISSOLVE to Ss=1; supersaturated → unchanged |
| Melter | DISSOLVE to Ss=1; never grow |
| Tank | DISSOLVE to Ss=1; never grow |
| Blender | May DISSOLVE; never grow |
| Heat Exchanger | If undersaturated after heating → DISSOLVE to Ss=1 |
| Injection Heater | Same as Heat Exchanger |
| Evaporator | Count MAINTAINED (no growth, no dissolution) |
| Cooler | NO growth; flow may become supersaturated |
| Flash Tank | NO growth; flow may become supersaturated |
| Receiver | NO change (no growth, no dissolution) |
| Dryer | GROWTH if supersaturated mother liquor on crystal surface |
| Pump, Pressure Reducer | No change |
| Separator/Filter | Proportional split; no change |

---

## A10. Colour Calculation Rules (LOCKED)
*Source: Separator_Filter_Features.htm, Centrifugal_Evaluations.htm, Reactor_Features.htm*

- Colour is carried by: Sucrose, Invert (N.S. #2), Ash (N.S. #1 portion), N.S. #1
- N.S. #1 carries all miscellaneous colour agents
- Separator Color entry: 100% = normal split; <100% = more colour to output 2. Applied to N.S. #1 only.
- Cannot remove colour from pure sucrose or N.S. #2
- Reactor ColorChange: applied to N.S. #1 only; if N.S. #1 = 0 → no effect
- Centrifugal: colour calculated from proportions of mother liquor + crystals + wash in each output
- Evaporator, Pan, Crystallizer, Melter, Tank all have `ColorRise` (% or absolute CU)
- Colour units must be consistent throughout entire model

---

## A11. Solubility Coefficient Propagation (LOCKED)
*Source: Separator_Filter_Features.htm, Blender_Features.htm, Receiver_Features.htm*

| Station | Rule |
|---------|------|
| Separator | Same as input (unless diluent has different coefficients → weight-weighted avg) |
| Blender | Weight-weighted average if primary and blend differ |
| Receiver | Weight-weighted average of all inputs if they differ |
| Centrifugal | Weight-weighted average from mother liquor + wash composition in each output |
| Reactor | Can explicitly SET new coefficients (even with NO reaction) |
| Pan | New a,b,c overrides if entered; otherwise inherits from syrup input |
| Crystallizer | New a,b,c overrides if entered; otherwise inherits from input |
| Distributor | All outputs identical to input |

---

## A12. API Contract — VBA ↔ Python (LOCKED)
*Source: §29 of previous rulebook*

### A12.1 Endpoints (Python must implement all)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | `{"status":"running","version":"x.y"}` |
| POST | `/solve` | Full balance (or single pass if `single_pass=true`) |
| POST | `/validate` | Pre-check without solving |
| POST | `/export/excel` | Returns base64-encoded xlsx |
| GET | `/supersaturation` | Calc Ss from `?ds=&purity=&temp=&a=&b=&c=` |

### A12.2 Request JSON (schema_version "1.0")

```json
{
  "schema_version": "1.0",
  "model_id": "string",
  "model_name": "string",
  "units": "SI",
  "sugar_type": "cane",
  "convergence_tolerance": 0.0001,
  "max_iterations": 150,
  "atmospheric_pressure_kpa": 101.325,
  "solubility_mode": "vavrinecz",
  "single_pass": false,
  "stations": [ { ...station object... } ],
  "flows":    [ { ...flow object... } ]
}
```

**Station object:**
```json
{
  "id": "visio_shape_id",
  "page": "page_name",
  "station_number": 100,
  "type": "evaporator",
  "name": "1st Effect",
  "equipment_id": "E-101",
  "master_name": "Robert Evaporator",
  "properties": { ...type-specific fields... }
}
```

**Flow object:**
```json
{
  "id": "visio_shape_id",
  "origin_station": 90,
  "dest_station": 100,
  "is_external": false,
  "is_required": false,
  "initial_state": {
    "mass_flow_kgh": 0.0,
    "temperature_c": 0.0,
    "pressure_kpa": 0.0,
    "ds_pct": 0.0,
    "purity_pct": 0.0,
    "crystal_pct": 0.0,
    "isns_pct": 0.0,
    "gas_pct": 0.0,
    "water": 0.0,
    "dissolved_sucrose": 0.0,
    "non_sucrose_1": 0.0,
    "non_sucrose_2": 0.0,
    "sucrose_crystals": 0.0,
    "fiber_isns": 0.0,
    "cao": 0.0,
    "caco3": 0.0,
    "water_vapor": 0.0,
    "co2": 0.0,
    "nh3": 0.0,
    "color_icu": 0.0,
    "sol_coef_a": 0.0,
    "sol_coef_b": 0.0,
    "sol_coef_c": 0.0
  }
}
```

### A12.3 Response JSON

**HTTP 200 for ALL solver outcomes. Only HTTP 5xx for genuine crashes.**

```json
{
  "status": "converged",
  "iterations": 12,
  "final_error": 0.0000034,
  "error_message": "",
  "stations": [ { ...station result... } ],
  "flows": [ { ...flow result... } ]
}
```

**Flow result fields** (written back to Visio Shape Data by VBA):
```json
{
  "id": "visio_shape_id",
  "mass_flow_kgh": 30000.0,
  "temperature_c": 73.0,
  "pressure_kpa": 101.3,
  "tdm_pct": 82.3,
  "sugar_pct": 63.7,
  "ds_pct": 82.3,
  "purity_pct": 77.0,
  "crystal_pct": 0.0,
  "isns_pct": 0.0,
  "gas_pct": 0.0,
  "color_icu": 4200.0,
  "enthalpy_kjkg": 321.5,
  "fluid_type": "syrup",
  "water": 0.177,
  "dissolved_sucrose": 0.617,
  "non_sucrose_1": 0.184,
  "non_sucrose_2": 0.0,
  "sucrose_crystals": 0.0,
  "fiber_isns": 0.0,
  "cao": 0.0,
  "caco3": 0.0,
  "water_vapor": 0.0,
  "co2": 0.0,
  "nh3": 0.0,
  "sol_coef_a": 0.178,
  "sol_coef_b": 0.82,
  "sol_coef_c": -2.1
}
```

### A12.4 VBA Colour Coding After Balance

VBA colours flow connectors by DS% using **inline RGB strings** (not constants):

| DS% | Colour | Inline string |
|-----|--------|---------------|
| No DS (steam/vapor) | Gray | `"RGB(180,178,169)"` |
| < 10% | Blue | `"RGB(59,139,212)"` |
| 10–30% | Green | `"RGB(99,153,34)"` |
| 30–60% | Amber | `"RGB(186,117,23)"` |
| 60–75% | Dark amber | `"RGB(133,79,11)"` |
| > 75% | Coral | `"RGB(153,60,29)"` |

---

## A13. VBA Implementation Rules (LOCKED)
*Source: §28 of previous rulebook*

1. **`Document_ShapeAdded`** and **`Document_ShapeDoubleClicked`** MUST be in `ThisDocument` under Visio Objects — NOT in a standard module
2. **`.vsdm` format** required — macros do not fire from `.vsdx`
3. **No `RGB()` in `Const` declarations** — VBA does not support function calls in Const
4. **No UserForms** — Visio VBA cannot create UserForms programmatically; use InputBox sequences
5. **Cancel = StrPtr(val) = 0** — never use `val = ""` to detect cancel (user may click OK with empty field)
6. **Max 24 line continuations** per statement — VBA compiler hard limit
7. **Shape Data prefix** = `"Prop."` — all rows stored as `Prop.<RowName>`
8. **`AddNamedRow`** must be called before setting a Shape Data value that doesn't yet exist
9. HTTP via `MSXML2.ServerXMLHTTP` only
10. Results stored in `doc.Description` (Phase 01 approach)

---

## PART B — PHASE 02: PYTHON THERMODYNAMICS ENGINE

---

## B1. Engine Overview

Phase 02 builds the Python thermodynamics library that Phase 03 will use. It is NOT the HTTP server (that is Phase 03). Phase 02 delivers only the calculation modules — each independently testable.

### B1.1 Directory structure

```
engine/
├── fluids.py          CoolProp integration (WATER.FLD, ETHANOL.FLD, HMX.BNC)
├── solubility.py      Vavrinecz, Wagnerowski, Van Hook equations
├── heat_content.py    Specific heat capacity for all phases
├── bpe.py             Kadlec-Bretschneider-Dandor boiling point elevation
├── crystals.py        Crystal content — forward and inverse
├── enthalpy.py        Total enthalpy calculator for a flow stream
├── density.py         Specific weight / density for syrups and massecuites
└── tests/
    ├── test_solubility.py
    ├── test_crystals.py
    ├── test_bpe.py
    ├── test_heat_content.py
    └── test_enthalpy.py
```

### B1.2 Python version and dependencies

```
Python 3.10+
CoolProp >= 6.6.0
numpy >= 1.24
pytest >= 7.0
```

Install: `pip install CoolProp numpy pytest`

---

## B2. Fluid Files (CoolProp)
*Source: §9 of RULES_v4, Acknowledgement.htm*

Three NIST REFPROP-format files required in `engine/fluids/`:

| File | Description | Source |
|------|-------------|--------|
| `WATER.FLD` | IAPWS-95 Helmholtz EOS | NIST via CoolProp |
| `ETHANOL.FLD` | Dillon & Penoncello 2004 | NIST via CoolProp |
| `HMX.BNC` | KW8 binary mixing rules | NIST via CoolProp |

### B2.1 `engine/fluids.py` — Required interface

```python
def init_fluids(fluids_dir: str) -> None:
    """Call once at startup. Fails loudly if any file is missing."""

def water_enthalpy_kJkg(temp_c: float, pressure_kpa: float,
                         quality: float = 1.0) -> float:
    """Specific enthalpy of water/steam.
    quality=1.0 → saturated steam; quality=0.0 → saturated liquid;
    quality in (0,1) → wet steam; quality not used if T and P define superheated.
    """

def water_sat_temp_c(pressure_kpa: float) -> float:
    """Saturation temperature of water at given pressure."""

def water_sat_pressure_kpa(temp_c: float) -> float:
    """Saturation pressure of water at given temperature."""

def water_latent_heat_kJkg(temp_c: float) -> float:
    """Latent heat of vaporisation of water at given temperature."""

def water_cp_kJkgK(temp_c: float, pressure_kpa: float) -> float:
    """Specific heat of water at given state."""

def steam_is_superheated(temp_c: float, pressure_kpa: float) -> bool:
    """True if T > saturation T at this pressure."""

def steam_superheat_K(temp_c: float, pressure_kpa: float) -> float:
    """Degrees of superheat (0 if not superheated)."""

def ethanol_water_bubble_temp_c(ethanol_mole_frac: float,
                                 pressure_kpa: float) -> float:
    """Bubble point of ethanol-water mixture via HMX.BNC."""
```

### B2.2 Rules

- **NEVER use IF-97 approximations or pyXSteam.** All steam/water properties MUST come from CoolProp + WATER.FLD.
- CoolProp state: `CP.PropsSI('H','T',T_K,'P',P_Pa,'Water')` → enthalpy in J/kg → divide by 1000 for kJ/kg
- Temperature always converted to Kelvin before CoolProp calls: `T_K = temp_c + 273.15`
- Pressure always converted to Pa before CoolProp calls: `P_Pa = pressure_kpa * 1000`
- If WATER.FLD missing → raise `FileNotFoundError` with clear message
- Ethanol VLE uses KW8 mixing rule from HMX.BNC via `CP.set_config_string(CP.ALTERNATIVE_REFPROP_HMX_BNC_PATH, path)`

---

## B3. Sucrose Solubility
*Source: Theory.htm, Pan_Properties.htm, Supersaturation.htm*

### B3.1 Vavrinecz equation — solubility of pure sucrose (ICUMSA official)

```
S(t) = 64.447 + 0.08222·t + 1.6169e-3·t² − 1.558e-6·t³ − 4.63e-8·t⁴
```
where:
- `S` = weight percent of sucrose in solution at saturation
- `t` = temperature in °C

### B3.2 Saturation coefficient — Vavrinecz function (used when c ≠ 0)

```
Sc = a·NSW + b + (1 − b)·exp(c·NSW)
```
where:
- `NSW` = non-sucrose to water ratio (weight basis)
- `a`, `b`, `c` = coefficients depending on impurity type
- `e` = natural log base (2.71828...)

**Reference coefficient values from documentation:**
| Source | a | b | c |
|--------|---|---|---|
| Beet (Grut) | 0.178 | 0.82 | −2.1 |
| Beet (Polish) | 0.27 | 0.71 | −1.4 |
| Cane (typical) | 0.04 | 0.71 | −2.1 |

Saturation coefficient is **independent of temperature.**

### B3.3 Saturation coefficient — Wagnerowski equation (used when c = 0)

```
Sc = a·NSW + b
```
(typically `Sc = 1 + 0.036·NSW` when default `a = 0.036, b = 1.0`)

**CRITICAL CONSTRAINT:** Valid ONLY for NSW between **1.6 and 3.5** (inclusive).
- If NSW < 1.6 → DO NOT use Wagnerowski; use Vavrinecz instead
- If NSW > 3.5 → emit WARNING `NSW_OUT_OF_RANGE` but continue with Wagnerowski

**Selection rule:** Use Wagnerowski if and only if `c == 0.0` in the flow's solubility coefficients. Otherwise use Vavrinecz.

### B3.4 NSW calculations

For a syrup (no crystals):
```
NSW = NonSucrose1 / Water                [when Water > 0]
```

For a massecuite (contains crystals), NSW of the **mother liquor**:
```
NSW = (1 − PUmc) · DSmc / (1 − DSmc)
```
where DSmc and PUmc are **massecuite** DS and purity (fractions, not %).

Equivalently:
```
NSW = NonSucrose1_ml / Water_ml
```
where `_ml` refers to the mother liquor portion only.

### B3.5 Supersaturation — Van Hook (ICUMSA official)

```
Ss = (sucrose/water)_sample / (sucrose/water)_sat
```

Sucrose-to-water ratio at saturation (Sugar's Help Book Theory.md):
```
suc_water_sat = Sc · S(t) / (100 − S(t))
```

Sucrose-to-water ratio of a syrup:
```
suc_water = DissolvedSucrose / Water       [for plain syrup]
```

For massecuite mother liquor:
```
suc_water_ml = DissolvedSucrose_ml / Water_ml
```

Therefore:
```
Ss = suc_water_ml / suc_water_sat
```

All values in weight fractions. DS and purity in fractions (0–1), not %.

### B3.6 `engine/solubility.py` — Required functions

```python
def sucrose_saturation_pct(temp_c: float) -> float:
    """Vavrinecz: weight% sucrose in saturated solution. Returns 0-100."""

def saturation_coefficient(nsw: float, a: float, b: float, c: float) -> float:
    """Vavrinecz (c≠0) or Wagnerowski (c=0). NSW must be >= 0."""

def nsw_from_syrup(non_sucrose_1: float, water: float) -> float:
    """NSW = NS1 / water. Returns 0 if water == 0."""

def nsw_from_massecuite(ds_mc: float, purity_mc: float) -> float:
    """NSW from massecuite DS and purity (both fractions 0-1)."""

def supersaturation(ds_ml: float, purity_ml: float,
                    temp_c: float,
                    a: float, b: float, c: float) -> float:
    """Ss from mother liquor DS, purity (fractions), temperature, and sol coefficients."""

def sucrose_water_at_saturation(temp_c: float,
                                 a: float, b: float, c: float,
                                 nsw: float) -> float:
    """suc/water ratio at saturation for given T and impurity composition."""
```

---

## B4. Crystal Content
*Source: Theory.htm (Crystal Content section)*

### B4.1 Forward calculation — DS, PU, T, Ss known → % crystals

Given massecuite DS (`DSmc`), purity (`PUmc`), temperature (`t`), and supersaturation (`Ss`):

1. Calculate `S = sucrose_saturation_pct(t)` (wt%)
2. Calculate `NSW = nsw_from_massecuite(DSmc, PUmc)`
3. Calculate `Sc = saturation_coefficient(NSW, a, b, c)`
4. `suc_water_sat = S·Sc / (100 − S·Sc)`
5. Mother liquor sucrose-to-water: `suc_water_ml = Ss · suc_water_sat`
6. From suc/water: `DSml = suc_water_ml / (1 + suc_water_ml)` for pure sucrose in water, but with impurities:
   ```
   PUml · DSml / Water_ml = suc_water_ml
   ```
   Use conservation equations (2 equations, 2 unknowns DSml and PUml):
   ```
   Equation 1 (from Ss):
       DSml · PUml / (1 - DSml) = Ss · S·Sc / (100 - S·Sc)

   Equation 2 (from mass balance — NSW is same in mother liquor and massecuite):
       (1 - PUml) · DSml / (1 - DSml) = NSW
   ```
   Solve simultaneously for DSml and PUml.

7. Crystal percentage:
   ```
   Crystals = (DSmc − DSml) / (1 − DSml)    [fractions, DScs=PUcs=1.0]
   ```

### B4.2 Inverse calculation — % crystals known → DSml, PUml

Given massecuite DS (`DSmc`), purity (`PUmc`), and crystal fraction (`Cry`):

```
DSml  = (DSmc − Cry) / (1 − Cry)
PUml  = (PUmc · DSmc − Cry) / (DSmc − Cry)
```

Both DScs and PUcs assumed = 1.0 (pure sucrose crystal, 100% solid).

### B4.3 `engine/crystals.py` — Required functions

```python
def crystals_forward(ds_mc: float, pu_mc: float, temp_c: float,
                     ss: float,
                     a: float, b: float, c: float) -> dict:
    """
    Input: massecuite DS, purity (fractions), temperature (C),
           supersaturation, solubility coefficients.
    Output: dict with keys:
      crystal_frac  - crystal weight fraction in massecuite
      ds_ml         - mother liquor DS (fraction)
      pu_ml         - mother liquor purity (fraction)
      nsw           - non-sucrose to water ratio
      ss_calc       - calculated supersaturation (should equal input Ss)
    """

def crystals_inverse(ds_mc: float, pu_mc: float,
                     crystal_frac: float) -> dict:
    """
    Input: massecuite DS, purity (fractions), crystal fraction.
    Output: dict with keys:
      ds_ml   - mother liquor DS (fraction)
      pu_ml   - mother liquor purity (fraction)
    """

def massecuite_crystal_content(ds_mc: float, pu_mc: float,
                                temp_c: float, ss: float,
                                a: float, b: float, c: float) -> float:
    """Convenience: returns crystal weight fraction only."""
```

### B4.4 Validation test case (from Theory.htm example)

Given:
- `DSmc = 0.9300`, `PUmc = 0.8644`, `T = 81°C`, `Ss = 1.100`
- Grut coefficients: a=0.178, b=0.82, c=−2.1

Expected results:
- Crystals = **0.4744** (47.44% by weight)
- `DSml = 0.8668` (86.68%)
- `PUml = 0.7232` (72.32%)

**This test MUST pass before Phase 03 begins.**

---

## B5. Specific Heat Capacity
*Source: Theory.htm (Heat Content section)*

### B5.1 Syrup Cp — Sugar Technologists Manual 8th ed, eq 341/3

```
Cp_syrup = (4.187 − 2.884·DS) + (0.00604 − 0.00382·DS)·t     [kJ/kg·K]
```
where:
- `DS` = dry substance fraction (0–1), NOT percentage
- `t` = temperature in °C

### B5.2 Sucrose crystal Cp — Sugar Technologists Manual 8th ed, eq 311/2

```
Cp_crystal = 1.2473 + 0.002096·t − 3.9×10⁻⁶·t²     [kJ/kg·K]
```

### B5.3 Limestone and lime Cp — Boynton curve fits

From Boynton, *Chemistry and Technology of Lime and Limestone*:

```
Cp_CaCO3 = 0.819 + 0.000234·t − 20700/T²     [kJ/kg·K, T = t+273.15 K]
Cp_CaO   = 0.753 + 0.000117·t − 11700/T²     [kJ/kg·K]
Cp_Ca(OH)2 ≈ 1.30    [kJ/kg·K, approximately constant in range 0-200°C]
```

### B5.4 Beet marc Cp — Vukov

From Vukov, *Physics and Chemistry of Sugar Beet in Sugar Manufacture*:
```
Cp_marc = 1.25 + 0.0034·moisture_fraction     [kJ/kg·K, approximate]
```

### B5.5 CO₂ and NH₃ Cp — Chemical Engineering, Aug 16 1976

```
Cp_CO2 = A + B·T + C·T² + D·T³     [J/mol·K, T in K]
  A=19.795, B=0.07344, C=-5.602e-5, D=1.715e-8   (CO₂)

Cp_NH3 = A + B·T + C·T²
  A=27.568, B=0.02563, C=9.890e-6   (NH₃)
```
Convert J/mol·K to kJ/kg·K by dividing by 1000 and by molecular weight.
- CO₂ MW = 44.01 g/mol
- NH₃ MW = 17.03 g/mol

### B5.6 Water vapor Cp — from CoolProp (not approximation)

Water vapor Cp comes from CoolProp + WATER.FLD at the actual T and P state.

### B5.7 `engine/heat_content.py` — Required functions

```python
def cp_syrup(ds_frac: float, temp_c: float) -> float:
    """Cp of syrup kJ/kg·K. ds_frac in 0-1."""

def cp_sucrose_crystal(temp_c: float) -> float:
    """Cp of sucrose crystal kJ/kg·K."""

def cp_water_liquid(temp_c: float, pressure_kpa: float) -> float:
    """Cp of liquid water kJ/kg·K via CoolProp."""

def cp_water_vapor(temp_c: float, pressure_kpa: float) -> float:
    """Cp of water vapor kJ/kg·K via CoolProp (includes superheat)."""

def cp_cao(temp_c: float) -> float:
    """Cp of CaO kJ/kg·K via Boynton."""

def cp_caco3(temp_c: float) -> float:
    """Cp of CaCO3 kJ/kg·K via Boynton."""

def cp_co2_gas(temp_c: float) -> float:
    """Cp of CO2 gas kJ/kg·K."""

def cp_nh3_gas(temp_c: float) -> float:
    """Cp of NH3 gas kJ/kg·K."""

def cp_fiber(temp_c: float, moisture_frac: float) -> float:
    """Cp of beet marc/fiber kJ/kg·K via Vukov."""
```

---

## B6. Boiling Point Elevation
*Source: Theory.htm (Boiling Point Elevation section)*

### B6.1 Kadlec, Bretschneider and Dandor (1978)

Published in *La Sucrerie Belge*, Vol. 97, November 1978, paper "Boiling Point Elevation of Sugar Solutions."

The BPE depends on **dry substance**, **purity**, and **ambient pressure**.

The exact polynomial from the paper (as implemented in Sugars):
```
BPE = f(DS, Purity, P_kPa)     [°C]
```

**Implementation note:** The exact coefficient values of the KBD equation are not printed in the documentation. The documentation only states that the equation *takes into consideration dry substance, purity and ambient pressure.* Implement using the following approach derived from the paper:

```
BPE ≈ K_B(T_sat) · m_sucrose · (1 + F_impurity(NSW))
```

Where:
- `K_B(T_sat)` = ebullioscopic constant of water at saturation temperature
- `m_sucrose` = molality of sucrose solution
- `F_impurity` = impurity correction based on NSW

**Practical implementation** (valid for sugar solutions in the range 50–90% DS, 50–98% purity, 10–200 kPa):

```python
def bpe_celsius(ds_frac: float, purity_frac: float,
                pressure_kpa: float) -> float:
    """
    Boiling point elevation using KBD 1978.
    ds_frac: dry substance (0-1)
    purity_frac: purity (0-1)
    pressure_kpa: absolute pressure
    Returns BPE in °C (always ≥ 0)
    """
```

**Reference values for validation** (from Sugars example data):
- DS=82.3%, Purity=77%, T_sat≈73°C (at ~34 kPa) → BPE ≈ 1.5–2.0°C
- DS=93%, Purity=86%, T_sat≈100°C (at 101 kPa) → BPE ≈ 2.5–3.5°C

The boiling temperature of the liquid:
```
T_boil = T_sat(P) + BPE
```

The vapor leaving the evaporator/pan exits at `T_sat(P)`, NOT at `T_boil`.

### B6.2 BPE Factor

The `BPEFactor` property on the Evaporator allows a multiplier adjustment:
```
BPE_effective = BPE × BPEFactor
```
If `BPEFactor` is not entered, it defaults to 1.0.

### B6.3 `engine/bpe.py` — Required functions

```python
def bpe_celsius(ds_frac: float, purity_frac: float,
                pressure_kpa: float) -> float:
    """BPE of sugar solution in °C."""

def boiling_temp_c(ds_frac: float, purity_frac: float,
                   pressure_kpa: float, bpe_factor: float = 1.0) -> float:
    """T_boil = T_sat(P) + BPE × bpe_factor."""

def vapor_sat_temp_from_boiling(boiling_temp_c: float,
                                 ds_frac: float, purity_frac: float,
                                 bpe_factor: float = 1.0) -> float:
    """
    Inverse: given known boiling temp and solution properties,
    find vapor saturation temperature (iterative).
    T_sat = T_boil - BPE(ds, pu, P_sat(T_sat))
    """

def pressure_from_vapor_temp(vapor_sat_temp_c: float) -> float:
    """Vapor saturation pressure from saturation temperature via CoolProp."""
```

---

## B7. Total Enthalpy of a Flow Stream
*Source: Theory.htm (Heat Content section)*

The total enthalpy of a flow stream is calculated by summing contributions from every component:

```
H_total = Σ (mass_i × Cp_i × T) + Σ (steam mass × latent_heat)
```

More precisely, for a flow stream with known fractions and temperature T:

```
H = (water_frac × h_water(T,P)) +
    (water_vapor_frac × h_steam(T,P)) +
    ((dissolved_sucrose + non_sucrose_1 + non_sucrose_2) × Cp_syrup(DS,T) × T) +
    (sucrose_crystals_frac × (Cp_crystal(T) × T + heat_of_crystallization)) +
    (fiber_frac × Cp_fiber(T) × T) +
    (cao_frac × Cp_cao(T) × T) +
    (caco3_frac × Cp_caco3(T) × T) +
    (co2_frac × Cp_co2(T) × T) +
    (nh3_frac × Cp_nh3(T) × T)
```

Reference temperature = 0°C.

**Heat of crystallization / dissolution of sucrose:**
- Crystallization (dissolve → crystal): ΔH ≈ +18.8 kJ/mol = +54.9 kJ/kg sucrose
- This heat is released when sucrose crystallises (exothermic) and must be accounted for in pan energy balance

### B7.1 `engine/enthalpy.py` — Required functions

```python
def flow_enthalpy_kJkg(fractions: dict, temp_c: float,
                        pressure_kpa: float) -> float:
    """
    Total specific enthalpy of a flow stream.
    fractions: dict with keys matching §A6 component names (weight fractions)
    temp_c: temperature
    pressure_kpa: pressure
    Returns kJ/kg of total flow.
    """

def heat_of_crystallization_kJkg() -> float:
    """Returns +54.9 kJ/kg (positive = heat released when sucrose crystallises)."""

def heat_of_dissolution_kJkg() -> float:
    """Returns -54.9 kJ/kg (negative = heat absorbed when crystals dissolve)."""
```

---

## B8. Specific Weight (Density)
*Source: Introduction.htm — "density of syrups, sugar crystals, insoluble solids, and gases"*

Required for volume flow calculations and centrifugal evaluation:

### B8.1 Syrup density

```
ρ_syrup = f(DS, T)     [kg/m³]
```

Standard approximation used in sugar industry:
```
ρ_syrup = 1000 + 349.2·DS + 0.0 (temp correction)
```

More accurate (Bubník-Kadlec):
```
ρ_syrup(DS, T) = 1000 / (w_water/ρ_water(T) + w_sucrose/ρ_sucrose(T))
```
where `ρ_sucrose ≈ 1580 kg/m³` (slight T dependence) and `ρ_water` from CoolProp.

### B8.2 `engine/density.py` — Required functions

```python
def syrup_density_kgm3(ds_frac: float, temp_c: float) -> float:
    """Density of sugar syrup kgm3."""

def massecuite_density_kgm3(ds_mc: float, pu_mc: float,
                              crystal_frac: float, temp_c: float) -> float:
    """Density of massecuite kgm3."""
```

---

## B9. Conservation Laws Enforced at Every Station
*Source: Theory.htm*

The Python solver (Phase 03) will use Phase 02 modules to enforce these laws at each station. Phase 02 must provide the arithmetic primitives.

### B9.1 Total mass

```
Σ mass_in = Σ mass_out     (within tolerance < 1e-6 relative)
```

### B9.2 Each of the 15 components

```
Σ (mass_in × component_fraction_in) = Σ (mass_out × component_fraction_out)
```
Except where the station explicitly transforms components (Reactor, phase changes, crystallization).

### B9.3 Energy

```
Σ H_in = Σ H_out + Q_loss + W_mechanical
```
where:
- `Q_loss` = heat loss specified as % of heat transferred
- `W_mechanical` = work extracted (turbine, turbo alternator) or added (pump, compressor)

---

## B10. Per-Station Solver Logic
*Source: Respective *_Features.htm files*

These are the calculation rules Phase 03 will implement, but Phase 02 modules must support them.

### B10.1 RECEIVER
```
mass_out = Σ mass_in
component_frac_out[i] = Σ (mass_in_j × frac_in_j[i]) / mass_out   # mass-weighted average
T_out = from energy balance: H_out = Σ H_in (no heat loss)
P_out = min(P_in_j)   [for all j where P_in_j > 0]
crystal_frac_out = crystal_frac_in (weighted average) — NO change
```

### B10.2 BLENDER
Same as Receiver for mass/component/energy balance.
Additional: P_out = min(P_primary, P_blend); crystals may dissolve (not grow) per §A9.

### B10.3 DISTRIBUTOR
Each output has same properties as input. Only mass flow splits.
Overflow → lowest-numbered unspecified output port.
Cannot mix % mode and required flows.

### B10.4 EVAPORATOR
```
Energy balance:
  Q_steam × (1 - heat_loss_frac) = Q_evaporation + Q_juice_heating
  Q_evaporation = m_vapor × h_fg(P_vapor)
  Q_juice_heating = m_juice × Cp_syrup × (T_out - T_in)

Mass balance:
  m_juice_in = m_juice_out + m_vapor
  [All 15 components except water conserved; water decreases by evaporation]

Crystal rule: crystal_frac_out = crystal_frac_in (no growth, no dissolution)

Vapor exits at T_sat(P_vapor); NOT at boiling temperature.
Juice exits at T_boil = T_sat(P_vapor) + BPE(DS_out, PU_out, P_vapor)

Control modes:
  Mode A: VaporPressure given → iterate to find m_vapor and DS_out
  Mode B: FlowOutTemp given → find P and m_vapor to satisfy energy balance
  Mode C: HeatTransferCoef + HeatingSurface → Q = U·A·LMTD → find m_vapor
           LMTD uses T_sat_steam (NOT actual superheated T) and T_boil of juice
```

### B10.5 PAN
```
Like Evaporator BUT:
  - Crystal GROWTH occurs
  - Steam is ALWAYS required
  - Crystals form until massecuite reaches specified Total Solids and Ss

Energy balance identical to Evaporator.
Crystal content calculated by crystals_forward() given DS_out, Ss_spec, T_out.

Vapor exits at T_sat(P_vapor); massecuite exits at T_boil = T_sat + BPE.

Entrainment: m_entrain = EntrainmentLoss_ppm × m_vapor_condensable / 1e6
             Entrained droplets have same DS and purity as mother liquor.
```

### B10.6 CRYSTALLIZER
```
Crystals GROW as massecuite cools.
Ss_out specified (< Ss_in for cooling).
T_out specified (< T_in for cooling).
New crystal content = crystals_forward(DS_mc, PU_mc, T_out, Ss_out, a,b,c).
No evaporation. No steam. Pure heat loss to surroundings.
```

### B10.7 COOLER
```
Q_removed = m × (H_in - H_out)
No crystal growth. Crystal_frac_out = Crystal_frac_in.
Output may become supersaturated.
Phase change considered (vapor may partially condense).
```

### B10.8 FLASH TANK
```
Control: vapor exits at P_vapor (or T_sat specified).
T_out = T_sat(P_vapor) + BPE (with BPE if solution contains sugar).
m_vapor calculated from energy balance: H_in = H_liquid_out + H_vapor_out.
No crystal growth. Crystal_frac_out = Crystal_frac_in.
```

### B10.9 HEAT EXCHANGER
```
Port 0 = process; Port 1 = heating (or cooling)
Flows do NOT mix.
Q = m_0 × (H_0_out - H_0_in) = m_1 × (H_1_in - H_1_out) × (1 - heat_loss_frac)

Control mode A (T_out specified for port 0):
  Find m_1 (required flow) to satisfy energy balance.

Control mode B (Effectiveness specified, both flows known):
  Q_actual = effectiveness × Q_max
  Q_max = m_min × Cp_min × (T_h_in - T_c_in)
  Effectiveness uses ACTUAL T (not saturation T) for superheated steam.

Control mode C (HTC + Surface, condensing steam):
  Q = U × A × ΔTLM
  ΔTLM = (ΔT1 - ΔT2) / ln(ΔT1/ΔT2)
  For condensing: uses T_sat of steam (not superheated T) for ΔT calculation;
  but TOTAL enthalpy (including superheat) used for energy balance.

Condensate Drop: T_condensate_out = T_sat - CondensateDrop_K

Crystal dissolution: If T_out > T_sat(solution) → crystals dissolve to Ss=1.
```

### B10.10 CENTRIFUGAL — Balance Equations
*Source: Theory.htm (Centrifugal Calculations section)*

**Variable definitions:**
- `Cry` = crystal fraction in massecuite (0–1)
- `R` = Wash/Massecuite weight ratio
- `Pw` = wash purge ratio (fraction of wash purged to green)
- `Pl` = liquor purge ratio (fraction of mother liquor purged to green)
- `Z` = crystal loss ratio (fraction of crystals lost to green)
- `DSmc, PUmc` = massecuite DS and purity
- `DSml, PUml` = mother liquor DS and purity
- `DSw, PUw` = wash DS and purity (0 for water)
- `DSg, PUg` = green output DS and purity
- `DSs, PUs` = sugar output DS and purity
- `WRg, WRs` = weight ratios of green and sugar outputs to massecuite input

**Material balance equations (2-Output, wash=water, DSw=0):**
```
Weight balance:
  WRg + WRs = 1 + R

DS balance:
  WRg × DSg + WRs × DSs = DSmc + R × 0   [if water wash]

Sucrose balance:
  WRg × DSg × PUg + WRs × DSs × PUs = DSmc × PUmc + R × 0
```

**Performance ratios from measured data:**
```
Cry = crystals_forward(DSmc, PUmc, T, Ss, a, b, c).crystal_frac

R   = Ww / Wmc

WRs = (1 - Z) × Cry + (1 - Pl) × (1 - Cry) × DSml × PUml / DSs / PUs
      [simplified — use exact mass balance equations above]

Z   = Crystal Loss Ratio   = (crystals_to_green) / (total crystals in mc)
Pl  = Liquor Purge Ratio  = (mother_liquor_to_green) / (total ML in mc)
Pw  = Wash Purge Ratio    = (wash_to_green) / (total wash in)
```

**Iteration during balance:**
Default: **Use Residual Data** — holds mother liquor and wash residue fractions on crystal surface.
Alternative: Use Purge Data (Z, Pl, Pw) — holds performance ratios constant.

---

## B11. Python Coding Standards for Phase 02

### B11.1 Type hints required on all public functions

```python
def sucrose_saturation_pct(temp_c: float) -> float: ...
```

### B11.2 Docstrings required on all public functions

```python
def saturation_coefficient(nsw: float, a: float, b: float, c: float) -> float:
    """
    Calculate saturation coefficient Sc.
    Uses Vavrinecz if c != 0, Wagnerowski if c == 0.
    Wagnerowski valid only for NSW 1.6-3.5.

    Args:
        nsw: non-sucrose to water ratio (weight)
        a, b, c: Vavrinecz coefficients

    Returns:
        Saturation coefficient Sc (dimensionless, typically 1.0–1.6)

    Raises:
        ValueError: if nsw < 0
    """
```

### B11.3 No silent failures

```python
# WRONG:
def sucrose_saturation_pct(temp_c):
    try:
        return 64.397 + ...
    except:
        return 64.0   # silent fallback — FORBIDDEN

# CORRECT:
def sucrose_saturation_pct(temp_c: float) -> float:
    if not (-40 <= temp_c <= 200):
        raise ValueError(f"Temperature {temp_c}°C outside valid range -40..200°C")
    return 64.397 + 0.07251*temp_c + 0.0002057*temp_c**2 + 0.000000344*temp_c**3
```

### B11.4 All constants explicitly named and sourced

```python
# Vavrinecz constants — ICUMSA official (Theory.htm)
_VAV_A0 = 64.397
_VAV_A1 = 0.07251
_VAV_A2 = 0.0002057
_VAV_A3 = 0.000000344

# Syrup Cp constants — Sugar Technologists Manual 8th ed, eq 341/3
_SYR_CP_A0 = 4.187
_SYR_CP_A1 = -2.884
_SYR_CP_B0 = 0.00604
_SYR_CP_B1 = -0.00382
```

### B11.5 Units convention (SI throughout)

| Quantity | Unit |
|---------|------|
| Temperature | °C (convert to K for CoolProp) |
| Pressure | kPa (convert to Pa for CoolProp) |
| Mass flow | kg/h |
| Enthalpy | kJ/kg |
| Cp | kJ/kg·K |
| Density | kg/m³ |
| DS, purity, fractions | 0–1 (NOT %) inside engine |
| NSW | dimensionless ratio |
| Ss | dimensionless ratio |

**Important:** The VBA layer sends DS as % (0–100) in some fields (e.g., `ds_pct`). The engine must convert to fractions before calculation. Document any conversion point explicitly.

### B11.6 No circular imports between modules

```
fluids.py        — imports: numpy, CoolProp only
solubility.py    — imports: numpy only
bpe.py           — imports: solubility, fluids
heat_content.py  — imports: fluids, numpy
crystals.py      — imports: solubility, numpy
enthalpy.py      — imports: fluids, heat_content, crystals
density.py       — imports: fluids, numpy
```

---

## B12. Mandatory Unit Tests

### B12.1 `test_solubility.py`

```python
def test_vavrinecz_at_20c():
    assert abs(sucrose_saturation_pct(20.0) - 67.09) < 0.05

def test_vavrinecz_at_80c():
    assert abs(sucrose_saturation_pct(80.0) - 74.18) < 0.05

def test_wagnerowski_at_nsw_2():
    # c=0 triggers Wagnerowski; NSW=2.0
    sc = saturation_coefficient(2.0, 0.04, 0.71, 0.0)
    assert abs(sc - 1.072) < 0.001

def test_vavrinecz_beet_grut():
    # NSW=2.0, Grut beet coefficients
    sc = saturation_coefficient(2.0, 0.178, 0.82, -2.1)
    assert abs(sc - 1.15) < 0.05  # approximate

def test_supersaturation_example():
    # From Theory.htm example: DSml=86.68%, PUml=72.32%, T=81°C
    ss = supersaturation(0.8668, 0.7232, 81.0, 0.178, 0.82, -2.1)
    assert abs(ss - 1.10) < 0.02
```

### B12.2 `test_crystals.py`

```python
def test_forward_theory_example():
    """Theory.htm example: DSmc=93%, PUmc=86.44%, T=81°C, Ss=1.10, Grut"""
    result = crystals_forward(0.9300, 0.8644, 81.0, 1.100, 0.178, 0.82, -2.1)
    assert abs(result['crystal_frac'] - 0.4744) < 0.005
    assert abs(result['ds_ml'] - 0.8668) < 0.005
    assert abs(result['pu_ml'] - 0.7232) < 0.005

def test_inverse_round_trip():
    """Inverse should recover DS_mc and PU_mc from crystal_frac."""
    result = crystals_inverse(0.9300, 0.8644, 0.4744)
    assert abs(result['ds_ml'] - 0.8668) < 0.005
    assert abs(result['pu_ml'] - 0.7232) < 0.005
```

### B12.3 `test_bpe.py`

```python
def test_bpe_pure_water():
    """BPE of pure water is 0."""
    assert abs(bpe_celsius(0.0, 1.0, 101.325)) < 0.01

def test_bpe_typical_evaporator():
    """Typical 2nd effect: DS=65%, Purity=85%, P≈50kPa → BPE ~1.2°C approx"""
    bpe = bpe_celsius(0.65, 0.85, 50.0)
    assert 0.5 < bpe < 3.0  # sanity range

def test_boiling_temp_from_vapor_temp():
    """If vapor at 85°C, boiling temp should be higher by BPE."""
    p = water_sat_pressure_kpa(85.0)
    bpe = bpe_celsius(0.65, 0.85, p)
    t_boil = boiling_temp_c(0.65, 0.85, p)
    assert abs(t_boil - (85.0 + bpe)) < 0.1
```

### B12.4 `test_heat_content.py`

```python
def test_cp_water_at_20c():
    assert abs(cp_water_liquid(20.0, 101.325) - 4.182) < 0.002

def test_cp_syrup_pure_water():
    """DS=0 should give water Cp."""
    assert abs(cp_syrup(0.0, 20.0) - 4.187) < 0.01

def test_cp_sucrose_crystal_at_20c():
    # eq 311/2: 1.2473 + 0.002096*20 - 3.9e-6*400 = 1.2473+0.04192-0.00156 = 1.288
    assert abs(cp_sucrose_crystal(20.0) - 1.288) < 0.005

def test_steam_enthalpy_100c():
    """Saturated steam at 100°C: ~2675.6 kJ/kg"""
    h = water_enthalpy_kJkg(100.0, water_sat_pressure_kpa(100.0), quality=1.0)
    assert abs(h - 2675.6) < 1.0
```

---

## B13. File-Level Implementation Checklist

Before Phase 03 begins, each file must:

| File | Must pass |
|------|-----------|
| `fluids.py` | All CoolProp calls work; FileNotFoundError if FLD missing |
| `solubility.py` | All B12.1 tests pass |
| `crystals.py` | Theory.htm example exactly matches (B12.2) |
| `bpe.py` | All B12.3 tests pass |
| `heat_content.py` | All B12.4 tests pass |
| `enthalpy.py` | Energy balance on simple receiver: H_in = H_out ± 0.1% |
| `density.py` | Syrup density at DS=82.3% ≈ 1350 kg/m³ |

---

## PART C — RULES THAT APPLY ACROSS ALL PHASES

---

## C1. Convergence Accuracy
*Source: Theory.htm, Program_Overview.htm*

- Default tolerance: **0.01%** (= 0.0001 as a fraction)
- Tolerance applies to relative change in all internal flow values between iterations
- Maximum iterations default: **150**
- Both settings are user-adjustable in Model Properties (§A-Model Properties)

## C2. Error Classification
*Source: Error_Messages.htm*

**Fatal (stop balance):**
- Missing station number
- Duplicate station numbers
- Missing station name
- Effect numbers out of sequence
- Circular pressure feedback
- Both vapor and liquid outputs required on flash tank
- More than one centrifugal output required
- Required flow cannot be back-traced to a source

**Non-fatal warnings (balance continues):**
- Station numbers not following material flow direction
- Wagnerowski used with NSW outside 1.6–3.5
- Specified quantity overridden by required flow
- Insufficient distributor input (specified flows reduced)
- Vapor/condensate from evaporator detected as required

## C3. Units (SI default)
*Source: Program_Overview.htm*

| Quantity | SI unit | US unit |
|---------|---------|---------|
| Mass flow | kg/h | lb/h |
| Temperature | °C | °C or °F |
| Pressure | kPa | psi or in Hg |
| Volume | m³ | ft³ |
| Enthalpy | kJ/kg | BTU/lb |
| Heat transfer | W/m²·K | BTU/h·ft²·°F |
| Heating surface | m² | ft² |
| Power | kW | kW or hp |

## C4. Solubility Coefficient Default Values
*Source: Pan_Properties.htm*

| Sugar type | a | b | c |
|-----------|---|---|---|
| Beet (Grut) | 0.178 | 0.82 | −2.1 |
| Beet (Polish) | 0.27 | 0.71 | −1.4 |
| Cane (typical) | 0.04 | 0.71 | −2.1 |

When `c = 0`, Wagnerowski equation is used (valid NSW 1.6–3.5 only).

## C5. Phased Roadmap (Updated)

| Phase | Status | Deliverables |
|-------|--------|-------------|
| **01 — Visio Foundation** | ✅ COMPLETE | ThisDocument.bas, PurityForSugar.bas, StationDialogManager.bas |
| **02 — Thermodynamics Engine** | 🔨 TO BUILD | fluids.py, solubility.py, crystals.py, bpe.py, heat_content.py, enthalpy.py, density.py + tests |
| **03 — FastAPI Solver** | ⏳ After 02 | server.py, solver.py, 24 station modules, required_flows.py, pressure.py |
| **04 — Full Integration** | ⏳ After 03 | Flow Legend, R/P markers, revenues, Shape Data display |
| **05 — Packaging** | ⏳ After 04 | purity_engine.exe, installer, test suite vs all 12 examples |

---

*End of RULES v5.0*
*Phase 01 sections are LOCKED — do not modify the VBA files.*
*Phase 02 sections define exactly what to build. Build one file at a time, run tests, then proceed.*
