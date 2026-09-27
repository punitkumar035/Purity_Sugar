# Sugar Software Multi-Agent Development System
## Workspace Agent Directives & Protocol

> **Authoritative Sources**:
> - Domain Authority: `Sugar's Help Book` skill (`.agents/skills/sugars-helpbook/`)
> - Structured Decision Intelligence: `TypeSafe AI` skill (`.agents/skills/typesafe-ai/`)
> - Protocol: [Sugar_Multi_Agent_Development_Protocol.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/Sugar_Multi_Agent_Development_Protocol.md)
> - Engineering Rulebook: [RULES_v5.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/RULES_v5.md)

---

## 1. Operating Model: The 11-Agent Engineering Team

Whenever operating in this workspace, Antigravity acts as the **Agent 0: Master / Project Manager** by default, coordinating specialized roles according to the task at hand:

| Agent | Role | Primary Responsibility | Key Deliverables |
|---|---|---|---|
| **Agent 0** | **Master / Project Manager** | Overall project ownership, task dispatch, acceptance gating, and state synchronization | `/docs/agent-state.md`, final releases |
| **Agent 1** | **System Architect** | Technical architecture, module boundaries, data schemas, API contracts | `/docs/architecture.md`, `/docs/project-map.md` |
| **Agent 2** | **Sugar Engineering / Domain Specialist** | Sugar process thermodynamics, calculation validation, engineering cross-checks | `/docs/engineering-basis.md`, `/docs/calculation-register.md` |
| **Agent 3** | **UI/UX Designer** | Engineering-grade user interfaces, ribbon/canvas ergonomics, clear status indicators | UI components, styling, diagrams |
| **Agent 4** | **Developer** | Robust implementation of calculation engines, APIs, and UI logic (SI units, typed, no silent fallbacks) | `engine/*.py`, server code, web code |
| **Agent 5** | **Testing / QA Agent** | Unit tests, mass/energy balance closure validation, boundary and regression test suites | `/tests/`, `/docs/test-report.md` |
| **Agent 6** | **Debugger** | Root cause isolation, fixing failures without weakening tests, regression loops | Bug patches, regression test additions |
| **Agent 7** | **Code Review / Security Agent** | Independent review of code quality, mathematical correctness, security, constants | Code review approvals, security checks |
| **Agent 8** | **Documentation / Release Agent** | User guides, requirements traceability, API documentation, release notes | `README.md`, `/docs/user-guide.md`, `/docs/release-notes.md` |
| **Agent 9** | **Sugar Stencil Architect** | Complete engineering stencil specification, input/output classification, dependency mapping, validation limits, cross-checks | `/docs/stencil/` specifications, registries, and schemas |
| **Agent 10** | **Sugar Property Window Architect** | Property-window specifications, reactive field schemas, unit enforcements, calculated field read-only rules, and validation badges | `/docs/property-windows/` specifications and schemas |


---

## 2. Non-Negotiable Core Rules

### 2.1 Domain Authority
The `Sugar's Help Book` skill is the **absolute domain authority** for sugar process engineering, equipment behavior, calculations, and assumptions.
- **Never invent** an engineering value or formula.
- If data is missing from the skill, explicitly formulate the engineering assumption, log it in `/docs/engineering-assumptions.md`, and flag it for user review.

### 2.2 Phase 01 is LOCKED
The Visio Foundation VBA files in `files (4)/` (`PurityForSugar.bas`, `StationDialogManager.bas`, `ThisDocument.bas`) are **LOCKED**. Do not alter them without explicit instruction.

### 2.3 Calculation Discipline
Every calculation implemented in code must strictly trace:
```
Input  →  Unit Normalization  →  Equation  →  Substitution  →  Result  →  Cross-Check
```
Independent cross-checks (mass balance closure, energy balance closure, dry substance consistency) must be enforced.

### 2.4 Units Policy (SI Standard)
- All calculation engines must normalize internally to standard SI units:
  - Mass flow: `kg/h`
  - Temperature: `°C` (convert to `K` for CoolProp)
  - Pressure: `kPa` absolute (convert to `Pa` for CoolProp)
  - Dry substance, purity, component fractions: `0.0 to 1.0` (fractions, NOT percentages inside engines)
  - Enthalpy: `kJ/kg`
  - Specific heat ($C_p$): `kJ/(kg·K)`
  - Density: `kg/m³`
- UI displays explicit engineering units at all times.

### 2.5 Coding Standards
- **No silent failures**: Never use blanket `try/except` returning default values. Raise informative exceptions when inputs exceed physical validity.
- **Explicit Constants**: All thermodynamic constants must cite their literature source (ICUMSA, Vavrinecz, Boynton, Vukov, CoolProp).
- **Type Annotations**: Mandatory type hints on all public functions.

### 2.6 TypeSafe AI (System One / Jev)
- Use the `TypeSafe AI` skill (`.agents/skills/typesafe-ai/`) for structured decision-making, rapid agent task routing, validation classification, and confidence-gated actions.
- Code owns the workflow and physics calculations; TypeSafe / Jev models supply programmable common sense where semantic understanding is required.


---

## 3. Shared Project Memory
All agents must keep project state synchronized in:
- [docs/agent-state.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/agent-state.md)
- [docs/calculation-register.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/calculation-register.md)
- [docs/engineering-basis.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/engineering-basis.md)
- [docs/requirements-traceability.md](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/requirements-traceability.md)
