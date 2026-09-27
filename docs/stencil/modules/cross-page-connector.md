# STENCIL SPECIFICATION: Cross-Page and On-Page Connectors
## Module Identifier: `STENCIL-CONN-CROSS-01`
### Station Type Code: `CONN-PAGE` | SUGARS Classification: Inter-Page & Intra-Page Routing

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Program_Operation/Cross-Page_and_On-Page_Connectors.md`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: Zero-loss stream continuity, Multi-page topological bridge  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

In large sugar factory and refinery models (e.g. Beet or Cane Factory, Multi-Effect Evaporator, Pan House, Centrifugal Battery, Refinery), flowsheets become too extensive and visually cluttered if all streams are routed across a single canvas with physical wire lines. 

Sugar's Help Book provides two dedicated connector primitives:
1. **On-Page Connector**: Used for connections between stations on the **same page** where a direct streamline would cross multiple vessels or create visual confusion. Displays a horizontal arrow / hexagonal banner.
2. **Cross-Page Connector**: Used for connections between stations located on **different pages** of a multi-page flowsheet (e.g., Evaporator Effect 5 syrup on Page 2 routed to Pan House Feed Tank on Page 3). Displays an off-page pentagonal flag / banner shape.

### Key Behaviors:
- **Stream Continuity**: Both connectors in a pair represent the exact same thermodynamic stream line. Flow rate, temperature, pressure, brix, purity, and component ledger are identical.
- **Bi-Directional Labeling**: 
  - Source connector displays target address: `[TargetPage : TargetStation - Port]` (e.g., `Page-2: 3010-1`).
  - Destination connector displays source address: `[SourcePage : SourceStation - Port]` (e.g., `Page-1: 3310-9`).
- **Interactive Navigation (Jump-to-Mate)**: Clicking or double-clicking either connector offers a direct jump navigation: switches active page, pans the viewport, and focuses the target station/connector.
- **Topological Integrity**: During multi-page network solving, the solver traverses connector pairs as virtual transparent stream segments.

---

## 2. Port Architecture & Topological Connectivity

### Type A: Source / Exit Connector (Sends stream out of page / section)
| Port Index | Direction | Stream Class | Semantic Name | Rules |
|---|---|---|---|---|
| **Port 0 In** | IN | `material` | Stream Inlet from Upstream Station | Receives stream from originating station port |

### Type B: Destination / Entry Connector (Brings stream into page / section)
| Port Index | Direction | Stream Class | Semantic Name | Rules |
|---|---|---|---|---|
| **Port 0 Out** | OUT | `material` | Stream Outlet to Downstream Station | Feeds stream into destination station port |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Range / Format | Description & Validation |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique connector station ID |
| `connectorType` | `enum` | — | `CROSS_PAGE` | `ON_PAGE`, `CROSS_PAGE` | Shape: Hexagon (On-Page) vs Pentagon (Cross-Page) |
| `role` | `enum` | — | `SOURCE` | `SOURCE`, `DESTINATION` | Exit stream vs Entry stream |
| `mateId` | `string` | — | `""` | Valid node ID | ID of paired connector node |
| `targetPageId` | `string` | — | `""` | Valid page ID | Target page identifier |
| `targetStationNo`| `integer` | — | 0 | 1 – 9999 | Connected equipment station number |
| `targetPortNo` | `integer` | — | 0 | 0 – 31 | Connected equipment port number |
| `label` | `string` | — | `Unlinked` | 1 – 32 chars | Displayed text badge inside shape |

---

## 4. Visual Stencil Rendering Standards

1. **On-Page Connector (`ON_PAGE`)**:
   - Shape: Hexagonal elongated arrow: `<polygon points="0,0 70,0 85,15 70,30 0,30 10,15" ... />`
   - Border: Cyan `#00d2ff`, Fill: Dark Navy `#0b1a2d`
   - Label: `Station-Port` (e.g., `3010-1`)
2. **Cross-Page Connector (`CROSS_PAGE`)**:
   - Shape: Off-page pentagonal banner: `<polygon points="0,0 65,0 85,17 65,34 0,34" ... />`
   - Border: Gold / Amber `#f59e0b`, Fill: `#1a1608`
   - Label: `Page: Station-Port` (e.g., `Page-2: 3010-1`)
3. **Interactive Jump Indicator**:
   - External link icon `↗` on hover. Clicking switches active page and pans to mate.
