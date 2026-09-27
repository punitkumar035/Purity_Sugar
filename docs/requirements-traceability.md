# Requirements Traceability Matrix

| Req ID | Requirement Description | Rule Source | Implementation Target | Verification / Test Case | Status |
|---|---|---|---|---|---|
| **REQ-VBA-01** | Visio Event Handlers in `ThisDocument` | RULES v5.0 §A13.1 | `files (4)/ThisDocument.bas` | Visio `.vsdm` runtime | LOCKED ✅ |
| **REQ-VBA-02** | Station Color States (RED/BLUE/YELLOW) | RULES v5.0 §A2 | `files (4)/PurityForSugar.bas` | Manual drop & property test | LOCKED ✅ |
| **REQ-VBA-03** | 15-Component Flow Stream Serialization | RULES v5.0 §A6, §A12 | `files (4)/PurityForSugar.bas` | `SerializeGraph()` payload test | LOCKED ✅ |
| **REQ-WEB-01** | Standalone Massecuite Simulator | Web App Specs | `massecuite_phase4_8_9_1_centrifugal_solver.html` | Browser execution | OPERATIONAL 🌐 |
| **REQ-ENG-01** | Vavrinecz Pure Sucrose Saturation | RULES v5.0 §B3.1 | `engine/solubility.py` | `test_solubility.py` (B12.1) | COMPLETED (32/32 pass) ✅ |
| **REQ-ENG-02** | Saturation Coefficient (Vavrinecz/Wagnerowski) | RULES v5.0 §B3.2-B3.3 | `engine/solubility.py` | `test_solubility.py` (B12.1) | COMPLETED (32/32 pass) ✅ |
| **REQ-ENG-03** | Forward & Inverse Crystal Calculations | RULES v5.0 §B4 | `engine/crystals.py` | `test_crystals.py` (B12.2) | COMPLETED (10/10 pass) ✅ |
| **REQ-ENG-04** | Kadlec-Bretschneider-Dandor BPE | RULES v5.0 §B6 | `engine/bpe.py` | `test_bpe.py` (B12.3) | COMPLETED (11/11 pass) ✅ |
| **REQ-ENG-05** | Specific Heat Capacity ($C_p$) | RULES v5.0 §B5 | `engine/heat_content.py` | `test_heat_content.py` (B12.4) | COMPLETED (14/14 pass) ✅ |
| **REQ-ENG-06** | Total Enthalpy with Crystallization Heat | RULES v5.0 §B7 | `engine/enthalpy.py` | `test_enthalpy.py` | COMPLETED (7/7 pass) ✅ |
| **REQ-ENG-07** | Syrup and Massecuite Density | RULES v5.0 §B8 | `engine/density.py` | `test_density.py` | COMPLETED (9/9 pass) ✅ |
| **REQ-ENG-08** | CoolProp Integration with NIST `WATER.FLD` | RULES v5.0 §B2 | `engine/fluids.py` | `test_fluids.py` | COMPLETED (14/14 pass) ✅ |
| **REQ-API-01** | FastAPI Solver Service (`localhost:8765`) | RULES v5.0 §A12 | `server/app.py`, `server.py` | `test_server.py`, `test_network.py` | COMPLETED (21/21 pass) ✅ |
| **REQ-STN-01** | Sugar Help Book Systematic Extraction | Agent 9 Mandate | `docs/stencil/skill-index.md` | Complete 110-file index | COMPLETED ✅ |
| **REQ-STN-02** | Software Module Registry & Lifecycle | Agent 9 Mandate | `docs/stencil/module-index.md` | 21-module registry | COMPLETED ✅ |
| **REQ-STN-03** | Field & Formula Standardization | Agent 9 Mandate | `docs/stencil/field-registry.md`, `formula-registry.md` | Mathematical & SI definitions | COMPLETED ✅ |
| **REQ-STN-04** | Physical Limits & Cross-Check Matrix | Agent 9 Mandate | `docs/stencil/validation-registry.md`, `cross-check-registry.md` | Error/warning/closure rules | COMPLETED ✅ |
| **REQ-STN-05** | Engineering Module Stencils | Agent 9 Mandate | `docs/stencil/modules/*.md` | 18-point stencils for all units | COMPLETED ✅ |
| **REQ-PW-01** | Property Window JSON Schema Specification | Agent 10 Mandate | `docs/property-windows/schemas/property-window-schema.json` | JSON Schema validation | COMPLETED ✅ |
| **REQ-PW-02** | Property Window Registry & Master Index | Agent 10 Mandate | `docs/property-windows/index.md` | Standard hierarchy & registry | COMPLETED ✅ |
| **REQ-PW-03** | Equipment Property Window Specifications | Agent 10 Mandate | `docs/property-windows/modules/*.md` | 10 specifications with cross-checks | COMPLETED ✅ |
| **REQ-PW-04** | Web Application Property Window Integration | Agent 10 Mandate | `massecuite_phase4_8_9_1_centrifugal_solver.html` | Sidebar & modal inspection in browser | COMPLETED ✅ |
| **REQ-REV-01** | Net Process Revenues Calculation | Help Book Program Overview & RULES §C5 | `solver/network.py`, `server/app.py`, `solver/excel_export.py` | `tests/test_revenues.py` | COMPLETED (4/4 pass) ✅ |
| **REQ-BRG-01** | Web Application HTTP Backend Bridge | RULES §A12, Architecture | `massecuite_phase4_8_9_1_centrifugal_solver.html` | Browser subagent verified & operational | COMPLETED ✅ |
| **REQ-RBN-01** | Multi-Page Model & PageManager | Implementation Plan §3–§4 | `massecuite_phase4_8_9_1_centrifugal_solver.html` | JSDOM & Chromium Browser Subagent | COMPLETED ✅ |
| **REQ-RBN-02** | Visio Bottom Page Tab Bar | Implementation Plan §5 | `massecuite_phase4_8_9_1_centrifugal_solver.html` | CRUD, tabs, scroll, context menu | COMPLETED ✅ |
| **REQ-RBN-03** | CAD Sheet Outline & Title Block | Implementation Plan §7, §13 | `massecuite_phase4_8_9_1_centrifugal_solver.html` | A4/A3/Letter/Custom dimensions | COMPLETED ✅ |
| **REQ-RBN-04** | 10 Ribbon Tabs & Action Bindings | Implementation Plan §11–§20 | `massecuite_phase4_8_9_1_centrifugal_solver.html` | File/Home/Insert/Design/Data/Process/Review/View/Developer/Help | COMPLETED ✅ |
| **REQ-RBN-05** | Multi-Page Project Serialization | Implementation Plan §8–§9 | `massecuite_phase4_8_9_1_centrifugal_solver.html` | `schemaVersion: 1`, legacy migration | COMPLETED ✅ |

