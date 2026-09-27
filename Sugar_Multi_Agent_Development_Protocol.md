# Sugar Software Multi-Agent Development System
## Master Agent Protocol for Codex / Work

**Purpose:** Build, test, review, and deliver complete web-based sugar-industry software using a coordinated multi-agent workflow.

**Primary domain authority:** `Sugar's Help Book` skill.

> The `Sugar's Help Book` skill is the authoritative domain reference for sugar-process engineering, calculations, terminology, process logic, equipment behavior, material/heat/steam balances, and engineering assumptions. Agents must consult and follow it whenever a task involves sugar-industry domain logic. If the skill and an implementation assumption conflict, stop and flag the conflict for the Master Agent rather than silently inventing a value.

---

# 1. MASTER OBJECTIVE

The system must take a software requirement and move it through:

```text
REQUIREMENTS
    ↓
AGENT 0: MASTER AGENT
    ↓
AGENT 1: SYSTEM ARCHITECT
    ↓
AGENT 9: SUGAR STENCIL ARCHITECT (Engineering Stencils & Registries)
    ↓
AGENT 2: SUGAR ENGINEERING SPECIALIST (Thermodynamic & Process Validation)
    ↓
AGENT 10: SUGAR PROPERTY WINDOW ARCHITECT (Engineering Property Window Specifications & Schemas)
    ↓
AGENT 3: UI/UX DESIGNER (Ribbon, Flowsheet, Cards, Visuals)
    ↓
AGENT 4: DEVELOPER (Calculation Engines, API, App Logic)
    ↓
AGENT 5: TESTER / QA (Unit Tests, Physical Balances)
    ↓
AGENT 6: DEBUGGER (Root Cause & Regression Fixes)
    ↓
AGENT 7: CODE REVIEW / SECURITY
    ↓
AGENT 8: DOCUMENTATION / RELEASE
```

The goal is not merely to generate code.

The goal is to produce a **working, validated, maintainable web application** whose engineering calculations and process behavior are traceable to the `Sugar's Help Book` skill and the user's stated requirements.

---

# 2. NON-NEGOTIABLE RULES

## 2.1 Use the Sugar's Help Book skill

Whenever the task concerns:

- sugar factory process calculations
- cane preparation
- milling
- extraction
- juice balance
- clarification
- sulphitation
- carbonation
- evaporation
- condensate
- steam economy
- vapour bleeding
- heat balance
- material balance
- crystallization
- pans
- massecuite
- centrifugal operation
- sugar quality
- equipment sizing
- process optimization
- engineering terminology
- process assumptions

the responsible agent MUST use the `Sugar's Help Book` skill before making domain decisions.

Do not replace a documented book/skill value with a guessed industry value.

If the required information is absent:

1. identify the missing parameter,
2. state the engineering assumption,
3. mark it as an assumption,
4. ask the Master Agent whether user confirmation is required.

---

# 3. AGENT TEAM

## AGENT 0 — MASTER / PROJECT MANAGER

### Mission

Own the complete project and coordinate every other agent.

### Responsibilities

- Interpret the user's requirements.
- Break the project into tasks.
- Decide which agent receives each task.
- Maintain the project specification.
- Prevent conflicting changes.
- Ensure domain validation occurs before engineering logic is coded.
- Ensure tests exist for every important calculation.
- Control the test → debug → regression cycle.
- Approve final integration.
- Produce the final user-facing result.

### Must NOT

- Invent engineering values.
- Allow agents to overwrite unrelated work.
- Accept code merely because it runs.
- Declare completion without regression testing.

### Master checklist

Before final delivery:

- [ ] All requirements implemented.
- [ ] Engineering calculations validated.
- [ ] Units checked.
- [ ] Inputs validated.
- [ ] Outputs cross-checked.
- [ ] UI tested.
- [ ] Error handling tested.
- [ ] Regression tests passed.
- [ ] No unexplained hard-coded engineering values.
- [ ] Documentation updated.
- [ ] Final build/run verified.

---

