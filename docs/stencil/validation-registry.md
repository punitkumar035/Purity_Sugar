# Sugar Engineering Validation Registry

> **Authoritative Basis**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **Agent 9: Sugar Stencil Architect**  
> **Severity Levels**:
> - `FATAL_ERROR`: Physical impossibility or model singularity. Calculation is aborted immediately.
> - `ENGINEERING_WARNING`: Outside typical operational range. Calculation proceeds with an explicit user notification.
> - `INFORMATION`: Valid configuration requiring operational awareness.

---

## 1. Master Validation Rules

| Rule ID | Target Field | Severity | Condition / Trigger | Message / Engineering Rationale |
|---|---|---|---|---|
| **VAL-GEN-001** | Any Flow Rate | FATAL_ERROR | $\text{Flow} < 0.0$ | Mass flow rate cannot be negative. Negative flow violates mass conservation. |
| **VAL-GEN-002** | Any Dry Substance / Brix | FATAL_ERROR | $\text{Brix} < 0.0$ or $\text{Brix} > 100.0$ | Dry substance fraction must remain bounded between $0.0$ and $1.0$ ($0–100\%$). |
| **VAL-GEN-003** | Any Apparent / True Purity | FATAL_ERROR | $\text{Purity} < 0.0$ or $\text{Purity} > 100.5$ | Sugar solution purity cannot exceed 100% (allowing +0.5% analytical tolerance). |
| **VAL-GEN-004** | Component Fractions Sum | FATAL_ERROR | $|\sum c_i - 100.0\%| > 0.01\%$ | Sum of 15 stream components must equal exactly 100.0%. Missing mass violates closure. |
| **VAL-GEN-005** | Absolute Pressure | FATAL_ERROR | $P_{abs} \le 0.0\text{ kPa}$ | Absolute pressure must strictly exceed zero absolute vacuum. |
| **VAL-GEN-006** | Temperature vs Saturation | ENGINEERING_WARNING | $T_{liquid} > T_{sat}(P) + 15^\circ\text{C}$ | Liquid temperature significantly exceeds saturation; spontaneous boiling or thermal degradation expected. |
| **VAL-GEN-007** | Steam Quality | FATAL_ERROR | $x < 0.0$ or $x > 1.0$ | Saturated steam dryness fraction must remain between $0.0$ (liquid) and $1.0$ (dry vapour). |
| **VAL-MILL-001** | Cane Crushing Rate | ENGINEERING_WARNING | $\text{TCH} < 50.0$ or $\text{TCH} > 1500.0$ | Crushing rate outside typical factory capacity bounds. |
| **VAL-MILL-002** | Imbibition Water % Cane | ENGINEERING_WARNING | $\% < 15.0\%$ or $\% > 45.0\%$ | Imbibition water addition outside standard milling range ($20–35\%$ typical). |
| **VAL-MILL-003** | Bagasse Moisture % | ENGINEERING_WARNING | $M < 45.0\%$ or $M > 54.0\%$ | Bagasse moisture outside normal 48–51% mill delivery range. Affects boiler combustion. |
| **VAL-EVAP-001** | Evaporator Syrup Brix | FATAL_ERROR | $\text{Brix}_{out} \le \text{Brix}_{in}$ | Evaporation effect requires target syrup Brix to exceed incoming juice Brix. |
| **VAL-EVAP-002** | Evaporator Syrup Brix Limit | ENGINEERING_WARNING | $\text{Brix}_{out} > 72.0^\circ\text{Brix}$ | Syrup Brix $> 72^\circ$ risks premature sucrose crystallization inside calandria tubes. |
| **VAL-EVAP-003** | Evaporator Temperature Drop | FATAL_ERROR | $T_{steam,in} \le T_{boil,juice}$ | Driving temperature difference $\Delta T = T_{steam} - T_{boil}$ must be positive for heat transfer. |
| **VAL-PAN-001** | Massecuite Target DS | FATAL_ERROR | $DS_{mc} \le DS_{feed}$ | Pan evaporative crystallization requires massecuite DS to exceed process syrup feed DS. |
| **VAL-PAN-002** | Pan Supersaturation Range | ENGINEERING_WARNING | $SS < 1.00$ or $SS > 1.25$ | $SS < 1.0$ causes crystal melting; $SS > 1.25$ causes uncontrolled false grain nucleation. |
| **VAL-PAN-003** | Mother Liquor Purity | FATAL_ERROR | $PU_{ml} \ge PU_{mc}$ | Mother liquor purity must be strictly lower than massecuite purity due to sucrose crystallization. |
| **VAL-CENT-001** | Centrifugal Wash Water | ENGINEERING_WARNING | $\text{Wash Ratio} > 0.08\text{ kg/kg}$ | Excessive wash water ($> 8\%$) causes severe sugar crystal dissolution and energy recycling. |
| **VAL-CENT-002** | Sugar Pol / Purity | FATAL_ERROR | $\text{Pol} < PU_{mc}$ | Centrifuged sugar purity must exceed incoming massecuite purity. |
| **VAL-MELT-001** | Target Melt Brix | FATAL_ERROR | $\text{Brix}_{melt} \ge \text{Brix}_{sugar}$ | Melt liquor Brix must be lower than incoming crystal sugar Brix ($99.5\%$). |
| **VAL-FLASH-001** | Flash Pressure | FATAL_ERROR | $P_{flash} \ge P_{feed}$ | Flash tank requires vessel pressure to be lower than feed liquor saturation pressure. |

---

## 2. Engineering Warning Action Matrix

```text
VALIDATION CHECK
       │
       ├──[ Passes All Limits ] ─────────────→ STATUS: PASS (Proceed to Solver)
       │
       ├──[ Violates Range Limit ] ──────────→ STATUS: WARNING
       │                                        ├── Notification logged in Solver Audit
       │                                        └── Solver continues with flagged parameter
       │
       └──[ Violates Physical Boundary ] ────→ STATUS: FATAL_ERROR
                                                ├── Solver execution halted
                                                └── Exact physical cause displayed to user
```
