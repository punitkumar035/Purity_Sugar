# Stream & Connector Property Window Specification

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-STRM-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/stream-connection.md)  
> **Domain Source**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)  
> **SUGARS Station Code**: `STREAM` | **Object Tag Prefix**: `STRM`  
> **Status**: `ENGINEERING-VALIDATED`  

---

## 1. Purpose & Engineering Scope
Property window for all flowsheet mass and energy connections, displaying the 15-component stream composition, flow rates, temperature, pressure, enthalpy, and phase.

---

## 2. Standard Property Window Layout & Hierarchy

```text
┌────────────────────────────────────────────────────────┐
│ [STRM] STREAM & CONNECTOR PROPERTY WINDOW S   [X] │
├────────────────────────────────────────────────────────┤
│ 1. GENERAL & IDENTIFICATION                            │
│    Station Number [____]   Equipment Tag [___________] │
│    Station Type Code [ 9 ] SUGARS Type Code            │
├────────────────────────────────────────────────────────┤
│ 2. PROCESS INPUTS (USER / OPTIONAL)                    │
│    Total Mass Flow          [_______] TPH      │
│    Dry Substance / Brix     [_______] °Brix    │
│    Purity (Apparent / True) [_______] %        │
│    Temperature              [_______] °C       │
│    Pressure                 [_______] kPa abs  │
├────────────────────────────────────────────────────────┤
│ 3. CALCULATED VALUES & RESULTS (READ-ONLY)             │
│    Specific Enthalpy        [_______] kJ/kg    🔒│
│    Stream Density           [_______] kg/m³    🔒│
│    Dry Substance Flow       [_______] TPH      🔒│
│    Free Water Flow          [_______] TPH      🔒│
├────────────────────────────────────────────────────────┤
│ 4. INTERMEDIATE TRACEABILITY & REFERENCE VALUES        │
├────────────────────────────────────────────────────────┤
│ 5. INDEPENDENT PHYSICAL BALANCE CROSS-CHECKS           │
│    ✓ Solids & Water Sum Closur [PASS / tol < 0.001%] │
└────────────────────────────────────────────────────────┘
```

---

## 3. Field Classification & Behavior Matrix

| Field ID | Label | Classification | Type | Unit | Editable | Required | Engineering Definition |
|---|---|---|---|---|---|---|---|
| `streamId` | **Stream Identifier** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | Unique stream UUID and sequence tag |
| `sourcePort` | **Source Station & Port** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | Originating station tag and discharge port |
| `targetPort` | **Target Station & Port** | `READ_ONLY` | `string` | `—` | NO (Locked) | YES | Destination station tag and inlet port |
| `massFlow` | **Total Mass Flow** | `USER_INPUT` | `number` | `TPH` | YES | YES | Gross mass flow rate |
| `brix` | **Dry Substance / Brix** | `USER_INPUT` | `number` | `°Brix` | YES | YES | Refractometric or gravimetric dry substance |
| `purity` | **Purity (Apparent / True)** | `USER_INPUT` | `number` | `%` | YES | YES | Sucrose % on Dry Substance |
| `temperature` | **Temperature** | `USER_INPUT` | `number` | `°C` | YES | YES | Stream thermodynamic temperature |
| `pressure` | **Pressure** | `USER_INPUT` | `number` | `kPa abs` | YES | YES | Static absolute pressure |
| `enthalpy` | **Specific Enthalpy** | `CALCULATED` | `number` | `kJ/kg` | NO (Locked) | NO | Thermodynamic heat content relative to 0°C water |
| `density` | **Stream Density** | `CALCULATED` | `number` | `kg/m³` | NO (Locked) | NO | Bulk fluid or slurry density |
| `drySubstanceFlow` | **Dry Substance Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Solids flow: massFlow * brix / 100 |
| `waterFlow` | **Free Water Flow** | `CALCULATED` | `number` | `TPH` | NO (Locked) | NO | Water flow: massFlow - drySubstanceFlow |

