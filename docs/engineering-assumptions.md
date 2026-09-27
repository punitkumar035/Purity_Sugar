# Engineering Assumptions Log

In accordance with the Sugar Multi-Agent Development Protocol, any assumption made during engineering, modeling, or software development must be explicitly cataloged here.

| ID | Module / Station | Parameter / Behavior | Engineering Assumption | Literature / Justification | Approval Status |
|---|---|---|---|---|---|
| **ASM-001** | General | Phase 01 Codebase | Visio VBA files (`files (4)/`) are strictly locked and serve as reference baseline. | Rulebook v5.0 §PART A | APPROVED (Locked) |
| **ASM-002** | Thermodynamics | Water & Steam Properties | NIST REFPROP/IAPWS-95 formulations via CoolProp + `WATER.FLD` replace all IF-97 approximations. | RULES v5.0 §B2 | APPROVED |
| **ASM-003** | Solubility | Wagnerowski Validity | Wagnerowski equation applied only when $c = 0$ AND $1.6 \le \text{NSW} \le 3.5$; otherwise Vavrinecz is selected. | RULES v5.0 §B3.3 | APPROVED |
| **ASM-004** | Crystallization | Enthalpy of Phase Change | Crystallization releases $+54.9\text{ kJ/kg}$ sucrose; dissolution absorbs $-54.9\text{ kJ/kg}$. | RULES v5.0 §B7 | APPROVED |
| **ASM-005** | Centrifugals | Pure Crystal Properties | Sucrose crystals entering or leaving are assumed 100% pure ($DS_{cs} = 1.0, PU_{cs} = 1.0$). | RULES v5.0 §B4.2 | APPROVED |
| **ASM-006** | Evaporators / Pans | Vapor Exit State | Vapor leaves at saturation temperature $T_{\text{sat}}(P_{\text{vapor}})$; liquid exits at $T_{\text{boil}} = T_{\text{sat}} + \text{BPE}$. | RULES v5.0 §B6.1 | APPROVED |
| **ASM-007** | Stations | Atmospheric Pressure Out | Melters, atmospheric tanks, and centrifugals output liquid streams at ambient atmospheric pressure ($101.325\text{ kPa}$). | RULES v5.0 §A8 | APPROVED |
