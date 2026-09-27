# Sugar Engineering Field Registry

> **Authoritative Basis**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Agent 9: Sugar Stencil Architect**  
> **Classification Standard**: User Input (`USER`), Optional Input (`OPTIONAL`), Dropdown Selection (`DROPDOWN`), Reference Lookup (`REFERENCE`), Intermediate Calculation (`INTERMEDIATE`), Final Output (`OUTPUT`).

---

## 1. Plant Capacity & Milling Fields

| Field ID | Field Name | Category | Data Type | Engineering Unit | Default | Validation Limits | Source / Module |
|---|---|---|---|---|---|---|---|
| `cane_crushing_rate` | Cane Crushing Rate | USER | Number | `t/h` (TCH) | 250.0 | $10.0 \le v \le 2000.0$ | `STENCIL-MILL-01` |
| `cane_fiber_pct` | Cane Fiber % | USER | Number | `%` | 13.5 | $8.0 \le v \le 22.0$ | `STENCIL-MILL-01` |
| `cane_pol_pct` | Cane Pol % | USER | Number | `%` | 13.0 | $8.0 \le v \le 18.0$ | `STENCIL-MILL-01` |
| `cane_brix_pct` | Cane Brix % | USER | Number | `°Brix` | 15.5 | $10.0 \le v \le 22.0$ | `STENCIL-MILL-01` |
| `imbibition_water_pct_cane` | Imbibition Water % Cane | USER | Number | `% cane` | 28.0 | $10.0 \le v \le 50.0$ | `STENCIL-MILL-01` |
| `imbibition_temp` | Imbibition Water Temp | USER | Number | `°C` | 75.0 | $50.0 \le v \le 95.0$ | `STENCIL-MILL-01` |
| `bagasse_moisture_pct` | Bagasse Moisture % | USER | Number | `%` | 49.0 | $40.0 \le v \le 56.0$ | `STENCIL-MILL-01` |
| `bagasse_pol_pct` | Bagasse Pol % | USER | Number | `%` | 2.2 | $1.0 \le v \le 4.5$ | `STENCIL-MILL-01` |
| `bagasse_fiber_pct` | Bagasse Fiber % | INTERMEDIATE | Number | `%` | 47.0 | Calculated ($100 - M - Pol - Brix$) | `STENCIL-MILL-01` |
| `bagasse_flow` | Bagasse Mass Flow | OUTPUT | Number | `kg/h` | — | Derived from fiber balance | `STENCIL-MILL-01` |
| `mixed_juice_flow` | Mixed Juice Mass Flow | OUTPUT | Number | `kg/h` | — | Derived from cane + imbibition - bagasse | `STENCIL-MILL-01` |
| `mixed_juice_brix` | Mixed Juice Brix | OUTPUT | Number | `°Brix` | — | Derived from solids balance | `STENCIL-MILL-01` |
| `mixed_juice_purity` | Mixed Juice Purity | OUTPUT | Number | `%` | — | Derived from pol / brix | `STENCIL-MILL-01` |
| `pol_extraction_pct` | Pol Extraction | OUTPUT | Number | `%` | — | Expected $94.0–98.0\%$ | `STENCIL-MILL-01` |

---

## 2. Juice Heating Fields

| Field ID | Field Name | Category | Data Type | Engineering Unit | Default | Validation Limits | Source / Module |
|---|---|---|---|---|---|---|---|
| `htr_control_mode` | Temperature Control Mode | DROPDOWN | Select | — | `TARGET_TEMP` | `TARGET_TEMP`, `TEMP_RISE`, `STEAM_FLOW` | `STENCIL-HEAT-01` |
| `htr_target_temp` | Target Output Temperature | USER | Number | `°C` | 85.0 | $30.0 \le v \le 135.0$ | `STENCIL-HEAT-01` |
| `htr_temp_rise` | Specified Temperature Rise | OPTIONAL | Number | `°C` | 30.0 | $5.0 \le v \le 80.0$ | `STENCIL-HEAT-01` |
| `htr_heat_loss_pct` | Heat Loss % | USER | Number | `%` | 1.0 | $0.0 \le v \le 5.0$ | `STENCIL-HEAT-01` |
| `htr_subcooling` | Condensate Subcooling | OPTIONAL | Number | `°C` | 0.0 | $0.0 \le v \le 15.0$ | `STENCIL-HEAT-01` |
| `htr_steam_press_abs` | Heating Steam / Vapour Pressure | USER | Number | `kPa abs` | 101.325 | $10.0 \le v \le 400.0$ | `STENCIL-HEAT-01` |
| `htr_heat_duty` | Heat Duty | INTERMEDIATE | Number | `kJ/h` | — | $M_{j} \cdot C_p \cdot \Delta T$ | `STENCIL-HEAT-01` |
| `htr_steam_demand` | Heating Steam Flow Required | OUTPUT | Number | `kg/h` | — | $Q / (\Delta h \cdot (1 - f_{loss}))$ | `STENCIL-HEAT-01` |
| `htr_condensate_flow` | Condensate Mass Flow Out | OUTPUT | Number | `kg/h` | — | Equal to steam flow | `STENCIL-HEAT-01` |

