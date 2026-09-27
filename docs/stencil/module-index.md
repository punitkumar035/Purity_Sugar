# Sugar Software Module Index & Stencil Directory
## Comprehensive Process Unit & Physical Chemistry Registry

> **Authoritative Basis**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Status Lifecycle**: `DISCOVERED` → `DRAFT` → `ENGINEERING-VALIDATED` → `UI-READY` → `IMPLEMENTED` → `TESTED` → `APPROVED`  
> **Status**: `ALL PRIMARY STENCILS ENGINEERING-VALIDATED`

---

## 1. Executive Module Roster

This registry establishes every process unit, physical chemistry calculation engine, and factory balance system derived from Sugar's Help Book. A software module cannot be coded by Agent 4 (Developer) until its specification is authored and marked `ENGINEERING-VALIDATED`.

| Module ID | Module Name | Scope / Equipment | Governing Source in Help Book | Stencil File | Status |
|---|---|---|---|---|---|
| **STENCIL-THERMO-01** | Physical Chemistry & Sucrose Thermodynamics | Pure sucrose solubility, Vavrinecz/Wagnerowski $S_c$, Van Hook $S_s$, BPE, $C_p$, enthalpy | `Theory/Theory.md`, `Sucrose_Supersaturation/` | `modules/sucrose-thermodynamics.md` | `ENGINEERING-VALIDATED` |
| **STENCIL-PAN-01** | Vacuum Pan Boiling | Batch & continuous vacuum pans, calandria steam, boiling massecuite, supersaturation | `Pan/`, `Theory/Theory.md` | [`modules/vacuum-pan.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/vacuum-pan.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-EVAP-01** | Evaporator Station & Effects | Single-effect & multi-effect trains (4/5/6 effect), Robert/falling film, bleeding | `Evaporator/`, `Examples/4-Effect_Multiple.md` | [`modules/evaporator.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/evaporator.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-HEAT-01** | Juice & Process Heating | Shell-and-tube, plate heaters (PHE), heat recovery, approach control | `Heat_Exchanger/` | [`modules/juice-heating.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/juice-heating.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-INJ-01** | Direct Steam Injection Heater | Direct steam mixing, instantaneous condensation, process dilution | `Injection_Heater/` | [`modules/injection-heater.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/injection-heater.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-MELT-01** | Sugar Melter & Remelt System | Crystal dissolution, water/sweet water dilution, target Brix control, heating | `Melter/` | [`modules/sugar-melter.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-melter.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-BLND-01** | Blender & Magma Mixer | Mingling sugar with syrup/water, crystal preservation, ratio/Brix control | `Blender/` | [`modules/magma-mixer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/magma-mixer.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CENT-01** | Centrifugal Separation Station | 2-output continuous & 3-output batch centrifugals, purge evaluations, molasses | `Centrifugal/`, `Theory/Theory.md` | [`modules/centrifugal.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/centrifugal.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CRYS-01** | Massecuite Cooling Crystallizer | Air/water cooling, desupersaturation, crystal growth, mother liquor exhaustion | `Crystallizer/`, `Theory/Theory.md` | [`modules/crystallizer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/crystallizer.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-FLS-01** | Flash Tank & Condensate Recovery | Condensate flash, liquor flash cooling, flash vapour generation | `Flash_Tank/` | [`modules/flash-tank.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/flash-tank.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-DRY-01** | Sugar Rotary Dryer | Rotary drum dryer, dust entrainment loss, moisture evaporation | `Dryer/` | [`modules/sugar-dryer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-dryer.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CLR-01** | Sugar Cooler & Heat Loss | Sensible cooling, non-crystallizing supersaturation, radiation loss | `Cooler/` | [`modules/sugar-cooler.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/sugar-cooler.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CMP-01** | Mechanical Vapor Compressor (MVR)| Vapor recompression, isentropic compression, non-condensation rule | `Compressor/` | [`modules/vapor-compressor.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/vapor-compressor.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-TCM-01** | Steam Thermocompressor | Supersonic steam jet ejector, Truffault formula, 5% wear allowance | `Thermocompressor/` | [`modules/thermocompressor.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/thermocompressor.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-PRV-01** | Pressure Reducer (PRV) | Isenthalpic throttling, Joule-Thomson expansion, quench spray | `Pressure_Reducer/` | [`modules/pressure-reducer.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/pressure-reducer.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-PMP-01** | Process Pump & Fluid Hydraulics | Centrifugal & positive displacement pumps, bubble collapse, head boost | `Pump/` | [`modules/process-pump.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/process-pump.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-TNK-01** | Process & Storage Tank | Storage accumulation/depletion, Port 9 Brix hold, Port 10 coil/injection | `Tank/` | [`modules/process-tank.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/process-tank.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-TRB-01** | Steam Turbines & Cogeneration | Back-pressure & condensing turbines, turbo alternators, power dispatch | `Turbine/`, `Turbo_Alternator/` | [`modules/steam-turbine.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/steam-turbine.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CND-01** | Barometric & Surface Condensers | Direct contact barometric condensers, surface condensers, approach control | `Contact_Condenser/`, `Surface_Condenser/` | [`modules/condensers.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/condensers.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-SEP-01** | Separator & Filter Station | Solid-liquid separation, rotary vacuum filter, bagacillo retention | `Separator_Filter/` | [`modules/separator-filter.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/separator-filter.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-CONN-01**| Cross-Page Connector | Multi-sheet topological bridging, off-page references, zero-loss link | Phase 4 Visio | [`modules/cross-page-connector.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/cross-page-connector.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-MILL-01** | Plant Capacity & Cane Milling | Cane prep, shredder, 4–6 mill tandem, imbibition water, bagasse, mixed juice | `Examples/Cane_Factory-Milling.md` | [`modules/plant-capacity-and-cane-milling.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/plant-capacity-and-cane-milling.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-DIFF-01** | Cane Diffusion & Dewatering | Cane diffuser, percolation, press water recirculation, dewatering mills | `Examples/Cane_Factory-Diffusion.md` | [`modules/cane-diffusion-and-extraction.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/cane-diffusion-and-extraction.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-BAL-01** | Factory Steam, Fuel & Energy Balance | Overall factory steam balance, boiler efficiency, bagasse fuel demand | `Examples/Cane_Factory-Milling.md` | [`modules/steam-and-heat-balance.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/steam-and-heat-balance.md) | `ENGINEERING-VALIDATED` |
| **STENCIL-REFIN-01** | Cane Sugar Refinery & Decolorization | Affination, melting, carbonatation, filtration, ion exchange, white boiling | `Examples/Cane_Sugar_Refinery.md` | [`modules/desugarization-and-ion-exchange.md`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/desugarization-and-ion-exchange.md) | `ENGINEERING-VALIDATED` |

---

## 2. Cross-Module Data Flow & Process Train Architecture

```text
[CANE / BEET FEED]
       │
       ▼
STENCIL-MILL-01 / STENCIL-DIFF-01 (Milling / Diffusion)
       │  ├── Bagasse → STENCIL-BAL-01 (Boiler Fuel)
       │  └── Mixed / Draft Juice
       ▼
STENCIL-HEAT-01 / STENCIL-INJ-01 (Primary Juice Heating)
       │  ▲
       │  └── Bleed Vapour from STENCIL-EVAP-01
       ▼
STENCIL-SEP-01 (Liming, Clarification & RVF Mud Filtration)
       │  ├── Filter Cake (Discard)
       │  ├── Sweet Water → STENCIL-MELT-01
       │  └── Clear Juice
       ▼
STENCIL-HEAT-01 (Secondary Juice Heating)
       ▼
STENCIL-EVAP-01 (Multi-Effect Evaporator Train)
       │  ├── Bleed Vapours → Heaters, Pans, TCM (STENCIL-TCM-01)
       │  ├── Condensates → STENCIL-FLS-01 & Boiler Feed
       │  └── Concentrated Syrup (~65° Brix)
       ▼
STENCIL-PAN-01 (Vacuum Pan Evaporative Crystallization)
       │  ├── Pan Vapours → STENCIL-CND-01 (Condensers) or MVR (STENCIL-CMP-01)
       │  ├── Condensate → Flash Recovery
       │  └── Massecuite (A, B, C)
       ▼
STENCIL-CRYS-01 (Crystallizers — Controlled Cooling Growth)
       │  └── Exhausted Massecuite
       ▼
STENCIL-CENT-01 (Centrifugals — Sugar / Molasses Separation)
       │  ├── C-Sugar / B-Sugar → STENCIL-BLND-01 / STENCIL-MELT-01 (Seed / Remelt)
       │  ├── Final Molasses → Storage / STENCIL-REFIN-01
       │  └── Commercial A-Sugar (Moist)
       ▼
STENCIL-DRY-01 / STENCIL-CLR-01 (Sugar Dryer & Cooler)
       ▼
[BAGGED COMMERCIAL SUGAR]
```
