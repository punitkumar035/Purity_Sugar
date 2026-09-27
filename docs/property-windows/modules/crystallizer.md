# Crystallizer Station Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CRYS-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/crystallizer.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `12` | **Object Tag Prefix**: `CRYS`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for continuous and batch cooling crystallizers desaturating massecuite by controlled cooling to maximize crystal recovery.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [CRYS] CRYSTALLIZER STATION PROPERTY WINDOW   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Station Number           [_______] —        │
│    Equipment Tag            [_______] —        │
│    Target Cooled Temperature [_______] °C       │
│    Target Mother Liquor Supersaturation (Ss) [_______] —        │
│    Nominal Residence Time   [_______] h        │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Additional Crystal Grown [_______] TPH      🔒│
│    Outlet Crystal Content   [_______] %        🔒│
│    Exhausted Mother Liquor Purity [_______] %        🔒│
│    Cooling Heat Duty        [_______] kW       🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Massecuite Mass Conservat [PASS / tol < 0.0%] │
│    ✓ Dry Substance Conservatio [PASS / tol < 0.0%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `stationNumber` | **Station Number** | `USER_INPUT` | `number` | `—` | YES | YES | Unique plant station number |
| `equipmentTag` | **Equipment Tag** | `USER_INPUT` | `string` | `—` | YES | YES | Plant tag (e.g. C_CRYS_01) |
| `stationTypeCode` | **Station Type Code** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | SUGARS station type code 12 |
| `outletTemp` | **Target Cooled Temperature** | `USER_INPUT` | `number` | `°C` | YES | YES | Cooled massecuite discharge temperature |
| `targetSupersaturation` | **Target Mother Liquor Supersaturation (Ss)** | `USER_INPUT` | `number` | `—` | YES | YES | Controlled saturation level to avoid false grain formation |
| `residenceTime` | **Nominal Residence Time** | `OPTIONAL_INPUT` | `number` | `h` | YES | NO | Massecuite retention time in cooling bank |
| `additionalCrystal` | **Additional Crystal Grown** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Mass of sucrose transferred from mother liquor to crystal faces |
| `outletCrystalContent` | **Outlet Crystal Content** | `CALCULATED` | `number` | `%` | NO (Locked) | NO | Final crystal percentage on discharged massecuite |
| `exhaustedPurity` | **Exhausted Mother Liquor Purity** | `CALCULATED` | `number` | `%` | NO (Locked) | NO | Purity of liquid phase feeding centrifugals |
| `coolingDuty` | **Cooling Heat Duty** | `CALCULATED` | `number` | `kW` | NO (Locked) | NO | Thermal energy removed by cooling coils/elements |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_mass` | **Massecuite Mass Conservation** | `Massecuite_In = Massecuite_Out` | `±0.0` | `%` | `PASS` if closure error < tolerance; else `WARNING` |
| `cc_ds` | **Dry Substance Conservation** | `Massecuite_In * DS_in = Massecuite_Out * DS_out` | `±0.0` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "crystallizer",
  "title": "Crystallizer Station Property Window Specification",
  "stencilId": "STENCIL-CRYS-01",
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
          "desc": "Plant tag (e.g. C_CRYS_01)"
        },
        {
          "id": "stationTypeCode",
          "label": "Station Type Code",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "defaultValue": "12",
          "desc": "SUGARS station type code 12"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "outletTemp",
          "label": "Target Cooled Temperature",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0C",
          "editable": true,
          "required": true,
          "min": 35.0,
          "max": 65.0,
          "defaultValue": 42.0,
          "desc": "Cooled massecuite discharge temperature"
        },
        {
          "id": "targetSupersaturation",
          "label": "Target Mother Liquor Supersaturation (Ss)",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u2014",
          "editable": true,
          "required": true,
          "min": 1.05,
          "max": 1.25,
          "defaultValue": 1.12,
          "desc": "Controlled saturation level to avoid false grain formation"
        },
        {
          "id": "residenceTime",
          "label": "Nominal Residence Time",
          "classification": "OPTIONAL_INPUT",
          "type": "number",
          "unit": "h",
          "editable": true,
          "required": false,
          "min": 12.0,
          "max": 48.0,
          "defaultValue": 24.0,
          "desc": "Massecuite retention time in cooling bank"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "additionalCrystal",
          "label": "Additional Crystal Grown",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Crystallizer_Deposition_Rate(M_in, T_in, T_out, Ss)",
          "desc": "Mass of sucrose transferred from mother liquor to crystal faces"
        },
        {
          "id": "outletCrystalContent",
          "label": "Outlet Crystal Content",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "%",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "100 * (Crystals_in + Crystals_grown) / M_out",
          "desc": "Final crystal percentage on discharged massecuite"
        },
        {
          "id": "exhaustedPurity",
          "label": "Exhausted Mother Liquor Purity",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "%",
          "editable": false,
          "required": false,
          "precision": 2,
          "formula": "Resulting mother liquor purity after crystallization",
          "desc": "Purity of liquid phase feeding centrifugals"
        },
        {
          "id": "coolingDuty",
          "label": "Cooling Heat Duty",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "kW",
          "editable": false,
          "required": false,
          "precision": 1,
          "formula": "M_flow * Cp * (T_in - T_out) / 3.6 + Q_crystallization",
          "desc": "Thermal energy removed by cooling coils/elements"
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
      "name": "Massecuite Mass Conservation",
      "rel": "Massecuite_In = Massecuite_Out",
      "tol": 0.0,
      "unit": "%"
    },
    {
      "id": "cc_ds",
      "name": "Dry Substance Conservation",
      "rel": "Massecuite_In * DS_in = Massecuite_Out * DS_out",
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
Module: Crystallizer Station Property Window Specification
Stencil ID: STENCIL-CRYS-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