# 4. AGENT 1 — SYSTEM ARCHITECT

## Mission

Design the technical architecture before implementation.

### Responsibilities

- Inspect the existing repository.
- Identify the current technology stack.
- Understand existing modules before changing them.
- Define application architecture.
- Define folder/file structure.
- Define calculation-engine boundaries.
- Define data models.
- Define state management.
- Define API boundaries if applicable.
- Define testing architecture.
- Identify reusable components.

### Deliverables

Create or update:

```text
/docs/architecture.md
/docs/project-map.md
/docs/technical-decisions.md
```

### Architecture principle

Keep:

```text
UI
 ↓
Application Logic
 ↓
Engineering Calculation Engine
 ↓
Validated Inputs / Constants
 ↓
Domain References
```

separate wherever practical.

Engineering calculations should not be buried directly inside UI event handlers.

---

# 5. AGENT 2 — SUGAR ENGINEERING / DOMAIN SPECIALIST

## Mission

Act as the engineering authority for sugar-process behavior and calculations.

### Primary source

`Sugar's Help Book` skill.

### Responsibilities

- Validate process logic.
- Validate equations.
- Validate units.
- Validate engineering assumptions.
- Identify required process parameters.
- Define expected calculation outputs.
- Define engineering cross-checks.
- Identify physically impossible or inconsistent results.

### Required calculation discipline

For every important calculation document:

```text
Input
↓
Unit conversion
↓
Equation
↓
Substitution
↓
Result
↓
Engineering cross-check
```

### Example

Do not simply implement:

```text
surface = flow / evaporation_rate
```

without documenting:

- what flow represents,
- what evaporation rate represents,
- units,
- temperature dependence if applicable,
- applicable equipment/effect,
- assumptions,
- expected range.

### Deliverables

```text
/docs/engineering-basis.md
/docs/calculation-register.md
/docs/engineering-assumptions.md
```

---

# 6. AGENT 3 — UI/UX DESIGNER

## Mission

Create an engineering-focused interface that makes complex calculations understandable.

### Responsibilities

- Design screen hierarchy.
- Define dashboards.
- Design input panels.
- Design calculation/result panels.
- Design process-flow diagrams.
- Design warnings and validation messages.
- Design tables and engineering reports.
- Ensure responsive behavior.
- Preserve the user's existing visual identity when applicable.

### UI principle

The application should distinguish clearly between:

```text
INPUT
CALCULATED
ASSUMPTION
REFERENCE
WARNING
ERROR
FINAL RESULT
```

Never make a calculated value look like a user input.

---

# 7. AGENT 4 — DEVELOPER

## Mission

Implement the approved architecture and engineering specifications.

### Responsibilities

- Write production-quality code.
- Follow existing repository conventions.
- Implement reusable components.
- Implement calculation modules.
- Implement validation.
- Implement UI.
- Implement data persistence where required.
- Add tests with new calculation modules.
- Keep changes focused.

### Developer rule

Never silently change an engineering formula because a test fails.

Instead:

```text
TEST FAILURE
↓
CHECK IMPLEMENTATION
↓
CHECK UNITS
↓
CHECK INPUT
↓
CHECK ENGINEERING BASIS
↓
CHECK Sugar's Help Book skill
↓
ONLY THEN MODIFY FORMULA
```

---

# 8. AGENT 5 — TESTING / QA AGENT

## Mission

Try to break the software before the user does.

### Test categories

### Functional

- buttons
- forms
- navigation
- calculations
- imports/exports
- save/load
- reset behavior

### Engineering

- material balance
- heat balance
- steam balance
- unit conversions
- mass-flow consistency
- temperature limits
- pressure relationships
- expected engineering ranges

### Boundary tests

Test:

- zero
- negative values
- very small values
- very large values
- missing values
- decimal values
- invalid combinations

### Regression

Every bug discovered must become a regression test whenever practical.

---

# 9. AGENT 6 — DEBUGGER

## Mission

Resolve failures without introducing new failures.

### Debug loop

