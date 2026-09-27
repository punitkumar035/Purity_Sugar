# External Boundary & Feed Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CAP-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/boundary-source.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `SOURCE` | **Object Tag Prefix**: `SRC`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for factory battery-limit inlets including cane crushing, mixed juice feed, utility steam headers, and raw water sources.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [SRC] EXTERNAL BOUNDARY & FEED PROPERTY WI   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Boundary Label           [_______] —        │
│    Boundary Mass Flow Rate  [_______] TPH      │
│    Feed Dry Substance / Brix [_______] °Brix    │
│    Feed Purity              [_______] %        │
│    Feed Temperature         [_______] °C       │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Solids Throughput        [_______] TPH      🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Non-Negative Feed Check   [PASS / tol < 0.0—] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `boundaryLabel` | **Boundary Label** | `USER_INPUT` | `string` | `—` | YES | YES | Plant feed tag (e.g. CANE_MILL_FEED, BOILER_STEAM) |
| `flowRate` | **Boundary Mass Flow Rate** | `USER_INPUT` | `number` | `TPH` | YES | YES | Gross throughput introduced to flowsheet |
| `feedBrix` | **Feed Dry Substance / Brix** | `USER_INPUT` | `number` | `°Brix` | YES | YES | Solids content of incoming raw stream |
| `feedPurity` | **Feed Purity** | `USER_INPUT` | `number` | `%` | YES | YES | Sucrose percentage in solids |
| `feedTemp` | **Feed Temperature** | `USER_INPUT` | `number` | `°C` | YES | YES | Feed temperature at battery limit |
| `dsFlow` | **Solids Throughput** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Solids mass rate introduced |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_positive` | **Non-Negative Feed Check** | `flowRate > 0 and feedBrix >= 0` | `±0.0` | `—` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "source",
  "title": "External Boundary & Feed Property Window Specification",
  "stencilId": "STENCIL-CAP-01",
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
          "id": "boundaryLabel",
          "label": "Boundary Label",
          "classification": "USER_INPUT",
          "type": "string",
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "desc": "Plant feed tag (e.g. CANE_MILL_FEED, BOILER_STEAM)"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "flowRate",
          "label": "Boundary Mass Flow Rate",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "TPH",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Gross throughput introduced to flowsheet"
        },
        {
          "id": "feedBrix",
          "label": "Feed Dry Substance / Brix",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0Brix",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Solids content of incoming raw stream"
        },
        {
          "id": "feedPurity",
          "label": "Feed Purity",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Sucrose percentage in solids"
        },
        {
          "id": "feedTemp",
          "label": "Feed Temperature",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0C",
          "editable": true,
          "required": true,
          "precision": 1,
          "desc": "Feed temperature at battery limit"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "dsFlow",
          "label": "Solids Throughput",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "desc": "Solids mass rate introduced"
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
      "id": "cc_positive",
      "name": "Non-Negative Feed Check",
      "rel": "flowRate > 0 and feedBrix >= 0",
      "tol": 0.0,
      "unit": "\u2014"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: External Boundary & Feed Property Window Specification
Stencil ID: STENCIL-CAP-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
