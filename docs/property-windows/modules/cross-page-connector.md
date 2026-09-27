# Cross-Page and On-Page Connector Property Window Specification
## Component Code: `PW-CONN-CROSS-01`
### SUGARS Station Type: `CONN-PAGE` | Object Tag Prefix: `CPC` / `OPC`

> **Governing Agent**: Agent 10 — Sugar Property Window Architect  
> **Governing Stencil**: [`STENCIL-CONN-CROSS-01`](file:///c:/Users/punit/OneDrive/Documents/Purity_Sugar/docs/stencil/modules/cross-page-connector.md)  
> **Domain Authority**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Program_Operation/Cross-Page_and_On-Page_Connectors.md`)  
> **Status**: `ENGINEERING-VALIDATED`

---

## 1. Visual Hierarchy & Window Layout

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [CPC] CROSS-PAGE CONNECTOR PROPERTIES                           [—][X] │
├────────────────────────────────────────────────────────────────────────┤
│ Connector Tag [CPC-01___________] Station No [ 3310-9 ] Type [Cross-Page]
├────────────────────────────────────────────────────────────────────────┤
│ [Routing & Pairing]  [Internal Flow Data]  [Diagnostics]               │
├────────────────────────────────────────────────────────────────────────┤
│ ┌─ CONNECTOR TOPOLOGY & ROUTING ─────────────────────────────────────┐ │
│ │ Connector Type:      ( ) On-Page (Same Sheet)                      │ │
│ │                      (o) Cross-Page (Inter-Sheet Link)             │ │
│ │ Role in Stream:      (o) Source (Out of Page)  ( ) Dest (Into Page)│ │
│ │                                                                    │ │
│ │ Target Destination:                                                │ │
│ │ Target Page:         [ Page-2: Pan House              ▼ ]          │ │
│ │ Target Station:      [ Station 3010 (White Pan A)     ▼ ]          │ │
│ │ Target Port:         [ Port 1: Vapor In               ▼ ]          │ │
│ │                                                                    │ │
│ │ Displayed Text:      [ Page-2: 3010-1                             ]│ │
│ │                                                                    │ │
│ │ [ ↗ Jump to Connected Page & Station ]                             │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                        │
│ ┌─ INTERNAL FLOW PROPERTIES (IDENTICAL AT BOTH ENDS) ────────────────┐ │
│ │ Mass Flow Rate:      [ 25.000 ] TPH   Temperature:   [ 72.50 ] °C   │ │
│ │ Pressure:            [  82.50 ] kPa   Enthalpy:      [ 2,631 ] kJ/kg│ │
│ │ Dry Substance:       [  68.20 ] °Bx   Purity:        [ 92.50 ] %    │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│ [✓ Connection Status: PAIRED & ACTIVE] [✓ Stream Continuous]          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Field Classification & Behavior Matrix

| Field ID | Label | Type | Units | Editable | Rule / Behavior |
|---|---|---|---|---|---|
| `tag` | Connector Tag | String | — | YES | Identifier tag for connector |
| `connectorType` | Connector Type | Enum | — | YES | `ON_PAGE` vs `CROSS_PAGE` |
| `role` | Role | Enum | — | YES | `SOURCE` (Exit stream) vs `DESTINATION` (Entry stream) |
| `targetPageId` | Target Page | Enum / Dropdown | — | YES | List of all flowsheet pages in project |
| `targetStationId` | Target Station | Enum / Dropdown | — | YES | Stations on selected page |
| `targetPortId` | Target Port | Enum / Dropdown | — | YES | Available compatible ports on target station |
| `displayLabel` | Displayed Text | String | — | Auto / YES | Auto-formatted as `[PageName : StationNo-PortNo]` or custom |
| `jumpAction` | Jump to Mate | Button | — | Action | Switches active flowsheet page to target page and highlights target station |

---

## 3. Pairing & Linking Workflow

1. **Auto-Pairing**: When a user drops a Cross-Page or On-Page connector and links it to a port, creating a mate connector and setting its target automatically synchronizes both shapes.
2. **Stream Property Propagation**: All properties (Brix, Purity, Mass Flow, Temperature, Pressure, Component fractions) flow through the connector pair without resistance or dissipation.