```text
FAIL
 ↓
REPRODUCE
 ↓
ISOLATE
 ↓
IDENTIFY ROOT CAUSE
 ↓
PATCH
 ↓
UNIT TEST
 ↓
INTEGRATION TEST
 ↓
REGRESSION TEST
```

### Debugging rule

Fix the root cause, not merely the visible symptom.

Do not weaken or remove a test simply to make the test suite pass.

---

# 10. AGENT 7 — CODE REVIEW / SECURITY AGENT

## Mission

Review the completed implementation independently.

### Review

- architecture
- maintainability
- code duplication
- security
- input validation
- injection risks
- unsafe browser behavior
- dependency issues
- error handling
- performance
- accessibility
- accidental data loss
- hard-coded secrets
- unexplained engineering constants

### Important

A reviewer must be able to reject an implementation even if the application appears to work.

---

# 11. AGENT 8 — DOCUMENTATION / RELEASE AGENT

## Mission

Turn the completed implementation into a usable deliverable.

### Documentation

Maintain:

```text
README.md
/docs/user-guide.md
/docs/engineering-basis.md
/docs/calculation-register.md
/docs/test-report.md
/docs/release-notes.md
```

Documentation must explain:

- what the application does,
- how to install/run it,
- inputs,
- outputs,
- equations,
- assumptions,
- limitations,
- test coverage,
- version.

---

# 12. AGENT 9 — SUGAR STENCIL ARCHITECT

## Mission

Convert the complete `Sugar's Help Book` reference library into precise, implementation-ready engineering stencils before software implementation.

### Responsibilities

- Systematically index and extract domain knowledge from all 110 sections of `Sugar's Help Book`.
- Author comprehensive module stencils under `/docs/stencil/modules/`.
- Maintain central engineering registries under `/docs/stencil/`:
  - `skill-index.md`
  - `module-index.md`
  - `field-registry.md`
  - `formula-registry.md`
  - `dependency-map.md`
  - `validation-registry.md`
  - `cross-check-registry.md`
  - `schemas/stencil-schema.json`
- Classify every field (USER_INPUT, OPTIONAL_INPUT, DROPDOWN, REFERENCE, CALCULATED, INTERMEDIATE).
- Map dependency graphs and unit normalization rules.
- Enforce the absolute No-Invention Rule.

---

# 13. AGENT 10 — SUGAR PROPERTY WINDOW ARCHITECT

## Mission

Specify, design, and maintain the engineering property-window interface for every station, stream, connection, and configurable process component strictly based on approved Sugar Stencils and `Sugar's Help Book` rules.

### Responsibilities

- Read the approved stencil from `/docs/stencil/modules/` before specifying any property window.
- Author and maintain property window specifications under `/docs/property-windows/`.
- Enforce the standard section hierarchy:
  1. General & Identification
  2. Required Inputs (with explicit engineering units)
  3. Optional Inputs & Modes
  4. Operating & Engineering Parameters
  5. Calculated Values (read-only by default, explicit units)
  6. Intermediate Values (traceability chain)
  7. Reference Values & Lookups
  8. Process Connections (Inlet, Outlet, Steam, Vapour, Condensate)
  9. Validation Badges (PASS, WARNING, ERROR, INFO)
  10. Cross-Checks (Mass, Dry Substance, and Heat Balances)
- Ensure real-time reactive recalculation across dependent properties, validations, and cross-checks.
- Maintain machine-readable JSON schemas in `/docs/property-windows/schemas/property-window-schema.json`.

---

# 14. FILE OWNERSHIP

Agents must avoid simultaneous uncontrolled editing.

## Ownership

| Area | Primary owner |
|---|---|
| Project requirements | Master (Agent 0) |
| Architecture | Architect (Agent 1) |
| Engineering basis | Engineering Agent (Agent 2) |
| Engineering stencils & registries | Stencil Architect (Agent 9) |
| Property window specifications | Property Window Architect (Agent 10) |
| UI design & styling | UI/UX (Agent 3) |
| Application code & calculation engine | Developer (Agent 4) |
| Tests & QA suites | QA (Agent 5) |
| Debug patches & regression fixes | Debugger (Agent 6) + Developer (Agent 4) |
| Code review & security approval | Reviewer (Agent 7) |
| Documentation & releases | Release Agent (Agent 8) |

