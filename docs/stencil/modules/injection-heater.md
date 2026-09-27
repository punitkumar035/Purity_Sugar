# STENCIL SPECIFICATION: Direct Injection Heater Station
## Module Identifier: `STENCIL-INJ-01`
### Station Type Code: `13` | SUGARS Classification: Injection Heater

> **Authoritative Domain Reference**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/references/Injection_Heater/`)  
> **Governing Agent**: Agent 9 — Sugar Stencil Architect  
> **Thermodynamic Basis**: `RULES_v5.md` (§A7, §A8), Direct Contact Steam Condensation, Dilution Enthalpy Balance  
> **Status**: `APPROVED FOR IMPLEMENTATION`

---

## 1. Process & Functional Description

The Injection Heater station injects steam or process vapour directly into a flowing process stream (such as raw juice, limed juice, or massecuite) without any intermediate metal heating surface.

Governing Principles:
1. **Direct Condensation & Mixing**: All of the heating steam or vapour condenses directly into the process fluid and mixes with it.
2. **Instantaneous Juice Dilution**: The condensed water increases the liquid flow and dilutes the dry substance (%Brix decreases).
3. **Heating Flow is Always Required [R]**: The quantity of steam/vapour injected is automatically calculated by the solver to satisfy the entered thermal specification.
4. **Mutually Exclusive Operating Specifications (Magenta Borders)**:
   - Exactly one of **Temperature Out** ($°C$) OR **Temperature Rise** ($K$) can be entered.

---

## 2. Port Architecture & Topological Connectivity

| Port Index | Semantic Name | Direction | Stream Class | Category | Accept Constraints | Required Flow Rule |
|---|---|---|---|---|---|---|
| **Port 0 In** | **Process Stream In** | IN | `material` | Juice / Liquid | Liquid stream to be heated | Process feed |
| **Port 1 In** | **Injection Steam / Vapour** | IN | `thermal` | Steam / Vapour | Heating steam or process vapour | **Always Required [R]** |
| **Port 0 Out**| **Heated & Diluted Stream Out**| OUT | `material` | Heated Liquid | Outlet liquid with increased mass and lowered Brix | Discharged downstream |

---

## 3. Engineering Parameter Schema

| Parameter Name | Data Type | Units | Default | Physical Range | Validation & Engineering Rules |
|---|---|---|---|---|---|
| `stationNumber` | `integer` | — | Auto | 1 – 9999 | Unique plant station identifier |
| `equipmentTag` | `string` | — | `INJ-01` | Up to 11 chars | Equipment asset tag |
| `controlMode` | `enum` | — | `TEMP_OUT` | `TEMP_OUT` / `TEMP_RISE` | Mutually exclusive control selector |
| `temperatureOut`| `float` | `°C` | 85.0 | 20.0 – 130.0 | Desired process outlet temperature (active when `TEMP_OUT`) |
| `temperatureRiseK`| `float` | `K` | 15.0 | 0.5 – 60.0 | Desired temperature elevation $\Delta T$ (active when `TEMP_RISE`) |
| `heatLossPct` | `float` | `%` | 0.5 | 0.0 – 5.0 | Percentage loss of heat from total heat transferred |

---

## 4. Governing Thermodynamic Equations

### 4.1 Process Fluid Heat Absorption
$$T_{out} = \begin{cases} \text{temperatureOut} & \text{if mode is } \text{TEMP\_OUT} \\ T_{in} + \text{temperatureRiseK} & \text{if mode is } \text{TEMP\_RISE} \end{cases}$$
$$Q_{absorbed} = \dot{M}_{process,in} \cdot C_{p,juice} \cdot (T_{out} - T_{in})$$
$$Q_{gross} = \frac{Q_{absorbed}}{1.0 - \text{heatLossPct} / 100.0}$$

### 4.2 Injection Steam Mass Rate (Required Flow)
$$\dot{M}_{steam,req} = \frac{Q_{gross}}{h_{steam,in} - h_{water}(T_{out}, P_{out})}$$

### 4.3 Juice Dilution & Dry Substance
$$\dot{M}_{out} = \dot{M}_{process,in} + \dot{M}_{steam,req}$$
$$DS_{out} = \frac{\dot{M}_{process,in} \cdot DS_{in}}{\dot{M}_{out}}$$

---

## 5. Independent Physical Balance Cross-Checks

1. **Total Mass Balance Closure**:
   $$\epsilon_{mass} = \frac{|(\dot{M}_{process,in} + \dot{M}_{steam,req}) - \dot{M}_{out}|}{\dot{M}_{process,in} + \dot{M}_{steam,req}} \times 100\% \equiv 0.000\%$$
2. **Dry Substance Conservation Closure**:
   $$\epsilon_{DS} = \frac{|\dot{M}_{process,in} \cdot DS_{in} - \dot{M}_{out} \cdot DS_{out}|}{\dot{M}_{process,in} \cdot DS_{in}} \times 100\% \equiv 0.000\%$$
3. **Enthalpy Balance Closure**:
   $$\epsilon_{heat} = \frac{|\dot{M}_{process,in} h_{in} + \dot{M}_{steam} h_{steam} - \dot{M}_{out} h_{out} - Q_{loss}|}{\dot{M}_{process,in} h_{in} + \dot{M}_{steam} h_{steam}} \times 100\% \le 0.05\%$$