---

## 3. Evaporator Station Fields

| Field ID | Field Name | Category | Data Type | Engineering Unit | Default | Validation Limits | Source / Module |
|---|---|---|---|---|---|---|---|
| `evap_num_effects` | Number of Evaporator Effects | USER | Integer | Bodies | 4 | $1 \le n \le 7$ | `STENCIL-EVAP-01` |
| `evap_solids_control` | Solids Control Mode | DROPDOWN | Select | — | `TARGET_BRIX` | `TARGET_BRIX`, `EVAPORATION_RATE`, `STEAM_FLOW` | `STENCIL-EVAP-01` |
| `evap_target_brix` | Target Output Syrup Brix | USER | Number | `°Brix` | 65.0 | $50.0 \le v \le 75.0$ | `STENCIL-EVAP-01` |
| `evap_pressure_mode` | Pressure Specification Mode | DROPDOWN | Select | — | `VAPOUR_PRESSURE` | `VAPOUR_PRESSURE`, `VAPOUR_TEMP` | `STENCIL-EVAP-01` |
| `evap_body_pressure` | Vapour Space Pressure | USER | Number | `kPa abs` | 20.0 | $10.0 \le v \le 350.0$ | `STENCIL-EVAP-01` |
| `evap_motive_steam_press` | 1st Effect Steam Pressure | USER | Number | `kPa abs` | 170.0 | $120.0 \le v \le 300.0$ | `STENCIL-EVAP-01` |
| `evap_heat_loss_pct` | Radiation & Convection Heat Loss | USER | Number | `%` | 1.5 | $0.5 \le v \le 5.0$ | `STENCIL-EVAP-01` |
| `evap_bpe_method` | BPE Algorithm | DROPDOWN | Select | — | `BUBNIK_KADLEC` | `BUBNIK_KADLEC`, `KBD_1978`, `SASKA_2002` | `STENCIL-EVAP-01` |
| `evap_bpe_value` | Calculated BPE | INTERMEDIATE | Number | `°C` | — | Expected $0.5–5.0^\circ\text{C}$ | `STENCIL-EVAP-01` |
| `evap_syrup_flow` | Syrup Mass Flow Out | OUTPUT | Number | `kg/h` | — | Solved by solids conservation | `STENCIL-EVAP-01` |
| `evap_evaporation_rate` | Total Water Evaporated | OUTPUT | Number | `kg/h` | — | $M_{juice} - M_{syrup}$ | `STENCIL-EVAP-01` |
| `evap_steam_consumption` | Motive Steam Consumed | OUTPUT | Number | `kg/h` | — | Energy balance on 1st calandria | `STENCIL-EVAP-01` |
| `evap_steam_economy` | Steam Economy | OUTPUT | Number | `kg evap / kg steam` | — | Ratio total evap / steam in | `STENCIL-EVAP-01` |

---

## 4. Vacuum Pan & Crystallization Fields