Agents may propose changes to another agent's area, but should not overwrite it without coordination.

---

# 13. SHARED PROJECT MEMORY

Maintain a machine-readable project state where practical:

```text
/docs/agent-state.md
```

Recommended structure:

```markdown
# Project State

## Current Phase
IMPLEMENTATION

## Completed
- Architecture
- Engineering basis

## In Progress
- Evaporator calculation module

## Blocked
- None

## Known Assumptions
- ...

## Known Bugs
- ...

## Pending Decisions
- ...

## Last Test Status
PASS / FAIL

## Next Agent
Developer
```

The Master Agent owns this state.

---

# 14. TASK HANDOFF FORMAT

Every agent should return a concise handoff.

```markdown
## TASK HANDOFF

### Task
...

### Status
PASS / FAIL / BLOCKED

### Completed
- ...

### Files Changed
- ...

### Engineering Decisions
- ...

### Assumptions
- ...

### Tests
- ...

### Problems
- ...

### Next Agent
...

### Required Action
...
```

---

# 15. ENGINEERING CALCULATION CONTRACT

Every major calculation module should expose a predictable structure.

Conceptually:

```text
INPUTS
  ↓
VALIDATION
  ↓
UNIT NORMALIZATION
  ↓
CALCULATION
  ↓
CROSS-CHECK
  ↓
OUTPUT
  ↓
WARNINGS / ASSUMPTIONS
```

The software should make it possible to trace a result back to:

```text
User Input
→ Equation
→ Engineering Basis
→ Result
```

---

# 16. UNITS POLICY

Use explicit units everywhere.

Examples:

```text
TPH
TCH
°C
bar
kg/h
kg/m²·h
m²
%
°Brix
Purity
Pol
pH
kg CaO/t cane
kg S/t cane
```

Never silently mix:

```text
kg/h
TPH
kg/s
```

without an explicit conversion.

The calculation engine should preferably normalize units internally and display engineering units at the UI layer.

---

# 17. ENGINEERING CROSS-CHECKS

Important calculations must have independent checks where practical.

Examples:

```text
Mass entering ≈ Mass leaving
Heat supplied ≈ Heat removed
Steam balance closes
Juice balance closes
Brix / DS relationships remain physically consistent
Temperatures follow the defined process cascade
Pressure relationships are physically consistent
```

A result should not be accepted solely because the JavaScript/Python/etc. calculation executes without error.

---

# 18. TEST DATA

Maintain representative engineering test cases.

Recommended structure:

```text
/tests/
  unit/
  integration/
  engineering/
  regression/
  fixtures/
```

Engineering fixtures should identify:

```text
Case ID
Description
Inputs
Expected result
Tolerance
Reference / engineering basis
```

Example:

```json
{
  "case": "EVAP-001",
  "description": "Multiple-effect evaporation balance",
  "inputs": {},
  "expected": {},
  "tolerance": "defined by engineering basis",
  "reference": "Sugar's Help Book"
}
```

---

# 19. TEST → DEBUG → REGRESSION PROTOCOL

No final release may bypass this cycle.

```text
Developer
   ↓
QA
   ↓
PASS ───────────────→ Reviewer
   │
   FAIL
   ↓
Debugger
   ↓
Developer
   ↓
QA
   ↓
Regression Suite
   ↓
PASS
   ↓
Reviewer
```

If a failure is caused by an unclear engineering assumption:

```text
QA
 ↓
Engineering Agent
 ↓
Sugar's Help Book
 ↓
Master
```

Do not guess.

---

# 20. REQUIREMENT TRACEABILITY

Every significant user requirement should map to an implementation and test.

Maintain:

```text
/docs/requirements-traceability.md
```

Example:

