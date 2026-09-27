# Master Agent Protocol & Workflow Lifecycle

Derived from `Sugar_Multi_Agent_Development_Protocol.md`.

## 1. Master Objective
Build, test, review, and deliver complete, mathematically validated sugar-industry software. Every engineering calculation and process behavior must be traceable to the `Sugar's Help Book` skill and verified requirements.

## 2. Agent Team Coordination Matrix
The Master Agent (Agent 0) orchestrates all specialized agents:

```text
                    MASTER AGENT (0)
                           │
            ┌──────────────┼──────────────┐
            │              │              │
       ARCHITECT (1)  ENGINEERING (2)  UI/UX (3)
            │              │              │
            └──────────────┼──────────────┘
                           │
                     DEVELOPER (4)
                           │
                        QA (5)
                           │
                    ┌──────┴──────┐
                    │             │
                 PASS           FAIL
                    │             │
                 REVIEW       DEBUGGER (6)
                    │             │
                    │         DEVELOPER (4)
                    │             │
                    │            QA (5)
                    │             │
                    └──────┬──────┘
                           │
                   REVIEWER / SEC (7)
                           │
                   DOCUMENTATION (8)
                           │
                     MASTER AGENT (0)
                           │
                      FINAL OUTPUT
```

## 3. Workflows by Task Type

### 3.1 Feature Workflow
1. **User Requirement** received by Master Agent.
2. **Architect** defines structure, interfaces, boundaries (`/docs/architecture.md`).
3. **Engineering Specialist** establishes thermodynamic basis, equations, and literature sources (`/docs/engineering-basis.md`).
4. **UI/UX Designer** creates interface specs, state representations, and layout.
5. **Developer** writes code with strict typing and no silent failures.
6. **QA Tester** runs functional, boundary, and engineering balance tests.
7. **Debugger** isolates and patches root causes if tests fail.
8. **Code Reviewer** validates security, mathematical consistency, and constants.
9. **Documentation Agent** updates manuals, registers, and traceability.
10. **Master Agent** reviews the Final Acceptance Gate.

### 3.2 Bug Fix Workflow
```text
BUG REPORT → MASTER → QA REPRODUCTION → DEBUGGER ROOT CAUSE → ENGINEERING CHECK (if domain) → DEVELOPER PATCH → REGRESSION TEST → REVIEW → MASTER
```

### 3.3 New Calculation Workflow
```text
REQUIREMENT → ENGINEERING SPECIALIST (Sugar's Help Book) → CALCULATION SPEC → ARCHITECT → DEVELOPER → INDEPENDENT CROSS-CHECK → QA → REVIEWER
```

## 4. Standard Task Handoff Format
Every handoff between agents must follow this markdown format:

```markdown
## TASK HANDOFF

### Task
[Brief task statement]

### Status
[PASS / FAIL / BLOCKED]

### Completed
- [List of accomplishments]

### Files Changed
- [file:///path/to/file]

### Engineering Decisions
- [Equations, constants, or assumptions applied]

### Assumptions
- [Any assumption logged in /docs/engineering-assumptions.md]

### Tests
- [Tests run, results, tolerances]

### Problems / Blockers
- [Unresolved items, ambiguities]

### Next Agent
[Agent Name]

### Required Action
[Specific instructions for next agent]
```

## 5. Final Acceptance Gate Checklist
Before declaring any phase or feature complete, the Master Agent must verify:
- [ ] Requirements implemented and traceable in `/docs/requirements-traceability.md`.
- [ ] Engineering calculations validated against `Sugar's Help Book`.
- [ ] Mass, energy, and component balance closures tested.
- [ ] All units explicitly normalized and documented.
- [ ] Zero, negative, extreme boundary conditions tested.
- [ ] Regression suite passed completely.
- [ ] Independent code & security review completed.
- [ ] `/docs/agent-state.md` updated.
- [ ] Application starts and runs successfully.
