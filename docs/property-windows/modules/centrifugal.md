# Centrifugal Station Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CENT-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/centrifugal.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `4` | **Object Tag Prefix**: `CFG`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for batch and continuous centrifugals separating massecuite into crystallized sugar, mother liquor (run-off), and wash syrup.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [CFG] CENTRIFUGAL STATION PROPERTY WINDOW    [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Equipment Tag            [_______] —        │
│    Separation Output Mode   [_______] —        │
│    Wash Water % on Massecuite [_______] %        │
│    Target Sugar Purity      [_______] %        │
│    Mother Liquor / Run-off Purity [_______] %        │
│    Sugar Moisture (% on Sugar) [_______] %        │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Discharged Sugar Flow    [_______] TPH      🔒│
│    Discharged Mother Liquor Flow [_______] TPH      🔒│
│    Crystal Yield on Massecuite [_______] %        🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
│    Crystal Dissolved by Wash [_______] TPH      ⓘ │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Overall Centrifugal Mass  [PASS / tol < 0.05%] │
│    ✓ Dry Substance Closure     [PASS / tol < 0.02%] │
│    ✓ Sucrose Inventory Balance [PASS / tol < 0.02%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `equipmentTag` | **Equipment Tag** | `USER_INPUT` | `string` | `—` | YES | YES | Plant tag (e.g. A_CENT_1, B_CONT_1) |
| `stationTypeCode` | **Station Type Code** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | SUGARS station type code 4 |
| `separationMode` | **Separation Output Mode** | `DROPDOWN` | `select` | `—` | YES | YES | Selection of 2 or 3 product liquor discharges |
| `washWaterPercent` | **Wash Water % on Massecuite** | `USER_INPUT` | `number` | `%` | YES | YES | Quantity of washing water injected per 100 kg massecuite |
| `sugarPurity` | **Target Sugar Purity** | `USER_INPUT` | `number` | `%` | YES | YES | Polarization / apparent purity of washed sugar product |
| `motherLiquorPurity` | **Mother Liquor / Run-off Purity** | `USER_INPUT` | `number` | `%` | YES | YES | Purity of mother liquor escaping basket screens |
| `sugarMoisture` | **Sugar Moisture (% on Sugar)** | `USER_INPUT` | `number` | `%` | YES | YES | Moisture content of discharged wet sugar |
| `sugarFlow` | **Discharged Sugar Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Total commercial/raw sugar crystals discharged |
| `runoffFlow` | **Discharged Mother Liquor Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Total green/wash run-off molasses flow |
| `crystalRecovery` | **Crystal Yield on Massecuite** | `CALCULATED` | `number` | `%` | NO (Locked) | NO | Percentage of incoming crystal recovered in sugar |
| `dissolvedLoss` | **Crystal Dissolved by Wash** | `INTERMEDIATE` | `number` | `TPH` | NO (Locked) | NO | Loss of sucrose crystal due to water washing |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_mass` | **Overall Centrifugal Mass Balance** | `Massecuite_In + Wash_Water_In = Sugar_Out + Runoff_Out` | `±0.05` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_ds` | **Dry Substance Closure** | `Massecuite_In * DS_m = Sugar_Out * DS_s + Runoff_Out * DS_ro` | `±0.02` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_sucrose` | **Sucrose Inventory Balance** | `Massecuite_Sucrose = Sugar_Sucrose + Runoff_Sucrose` | `±0.02` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "centrifugal2",
  "title": "Centrifugal Station Property Window Specification",
  "stencilId": "STENCIL-CENT-01",
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
          "desc": "Plant tag (e.g. A_CENT_1, B_CONT_1)"
        },
        {
          "id": "stationTypeCode",
          "label": "Station Type Code",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "defaultValue": "4",
          "desc": "SUGARS station type code 4"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "separationMode",
          "label": "Separation Output Mode",
          "classification": "DROPDOWN",
          "type": "select",
          "options": [
            "2-Stream (Sugar + Run-off)",
            "3-Stream (Sugar + Molasses + Wash)"
          ],
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "defaultValue": "2-Stream (Sugar + Run-off)",
          "desc": "Selection of 2 or 3 product liquor discharges"
        },
        {
          "id": "washWaterPercent",
          "label": "Wash Water % on Massecuite",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 0.0,
          "max": 10.0,
          "defaultValue": 2.5,
          "desc": "Quantity of washing water injected per 100 kg massecuite"
        },
        {
          "id": "sugarPurity",
          "label": "Target Sugar Purity",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 90.0,
          "max": 99.9,
          "defaultValue": 99.5,
          "desc": "Polarization / apparent purity of washed sugar product"
        },
        {
          "id": "motherLiquorPurity",
          "label": "Mother Liquor / Run-off Purity",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 35.0,
          "max": 85.0,
          "defaultValue": 68.0,
          "desc": "Purity of mother liquor escaping basket screens"
        },
        {
          "id": "sugarMoisture",
          "label": "Sugar Moisture (% on Sugar)",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 0.1,
          "max": 3.0,
          "defaultValue": 0.8,
          "desc": "Moisture content of discharged wet sugar"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "sugarFlow",
          "label": "Discharged Sugar Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Centrifugal_Purge_Sugar(M_in, W_in, P_s, P_ml)",
          "desc": "Total commercial/raw sugar crystals discharged"
        },
        {
          "id": "runoffFlow",
          "label": "Discharged Mother Liquor Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "M_in + W_wash - F_sugar",
          "desc": "Total green/wash run-off molasses flow"
        },
        {
          "id": "crystalRecovery",
          "label": "Crystal Yield on Massecuite",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "%",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "F_sugar * (1 - Moisture) / (M_in * (Xc / 100))",
          "desc": "Percentage of incoming crystal recovered in sugar"
        }
      ]
    },
    {
      "id": "intermediate",
      "title": "Intermediate Traceability Values",
      "fields": [
        {
          "id": "dissolvedLoss",
          "label": "Crystal Dissolved by Wash",
          "classification": "INTERMEDIATE",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Xc_in - Sugar_Crystals_Out",
          "desc": "Loss of sucrose crystal due to water washing"
        }
      ]
    }
  ],
  "crossChecks": [
    {
      "id": "cc_mass",
      "name": "Overall Centrifugal Mass Balance",
      "rel": "Massecuite_In + Wash_Water_In = Sugar_Out + Runoff_Out",
      "tol": 0.05,
      "unit": "%"
    },
    {
      "id": "cc_ds",
      "name": "Dry Substance Closure",
      "rel": "Massecuite_In * DS_m = Sugar_Out * DS_s + Runoff_Out * DS_ro",
      "tol": 0.02,
      "unit": "%"
    },
    {
      "id": "cc_sucrose",
      "name": "Sucrose Inventory Balance",
      "rel": "Massecuite_Sucrose = Sugar_Sucrose + Runoff_Sucrose",
      "tol": 0.02,
      "unit": "%"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: Centrifugal Station Property Window Specification
Stencil ID: STENCIL-CENT-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