| Field ID | Field Name | Category | Data Type | Engineering Unit | Default | Validation Limits | Source / Module |
|---|---|---|---|---|---|---|---|
| `pan_strike_type` | Strike / Massecuite Type | DROPDOWN | Select | — | `A_MASSECUITE` | `A_MASSECUITE`, `B_MASSECUITE`, `C_MASSECUITE`, `REFINED` | `STENCIL-PAN-01` |
| `pan_operation_mode` | Pan Operation Mode | DROPDOWN | Select | — | `CONTINUOUS` | `CONTINUOUS`, `BATCH` | `STENCIL-PAN-01` |
| `pan_target_massecuite_ds` | Target Massecuite DS | USER | Number | `% DS` | 90.0 | $80.0 \le v \le 96.0$ | `STENCIL-PAN-01` |
| `pan_supersaturation` | Mother Liquor Supersaturation (SS) | USER | Number | Dimensionless | 1.10 | $1.00 \le v \le 1.30$ | `STENCIL-PAN-01` |
| `pan_solubility_basis` | Solubility Model | DROPDOWN | Select | — | `CANE_TYPICAL` | `CANE_TYPICAL`, `BEET_TYPICAL`, `CUSTOM` | `STENCIL-PAN-01` |
| `pan_coef_a` | Vavrinecz Coefficient 'a' | USER / REF | Number | Dimensionless | 0.0400 | $-1.0 \le v \le 2.0$ | `STENCIL-PAN-01` |
| `pan_coef_b` | Vavrinecz Coefficient 'b' | USER / REF | Number | Dimensionless | 0.7100 | $0.0 \le v \le 2.0$ | `STENCIL-PAN-01` |
| `pan_coef_c` | Vavrinecz Coefficient 'c' | USER / REF | Number | Dimensionless | -2.1000 | $-5.0 \le v \le 0.0$ | `STENCIL-PAN-01` |
| `pan_vapour_pressure` | Pan Operating Vacuum / Absolute Pressure | USER | Number | `kPa abs` | 16.0 | $12.0 \le v \le 30.0$ | `STENCIL-PAN-01` |
| `pan_crystal_content` | Massecuite Crystal Content ($X_c$) | OUTPUT | Number | `% on mc` | — | Expected $35–52\%$ | `STENCIL-PAN-01` |
| `pan_mother_liquor_ds` | Mother Liquor DS | OUTPUT | Number | `%` | — | Expected $75–88\%$ | `STENCIL-PAN-01` |
| `pan_mother_liquor_purity` | Mother Liquor Purity | OUTPUT | Number | `%` | — | Must be lower than feed purity | `STENCIL-PAN-01` |
| `pan_boiling_temp` | Massecuite Boiling Temperature | OUTPUT | Number | `°C` | — | $T_{sat}(P) + \text{BPE}$ | `STENCIL-PAN-01` |
| `pan_steam_demand` | Calandria Steam Required | OUTPUT | Number | `kg/h` | — | Derived from energy balance | `STENCIL-PAN-01` |

---

## 5. Centrifugal Separation Fields

| Field ID | Field Name | Category | Data Type | Engineering Unit | Default | Validation Limits | Source / Module |
|---|---|---|---|---|---|---|---|
| `cent_machine_type` | Machine Type | DROPDOWN | Select | — | `BATCH` | `BATCH` (3-out), `CONTINUOUS` (2-out) | `STENCIL-CENT-01` |
| `cent_wash_ratio` | Wash Water / Massecuite Ratio | USER | Number | `kg/kg` | 0.030 | $0.00 \le v \le 0.15$ | `STENCIL-CENT-01` |
| `cent_wash_temp` | Wash Water Temperature | USER | Number | `°C` | 85.0 | $60.0 \le v \le 100.0$ | `STENCIL-CENT-01` |
| `cent_purge_zg` | Mother Liquor Purge Fraction ($Z_g$) | USER / REF | Number | Dimensionless | 0.80 | $0.50 \le v \le 0.98$ | `STENCIL-CENT-01` |
| `cent_wash_purge_pw` | Wash Water Purge Fraction ($P_w$) | USER / REF | Number | Dimensionless | 0.85 | $0.50 \le v \le 0.99$ | `STENCIL-CENT-01` |
| `cent_sugar_pol` | Sugar Pol / Purity | OUTPUT | Number | `°Z / %` | — | Batch: $99.5–99.9$; Cont: $90–94$ | `STENCIL-CENT-01` |
| `cent_sugar_moisture` | Sugar Moisture | OUTPUT | Number | `%` | — | Expected $0.5–1.5\%$ | `STENCIL-CENT-01` |
| `cent_sugar_yield` | Sugar Yield on Massecuite | OUTPUT | Number | `%` | — | Mass sugar / mass mc $\times 100$ | `STENCIL-CENT-01` |
| `cent_green_mol_flow` | Green Molasses Flow | OUTPUT | Number | `kg/h` | — | Purged mother liquor | `STENCIL-CENT-01` |
| `cent_wash_mol_flow` | Wash Molasses Flow | OUTPUT | Number | `kg/h` | — | Batch only (wash + dissolved sugar) | `STENCIL-CENT-01` |