---

## 4. Independent Physical Balance Cross-Checks

| Check ID | Cross-Check Name | Governing Relationship | Tolerance | Unit | Status Condition |
|---|---|---|---|---|---|
| `cc_ds_mass` | **Solids & Water Sum Closure** | `massFlow = drySubstanceFlow + waterFlow` | `±0.001` | `%` | `PASS` if closure error < tolerance; else `WARNING` |

---

## 5. Formal Machine-Readable JSON Schema

```json
{
  "objectType": "stream",
  "title": "Stream & Connector Property Window Specification",
  "stencilId": "STENCIL-STRM-01",
  "engineeringBasis": "Sugar's Help Book",
  "sections": [
    {
      "id": "general",
      "title": "General & Identification",
      "fields": [
        {
          "id": "streamId",
          "label": "Stream Identifier",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "desc": "Unique stream UUID and sequence tag"
        },
        {
          "id": "sourcePort",
          "label": "Source Station & Port",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "desc": "Originating station tag and discharge port"
        },
        {
          "id": "targetPort",
          "label": "Target Station & Port",
          "classification": "READ_ONLY",
          "type": "string",
          "unit": "\u2014",
          "editable": false,
          "required": true,
          "desc": "Destination station tag and inlet port"
        }
      ]
    },
    {
      "id": "inputs",
      "title": "Process & Operating Inputs",
      "fields": [
        {
          "id": "massFlow",
          "label": "Total Mass Flow",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "TPH",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Gross mass flow rate"
        },
        {
          "id": "brix",
          "label": "Dry Substance / Brix",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0Brix",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Refractometric or gravimetric dry substance"
        },
        {
          "id": "purity",
          "label": "Purity (Apparent / True)",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "%",
          "editable": true,
          "required": true,
          "precision": 2,
          "desc": "Sucrose % on Dry Substance"
        },
        {
          "id": "temperature",
          "label": "Temperature",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "\u00b0C",
          "editable": true,
          "required": true,
          "precision": 1,
          "desc": "Stream thermodynamic temperature"
        },
        {
          "id": "pressure",
          "label": "Pressure",
          "classification": "USER_INPUT",
          "type": "number",
          "unit": "kPa abs",
          "editable": true,
          "required": true,
          "precision": 1,
          "desc": "Static absolute pressure"
        }
      ]
    },
    {
      "id": "calculated",
      "title": "Calculated Results",
      "fields": [
        {
          "id": "enthalpy",
          "label": "Specific Enthalpy",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "kJ/kg",
          "editable": false,
          "required": false,
          "precision": 1,
          "desc": "Thermodynamic heat content relative to 0\u00b0C water"
        },
        {
          "id": "density",
          "label": "Stream Density",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "kg/m\u00b3",
          "editable": false,
          "required": false,
          "precision": 1,
          "desc": "Bulk fluid or slurry density"
        },
        {
          "id": "drySubstanceFlow",
          "label": "Dry Substance Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "desc": "Solids flow: massFlow * brix / 100"
        },
        {
          "id": "waterFlow",
          "label": "Free Water Flow",
          "classification": "CALCULATED",
          "type": "number",
          "unit": "TPH",
          "editable": false,
          "required": false,
          "precision": 2,
          "desc": "Water flow: massFlow - drySubstanceFlow"
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
      "id": "cc_ds_mass",
      "name": "Solids & Water Sum Closure",
      "rel": "massFlow = drySubstanceFlow + waterFlow",
      "tol": 0.001,
      "unit": "%"
    }
  ]
}
```

---

## 6. Developer & UI Implementation Directive
```text
STENCIL HANDOFF:
Module: Stream & Connector Property Window Specification
Stencil ID: STENCIL-STRM-01
Status: ENGINEERING-VALIDATED
Developer Action: Implement property pane and reactivity exactly according to this specification.
```
