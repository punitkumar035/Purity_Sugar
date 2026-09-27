# Project Map: Purity for Sugar

## 1. Directory Structure

```text
c:\Users\punit\OneDrive\Documents\Purity_Sugar\
├── AGENTS.md                                   # Root multi-agent directives
├── GEMINI.md                                   # Workspace directives mirror
├── README.md                                   # Master project readme
├── RULES_v5.md                                 # Master engineering rulebook (v5.0)
├── Sugar_Multi_Agent_Development_Protocol.md   # Multi-agent protocol specification
├── massecuite_phase4_8_9_1_centrifugal_solver.html # Standalone web simulator (Phase 4.8.9)
├── sugars-helpbook.skill                       # Compressed skill archive
├── pytest.ini                                  # Pytest configuration
├── server.py                                   # Standalone FastAPI launcher on port 8765
│
├── .agents/                                    # Antigravity agent configuration root
│   ├── rules/                                  # Workspace rules
│   │   ├── 00_master_agent_protocol.md
│   │   ├── 01_sugar_engineering_rules.md
│   │   ├── 02_agent_roles_and_responsibilities.md
│   │   ├── 03_coding_and_quality_standards.md
│   │   ├── 04_stencil_architect_rules.md
│   │   └── 05_property_window_architect_rules.md
│   └── skills/                                 # Specialized skills
│       ├── sugars-helpbook/                    # Extracted Sugar's Help Book library (415 files)
│       │   ├── SKILL.md
│       │   ├── references/                     # Properties, Features, Examples, Theory
│       │   └── assets/                         # Equation diagrams & screenshots
│       ├── sugar-master-agent/SKILL.md
│       ├── sugar-architect-agent/SKILL.md
│       ├── sugar-engineering-specialist/SKILL.md
│       ├── sugar-uiux-agent/SKILL.md
│       ├── sugar-developer-agent/SKILL.md
│       ├── sugar-qa-tester/SKILL.md
│       ├── sugar-debugger-agent/SKILL.md
│       ├── sugar-code-reviewer/SKILL.md
│       ├── sugar-documentation-agent/SKILL.md
│       ├── sugar-stencil-architect/SKILL.md
│       ├── sugar-property-window-architect/SKILL.md
│       └── typesafe-ai/SKILL.md                # TypeSafe / Jev AI structured decision model
│
├── docs/                                       # Shared project memory
│   ├── agent-state.md                          # Active machine-readable state
│   ├── project-map.md                          # This file
│   ├── architecture.md                         # Technical architecture & layer boundaries
│   ├── engineering-basis.md                    # Thermodynamic equations & literature sources
│   ├── calculation-register.md                 # Complete register of all calculation modules
│   ├── engineering-assumptions.md              # Explicit assumptions register
│   ├── requirements-traceability.md            # Traceability matrix
│   ├── stencil/                                # Stencil Architect specifications (Agent 9)
│   └── property-windows/                       # Property Window specifications (Agent 10)
│
├── engine/                                     # Phase 02: Thermodynamics Library (97/97 tests pass ✅)
│   ├── __init__.py
│   ├── solubility.py                           # Vavrinecz sucrose solubility & saturation coefficients
│   ├── crystals.py                             # Crystal content, mother liquor exhaustion, mass balance
│   ├── fluids.py                               # CoolProp IAPWS-95 steam/water properties
│   ├── heat_content.py                         # Specific heats (syrup, crystals, lime, fiber, gases)
│   ├── bpe.py                                  # Bubník-Kadlec & KBD boiling point elevation
│   ├── enthalpy.py                             # 15-component stream enthalpy & crystallization heat
│   ├── density.py                              # Lyle/Rein syrup & two-phase massecuite density
│   └── tests/                                  # Unit tests for thermodynamics engine
│
├── solver/                                     # Phase 03: Flowsheet Network Solver (118/118 tests pass ✅)
│   ├── __init__.py
│   ├── stream.py                               # 15-component stream representation & mixing
│   ├── schemas.py                              # Pydantic data contracts (API schema v1.0)
│   ├── network.py                              # Sequential modular network solver & closures
│   ├── excel_export.py                         # Openpyxl multi-sheet workbook generation
│   └── stations/                               # 24 station unit operations
│       ├── __init__.py
│       ├── base.py
│       ├── blender.py
│       ├── centrifugal.py
│       ├── cooler.py
│       ├── condensers.py
│       ├── compressor.py
│       ├── crystallizer.py
│       ├── distributor.py
│       ├── evaporator.py
│       ├── flash_tank.py
│       ├── heat_exchanger.py
│       ├── injection_heater.py
│       ├── melter.py
│       ├── pan.py
│       ├── pressure_reducer.py
│       ├── process_units.py
│       ├── pump.py
│       ├── receiver.py
│       ├── tank.py
│       ├── thermocompressor.py
│       └── turbine.py
│
├── server/                                     # Phase 03: FastAPI Service
│   ├── __init__.py
│   └── app.py                                  # REST endpoints (/status, /solve, /validate, /export/excel)
│
├── tests/                                      # Phase 03: Solver & Service Tests
│   ├── test_stream.py
│   ├── test_stations.py
│   ├── test_network.py
│   └── test_server.py
│
└── files (4)/                                  # Phase 01: Visio Foundation (LOCKED ✅)
    ├── PurityForSugar.bas                      # Main VBA module (Ribbon, Graph serialization, API)
    ├── StationDialogManager.bas                # InputBox field specs for 24 station types
    └── ThisDocument.bas                        # Visio Object event handlers (Drop, DoubleClick)
```

## 2. Component Inventory

| Component | Technology | Role | Status |
|---|---|---|---|
| **Phase 01: Visio Canvas** | MS Visio `.vsdm`, VBA | Process flowsheet UI, station numbering, Shape Data display | LOCKED ✅ |
| **Phase 01: VBA API Client** | `MSXML2.ServerXMLHTTP` | Serializes Visio graph to JSON, communicates with Python engine | LOCKED ✅ |
| **Web Simulator** | HTML5, Vanilla CSS, JS | Interactive Massecuite Boiling Scheme Simulator (Phase 4.8.9) | Operational 🌐 |
| **Domain Authority** | Markdown, assets | `Sugar's Help Book` reference manual & theory | Active 📚 |
| **Multi-Agent System** | Antigravity IDE Agents | Coordinated 11-agent engineering team (Agents 0-10) | Configured 🤖 |
| **Phase 02: Python Engine** | Python 3.10+, CoolProp | Thermodynamics library (solubility, crystals, BPE, Cp, enthalpy) | COMPLETED (97/97 PASS) ✅ |
| **Phase 03: FastAPI Solver** | Python, FastAPI | Full network balance solver on `localhost:8765` | COMPLETED (118/118 PASS) ✅ |
| **Phase 04: Full Integration** | Python, HTML5, VBA | Revenues engine, Web App backend bridge, Flow Legend & R/P markers | IN PROGRESS 🔨 |
| **Phase 05: Packaging** | PyInstaller | Standalone executable (`purity_engine.exe`) & installer | Planned ⏳ |
