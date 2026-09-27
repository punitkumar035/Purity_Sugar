# Coding & Quality Standards

## 1. Python Thermodynamics Engine Standards (Phase 02 & 03)

### 1.1 Environment & Dependencies
- Python: `3.10+`
- Core libraries: `CoolProp >= 6.6.0`, `numpy >= 1.24`, `pytest >= 7.0`
- Steam / Water properties: Must use `CoolProp` backed by NIST `WATER.FLD`. No IF-97 approximations or third-party wrappers.

### 1.2 Unit Conventions (Internal SI)
Internal calculation modules MUST work exclusively in SI units:
- Mass flow: `kg/h`
- Temperature: `°C` (convert to `K` for CoolProp: $T_K = t + 273.15$)
- Pressure: `kPa` absolute (convert to `Pa` for CoolProp: $P_{Pa} = P_{kPa} \times 1000$)
- Dry Substance / Purity / Fractions: `0.0 to 1.0` (weight fractions)
- Enthalpy: `kJ/kg`
- Specific Heat ($C_p$): `kJ/(kg·K)`
- Density: `kg/m³`

External representations (such as Visio Shape Data or web forms passing `ds_pct` $0–100\%$) must be normalized immediately at the API boundary.

### 1.3 Strict Exception Handling
Silent fallbacks are **strictly forbidden**:
```python
# FORBIDDEN:
try:
    return calculate_property(temp)
except Exception:
    return 65.0  # Silent default

# REQUIRED:
if not (-40.0 <= temp_c <= 200.0):
    raise ValueError(f"Temperature {temp_c}°C outside valid physical bounds (-40 to 200°C)")
```

### 1.4 Code Structure & Import Discipline
No circular dependencies. The dependency hierarchy:
```
fluids.py       → numpy, CoolProp
solubility.py   → numpy
bpe.py          → solubility, fluids
heat_content.py → fluids, numpy
crystals.py     → solubility, numpy
enthalpy.py     → fluids, heat_content, crystals
density.py      → fluids, numpy
```

---

## 2. Web Application Standards (Phase 04 & HTML Solvers)

1. **Separation of Concerns**:
   Keep UI interaction, state management, thermodynamic solver algorithms, and validation checks decoupled into distinct layers.
2. **Design Aesthetics**:
   - Modern, clean engineering palette with high contrast and intuitive indicators.
   - Status indicators: CLEAR distinction between User Input, Calculated Value, Model Assumption, Reference Value, Warning, and Error.
3. **Data Integrity**:
   - Every input field must have min, max, step, and explicit unit indicators.
   - Live recalculation or explicit solve triggers with convergence diagnostics.