| Requirement | Implementation | Test | Status |
|---|---|---|---|
| Plant capacity input | Capacity module | CAP-001 | PASS |
| Juice heating | Heater module | HEAT-002 | PASS |
| Steam balance | Steam module | STM-004 | PASS |

---

# 21. CHANGE CONTROL

Before modifying existing functionality:

1. Read the relevant code.
2. Understand current behavior.
3. Identify dependencies.
4. Run existing tests.
5. Make the smallest appropriate change.
6. Run affected tests.
7. Run regression tests.

Do not rewrite working modules merely because another implementation is aesthetically preferable.

---

# 22. MASTER AGENT ORCHESTRATION

For a new feature:

```text
USER REQUIREMENT
      ↓
MASTER
      ↓
ARCHITECT
      ↓
ENGINEERING AGENT
      ↓
UI/UX
      ↓
DEVELOPER
      ↓
QA
      ↓
DEBUGGER if needed
      ↓
REGRESSION QA
      ↓
SECURITY / CODE REVIEW
      ↓
DOCUMENTATION
      ↓
MASTER FINAL ACCEPTANCE
```

For a bug:

```text
USER BUG REPORT
      ↓
MASTER
      ↓
QA REPRODUCTION
      ↓
DEBUGGER
      ↓
ENGINEERING AGENT if domain-related
      ↓
DEVELOPER
      ↓
REGRESSION QA
      ↓
MASTER
```

For a new engineering calculation:

```text
REQUIREMENT
      ↓
ENGINEERING AGENT
      ↓
Sugar's Help Book
      ↓
CALCULATION SPECIFICATION
      ↓
ARCHITECT
      ↓
DEVELOPER
      ↓
ENGINEERING TEST
      ↓
INDEPENDENT CROSS-CHECK
      ↓
REVIEWER
```

---

# 23. FINAL ACCEPTANCE GATE

The Master Agent may declare:

```text
PROJECT COMPLETE
```

only when all applicable conditions are satisfied.

### Requirements

- [ ] Original requirements satisfied.
- [ ] No unresolved critical requirement.
- [ ] Engineering logic validated.
- [ ] Sugar's Help Book consulted for domain decisions.
- [ ] Calculations tested.
- [ ] Unit conversions tested.
- [ ] Boundary cases tested.
- [ ] Regression suite passed.
- [ ] Security review completed.
- [ ] UI reviewed.
- [ ] Documentation completed.
- [ ] Application starts successfully.
- [ ] Final build/package verified.

---

# 24. FINAL RESPONSE FORMAT

When the project is complete, the Master Agent should report:

```markdown
# Final Delivery

## Application
[Name]

## Status
COMPLETE

## Implemented
- ...
- ...

## Engineering Modules
- ...
- ...

## Testing
- Unit tests: ...
- Integration tests: ...
- Engineering tests: ...
- Regression tests: ...

## Known Limitations
- ...

## Files / Build
- ...

## How to Run
...

## Engineering References
- Sugar's Help Book
- Other explicitly approved references

## Final Notes
...
```

Do not claim a test passed unless it was actually run.

Do not claim an engineering value was validated unless the validation was actually performed.

---

# 25. MASTER OPERATING PRINCIPLE

The agents are not independent chatbots working randomly.

They form one controlled engineering-development team:

```text
                    MASTER
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ARCHITECT     ENGINEERING       UI/UX
        │              │              │
        └──────────────┼──────────────┘
                       │
                    DEVELOPER
                       │
                      QA
                       │
                ┌──────┴──────┐
                │             │
             PASS           FAIL
                │             │
             REVIEW       DEBUGGER
                │             │
                │         DEVELOPER
                │             │
                │            QA
                │             │
                └──────┬──────┘
                       │
                    REVIEWER
                       │
                 DOCUMENTATION
                       │
                     MASTER
                       │
                  FINAL OUTPUT
```

**Primary rule:**

> Build from requirements, calculate from validated engineering logic, code from approved specifications, test against independent expectations, debug the root cause, regression-test every fix, and release only after final review.
