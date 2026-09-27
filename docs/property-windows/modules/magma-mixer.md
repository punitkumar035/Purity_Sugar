# Magma Mixer Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-MAGMA-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/magma-mixer.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `1` | **Object Tag Prefix**: `MGM`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for magma preparation vessels blending seed crystals (e.g. C-sugar) with syrup, molasses, or clarified juice to produce footing for vacuum boiling pans.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [MGM] MAGMA MIXER PROPERTY WINDOW SPECIFIC   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Equipment Tag            [_______] —        │
│    Target Magma Crystal Content [_______] %        │
│    Target Magma Brix        [_______] °Brix    │
│    Blending Medium Type     [_______] —        │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Prepared Magma Flow      [_______] TPH      🔒│
│    Blending Liquid Flow     [_______] TPH      🔒│
│    Resulting Magma Purity   [_______] %        🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Total Mass Balance Closur [PASS / tol < 0.0%] │
│    ✓ Dry Substance Balance     [PASS / tol < 0.0%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `equipmentTag` | **Equipment Tag** | `USER_INPUT` | `string` | `—` | YES | YES | Plant tag (e.g. C_MAGMA_MIX) |
| `stationTypeCode` | **Station Type Code** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | SUGARS station type code 1 |
| `targetCrystalContent` | **Target Magma Crystal Content** | `USER_INPUT` | `number` | `%` | YES | YES | Solid crystal content percentage in blended magma |
| `targetMagmaBrix` | **Target Magma Brix** | `USER_INPUT` | `number` | `°Brix` | YES | YES | Dry substance concentration of magma footing |
| `blendingLiquid` | **Blending Medium Type** | `DROPDOWN` | `select` | `—` | YES | YES | Liquid phase used to mingle sugar crystals |
| `magmaFlow` | **Prepared Magma Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Finished magma pumped to pan footing receivers |
| `liquidDemand` | **Blending Liquid Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Quantity of blending syrup/molasses added |
| `magmaPurity` | **Resulting Magma Purity** | `CALCULATED` | `number` | `%` | NO (Locked) | NO | Overall purity of prepared footing |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_mass` | **Total Mass Balance Closure** | `Sugar_In + Liquid_In = Magma_Out` | `±0.0` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_ds` | **Dry Substance Balance** | `Sugar_In * DS_s + Liquid_In * DS_liq = Magma_Out * DS_magma` | `±0.0` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "magma",
  "title": "Magma Mixer Property Window Specification",
  "stencilId": "STENCIL-MAGMA-01",
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
          "desc": "Plant tag (e.g. C_MAGMA_MIX)"
        },
        {
          "id": "stationTypeCode",
          "label": "Station Type Code",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "defaultValue": "1",
          "desc": "SUGARS station type code 1"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "targetCrystalContent",
          "label": "Target Magma Crystal Content",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "min": 30.0,
          "max": 60.0,
          "defaultValue": 45.0,
          "desc": "Solid crystal content percentage in blended magma"
        },
        {
          "id": "targetMagmaBrix",
          "label": "Target Magma Brix",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0Brix",
          "editable": true,
          "required": true,
          "min": 85.0,
          "max": 93.0,
          "defaultValue": 89.0,
          "desc": "Dry substance concentration of magma footing"
        },
        {
          "id": "blendingLiquid",
          "label": "Blending Medium Type",
          "classification": "DROPDOWN",
          "type": "select",
          "options": [
            "Clarified Syrup",
            "A-Molasses",
            "B-Molasses",
            "Clarified Juice"
          ],
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "defaultValue": "Clarified Syrup",
          "desc": "Liquid phase used to mingle sugar crystals"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "magmaFlow",
          "label": "Prepared Magma Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Sugar_Feed_Flow / (targetCrystalContent / 100)",
          "desc": "Finished magma pumped to pan footing receivers"
        },
        {
          "id": "liquidDemand",
          "label": "Blending Liquid Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Magma_Flow - Sugar_Feed_Flow",
          "desc": "Quantity of blending syrup/molasses added"
        },
        {
          "id": "magmaPurity",
          "label": "Resulting Magma Purity",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "%",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "(Sugar_Sucrose + Liquid_Sucrose) / Magma_DS * 100",
          "desc": "Overall purity of prepared footing"
        }
      ]
    },
    {
      "id": "intermediate",
      "title": "Intermediate Traceability Values",
      "fields": []
    }
  ],
  "crossChecks": [
    {
      "id": "cc_mass",
      "name": "Total Mass Balance Closure",
      "rel": "Sugar_In + Liquid_In = Magma_Out",
      "tol": 0.0,
      "unit": "%"
    },
    {
      "id": "cc_ds",
      "name": "Dry Substance Balance",
      "rel": "Sugar_In * DS_s + Liquid_In * DS_liq = Magma_Out * DS_magma",
      "tol": 0.0,
      "unit": "%"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: Magma Mixer Property Window Specification
Stencil ID: STENCIL-MAGMA-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
