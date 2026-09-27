# Technical Architecture: Purity for Sugar

## 1. System Overview

Purity for Sugar is a hybrid engineering simulation platform supporting two complementary user interfaces and a unified calculation architecture:

1. **Visio Macro-Enabled Workspace (`.vsdm`)**:
   Built on Microsoft Visio with custom stencils (`Sug_*.vss`) and VBA modules (`files (4)/`). It serializes the flowsheet graph to JSON and invokes the backend via HTTP.
2. **Standalone Web Simulator (`massecuite_phase4_8_9_1_centrifugal_solver.html`)**:
   A single-page, browser-native simulation tool featuring an engineering ribbon, interactive flowsheet canvas, property panes, and client-side balance solver.
3. **Python Thermodynamics & Balance Engine (Phases 02 & 03)**:
   A dedicated Python service (`http://localhost:8765`) utilizing CoolProp and authoritative sugar thermodynamic equations to execute full mass, energy, and component balance simulations.

## 2. Layered Architecture

To prevent architectural debt and ensure mathematical rigor, the system enforces a 5-layer separation:

```text
┌────────────────────────────────────────────────────────┐
│  Presentation Layer (Visio Canvas / Web UI Ribbon)     │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Application Logic (Event Handlers, Validation, Dialogs)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  API Gateway & Serialization (JSON Schema v1.0)        │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Thermodynamic & Balance Engine (CoolProp, Solubility) │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│  Authoritative Domain Knowledge (Sugar's Help Book)    │
└────────────────────────────────────────────────────────┘
```

## 3. API Contract (Schema Version 1.0)

- **Base URL**: `http://localhost:8765`
- **Endpoints**:
  - `GET /status`: Health and engine version.
  - `POST /solve`: Solves full mass and energy balance for the complete graph.
  - `POST /validate`: Topology and input validation without solving.
  - `POST /export/excel`: Generates base64-encoded Excel balance report.
  - `GET /supersaturation`: Calculates $S_s$ from dry substance, purity, temperature, and solubility coefficients.
- **Protocol Rules**:
  - HTTP 200 returned for all completed solver runs (with `converged: true/false`).
  - HTTP 500 reserved strictly for unexpected runtime crashes.
  - Internal calculations run exclusively in SI units.
