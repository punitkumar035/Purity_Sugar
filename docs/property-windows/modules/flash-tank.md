# Flash Tank Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-FLASH-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/flash-tank.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `10` | **Object Tag Prefix**: `FLT`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for condensate and hot liquor flash tanks recovering secondary vapour by adiabatic expansion.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [FLT] FLASH TANK PROPERTY WINDOW SPECIFICA   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Equipment Tag            [_______] —        │
│    Flash Vessel Pressure    [_______] kPa abs  │
│    Vent Condenser Enabled   [_______] —        │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Flashed Vapour Flow      [_______] TPH      🔒│
│    Discharged Liquid Flow   [_______] TPH      🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
│    Flash Saturation Temperature [_______] °C       ⓘ │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Total Mass Balance Closur [PASS / tol < 0.01%] │
│    ✓ Enthalpy Conservation     [PASS / tol < 0.05%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `equipmentTag` | **Equipment Tag** | `USER_INPUT` | `string` | `—` | YES | YES | Plant tag (e.g. FLASH_01, COND_FLT) |
| `stationTypeCode` | **Station Type Code** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | SUGARS station type code 10 |
| `operatingPressure` | **Flash Vessel Pressure** | `USER_INPUT` | `number` | `kPa abs` | YES | YES | Operating flash tank head pressure |
| `ventCondenser` | **Vent Condenser Enabled** | `BOOLEAN` | `boolean` | `—` | YES | NO | Subcooler on vent vapor |
| `flashedVapourFlow` | **Flashed Vapour Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Low-pressure vapour recovered for heating |
| `degassedLiquidFlow` | **Discharged Liquid Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Saturated liquid leaving bottom seal |
| `saturationTemp` | **Flash Saturation Temperature** | `INTERMEDIATE` | `number` | `°C` | NO (Locked) | NO | Boiling temperature at operating pressure |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_mass` | **Total Mass Balance Closure** | `Liquid_In = Flashed_Vapour_Out + Liquid_Out` | `±0.01` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_enthalpy` | **Enthalpy Conservation** | `F_in * h_in = F_vap * h_g + F_liq * h_f` | `±0.05` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "flashTank",
  "title": "Flash Tank Property Window Specification",
  "stencilId": "STENCIL-FLASH-01",
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
          "desc": "Plant tag (e.g. FLASH_01, COND_FLT)"
        },
        {
          "id": "stationTypeCode",
          "label": "Station Type Code",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "defaultValue": "10",
          "desc": "SUGARS station type code 10"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "operatingPressure",
          "label": "Flash Vessel Pressure",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "kPa abs",
          "editable": true,
          "required": true,
          "min": 10.0,
          "max": 250.0,
          "defaultValue": 101.3,
          "desc": "Operating flash tank head pressure"
        },
        {
          "id": "ventCondenser",
          "label": "Vent Condenser Enabled",
          "classification": "BOOLEAN",
          "type": "boolean",
          "unit": "\u2014",
          "editable": true,
          "required": false,
          "defaultValue": false,
          "desc": "Subcooler on vent vapor"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "flashedVapourFlow",
          "label": "Flashed Vapour Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "F_in * (h_in - h_f) / h_fg",
          "desc": "Low-pressure vapour recovered for heating"
        },
        {
          "id": "degassedLiquidFlow",
          "label": "Discharged Liquid Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "F_in - Flashed_Vapour_Flow",
          "desc": "Saturated liquid leaving bottom seal"
        }
      ]
    },
    {
      "id": "intermediate",
      "title": "Intermediate Traceability Values",
      "fields": [
        {
          "id": "saturationTemp",
          "label": "Flash Saturation Temperature",
          "classification": "INTERMEDIATE",
          "type": "number",
          "unit": "\u00b0C",
          "editable": false,
          "required": false,
          "precision": 1,
          "formula": "T_sat(operatingPressure)",
          "desc": "Boiling temperature at operating pressure"
        }
      ]
    }
  ],
  "crossChecks": [
    {
      "id": "cc_mass",
      "name": "Total Mass Balance Closure",
      "rel": "Liquid_In = Flashed_Vapour_Out + Liquid_Out",
      "tol": 0.01,
      "unit": "%"
    },
    {
      "id": "cc_enthalpy",
      "name": "Enthalpy Conservation",
      "rel": "F_in * h_in = F_vap * h_g + F_liq * h_f",
      "tol": 0.05,
      "unit": "%"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: Flash Tank Property Window Specification
Stencil ID: STENCIL-FLASH-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
