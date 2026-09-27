# Vacuum Pan Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-PAN-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/vacuum-pan.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `8` | **Object Tag Prefix**: `PAN`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for batch and continuous vacuum boiling pans, governing syrup/molasses feeding, water evaporation, sucrose crystallization, crystal content, and massecuite dropping.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [PAN] VACUUM PAN PROPERTY WINDOW SPECIFICA   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Equipment Tag            [_______] —        │
│    Target Massecuite Brix   [_______] °Brix    │
│    Target Mother Liquor Purity [_______] %        │
│    Operating Pan Vacuum     [_______] kPa abs  │
│    Heating Vapour / Steam Pressure [_______] kPa abs  │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Crystal Content (% on Massecuite) [_______] %        🔒│
│    Massecuite Production Flow [_______] TPH      🔒│
│    Evaporated Vapour Flow   [_______] TPH      🔒│
│    Calandria Steam Demand   [_______] TPH      🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
│    Mother Liquor Supersaturation (Ss) [_______] —        ⓘ │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Total Mass Balance        [PASS / tol < 0.05%] │
│    ✓ Dry Substance Balance     [PASS / tol < 0.01%] │
│    ✓ Sucrose Balance           [PASS / tol < 0.01%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `equipmentTag` | **Equipment Tag** | `USER_INPUT` | `string` | `—` | YES | YES | Plant tag (e.g. A_PAN_1, C_PAN_2) |
| `stationTypeCode` | **Station Type Code** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | SUGARS station type code 8 |
| `massecuiteBrix` | **Target Massecuite Brix** | `USER_INPUT` | `number` | `°Brix` | YES | YES | Target dry substance of finished massecuite |
| `motherLiquorPurity` | **Target Mother Liquor Purity** | `USER_INPUT` | `number` | `%` | YES | YES | Target purity of mother liquor (run-off) |
| `panVacuum` | **Operating Pan Vacuum** | `USER_INPUT` | `number` | `kPa abs` | YES | YES | Absolute boiling pressure in pan head |
| `steamPressure` | **Heating Vapour / Steam Pressure** | `USER_INPUT` | `number` | `kPa abs` | YES | YES | Calandria supply vapour pressure |
| `crystalContent` | **Crystal Content (% on Massecuite)** | `CALCULATED` | `number` | `%` | NO (Locked) | NO | Percentage of solid sucrose crystals in total massecuite |
| `massecuiteFlow` | **Massecuite Production Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Total massecuite dropped per hour |
| `vapourFlow` | **Evaporated Vapour Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Water vaporized to pan condenser |
| `steamDemand` | **Calandria Steam Demand** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Heating steam or bleeding vapour required |
| `supersaturation` | **Mother Liquor Supersaturation (Ss)** | `INTERMEDIATE` | `number` | `—` | NO (Locked) | NO | Metastable driving force for crystal growth (1.05 - 1.25 typical) |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_mass` | **Total Mass Balance** | `Feed_In + Steam_In = Massecuite_Out + Vapour_Out + Condensate_Out` | `±0.05` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_ds` | **Dry Substance Balance** | `Feed_In * DS_Feed = Massecuite_Out * DS_Massecuite` | `±0.01` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_sucrose` | **Sucrose Balance** | `Feed_In * Sucrose_Feed = Massecuite_Out * Sucrose_Massecuite` | `±0.01` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "pan",
  "title": "Vacuum Pan Property Window Specification",
  "stencilId": "STENCIL-PAN-01",
  "engineeringBasis": "Sugar's Help Book",
  "sections": [
    {
      "id": "general",
      "title": "General & Identification",
      "fields": [
        {
          "id": "stationNumber",
          "label": "Station Number",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "min": 1,
          "max": 9999,
          "desc": "Unique plant station number"
        },
        {
          "id": "equipmentTag",
          "label": "Equipment Tag",
          "classification": "USER_INPUT",
          "type": "string",
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "desc": "Plant tag (e.g. A_PAN_1, C_PAN_2)"
        },
        {
          "id": "stationTypeCode",
          "label": "Station Type Code",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "defaultValue": "8",
          "desc": "SUGARS station type code 8"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "massecuiteBrix",
          "label": "Target Massecuite Brix",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0Brix",
          "editable": true,
          "required": true,
          "min": 85.0,
          "max": 96.0,
          "defaultValue": 91.5,
          "desc": "Target dry substance of finished massecuite"
        },
        {
          "id": "motherLiquorPurity",
          "label": "Target Mother Liquor Purity",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 40.0,
          "max": 90.0,
          "defaultValue": 72.0,
          "desc": "Target purity of mother liquor (run-off)"
        },
        {
          "id": "panVacuum",
          "label": "Operating Pan Vacuum",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "kPa abs",
          "editable": true,
          "required": true,
          "min": 15.0,
          "max": 40.0,
          "defaultValue": 20.0,
          "desc": "Absolute boiling pressure in pan head"
        },
        {
          "id": "steamPressure",
          "label": "Heating Vapour / Steam Pressure",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "kPa abs",
          "editable": true,
          "required": true,
          "min": 80.0,
          "max": 250.0,
          "defaultValue": 130.0,
          "desc": "Calandria supply vapour pressure"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "crystalContent",
          "label": "Crystal Content (% on Massecuite)",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "%",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "100 * (P_m - P_ml) / (100 - P_ml) * (DS_m / 100)",
          "desc": "Percentage of solid sucrose crystals in total massecuite"
        },
        {
          "id": "massecuiteFlow",
          "label": "Massecuite Production Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "F_feed * DS_feed / DS_massecuite",
          "desc": "Total massecuite dropped per hour"
        },
        {
          "id": "vapourFlow",
          "label": "Evaporated Vapour Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "F_feed - F_massecuite",
          "desc": "Water vaporized to pan condenser"
        },
        {
          "id": "steamDemand",
          "label": "Calandria Steam Demand",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Q_evap_pan / Latent_Heat_Vapour",
          "desc": "Heating steam or bleeding vapour required"
        }
      ]
    },
    {
      "id": "intermediate",
      "title": "Intermediate Traceability Values",
      "fields": [
        {
          "id": "supersaturation",
          "label": "Mother Liquor Supersaturation (Ss)",
          "classification": "INTERMEDIATE",
          "type": "number",
          "unit": "\u2014",
          "editable": false,
          "required": false,
          "precision": 3,
          "formula": "Van_Hook(C_sucrose, C_sat)",
          "desc": "Metastable driving force for crystal growth (1.05 - 1.25 typical)"
        }
      ]
    }
  ],
  "crossChecks": [
    {
      "id": "cc_mass",
      "name": "Total Mass Balance",
      "rel": "Feed_In + Steam_In = Massecuite_Out + Vapour_Out + Condensate_Out",
      "tol": 0.05,
      "unit": "%"
    },
    {
      "id": "cc_ds",
      "name": "Dry Substance Balance",
      "rel": "Feed_In * DS_Feed = Massecuite_Out * DS_Massecuite",
      "tol": 0.01,
      "unit": "%"
    },
    {
      "id": "cc_sucrose",
      "name": "Sucrose Balance",
      "rel": "Feed_In * Sucrose_Feed = Massecuite_Out * Sucrose_Massecuite",
      "tol": 0.01,
      "unit": "%"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: Vacuum Pan Property Window Specification
Stencil ID: STENCIL-PAN-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
