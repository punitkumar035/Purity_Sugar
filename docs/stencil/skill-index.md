# Sugar's Help Book: Comprehensive Domain Index

> **Authoritative Reference Base**: `Sugar's Help Book` (`.agents/skills/sugars-helpbook/`)
> **Agent 9 Deliverable**: Full knowledgebase extraction and mapping for software stencils.

This document provides a systematic index of all 110 engineering reference sections, equipment unit operations, physical chemistry theory, and worked factory simulation models in the Sugar's Help Book reference library.

---

## 1. Master Chapter & Section Directory

| Section / Directory | Topic Category | Primary Files | Equipment / Unit Models Covered |
|---|---|---|---|
| **Blender** | Liquid / Material Mixing | 3 files (`Blender_Examples.md, Blender_Features.md, Blender_Properties.md`) | Blender |
| **Centrifugal** | Solid-Liquid Separation / Purging | 7 files (`2-Output_Centrifugal_Evaluation.md, 2-Output_Centrifugal_Properties.md, 3-Output_Centrifugal_Evaluation.md...`) | Centrifugal |
| **Compressor** | Vapour Compression & Gas Handling | 3 files (`Compressor_Examples.md, Compressor_Features.md, Compressor_Properties.md`) | Compressor |
| **Contact Condenser** | Direct-Contact Barometric Condensing | 3 files (`Contact_Condenser_Examples.md, Contact_Condenser_Features.md, Contact_Condenser_Properties.md`) | Contact Condenser |
| **Cooler** | Air & Water Process Fluid Cooling | 3 files (`Cooler_Examples.md, Cooler_Features.md, Cooler_Properties.md`) | Cooler |
| **Crystallizer** | Batch & Continuous Cooling Crystallization | 3 files (`Crystallizer_Examples.md, Crystallizer_Features.md, Crystallizer_Properties.md`) | Crystallizer |
| **Distributor** | Stream Splitting & Vapour Bleeding | 3 files (`Distributor_Examples.md, Distributor_Features.md, Distributor_Properties.md`) | Distributor |
| **Dryer** | Sugar & Pulp Solids Drying | 3 files (`Dryer_Examples.md, Dryer_Features.md, Dryer_Properties.md`) | Dryer |
| **Error Messages** | Diagnostic & Convergence Validation | 1 files (`Error_Messages.md`) | Error Messages |
| **Evaporator** | Multi-Effect Juice Evaporation & Vapour Bleeding | 3 files (`Evaporator_Examples.md, Evaporator_Features.md, Evaporator_Properties.md`) | Evaporator |
| **Examples** | Full Factory & Refinery Flowsheet Models | 13 files (`4-Effect_Multiple.md, 6-Effect_Multiple.md, Beet_Factory.md...`) | Examples |
| **Flash Tank** | Sensible Heat & Condensate Flash Recovery | 3 files (`Flash_Tank_Examples.md, Flash_Tank_Features.md, Flash_Tank_Properties.md`) | Flash Tank |
| **Heat Exchanger** | Indirect Heating (Shell & Tube, Plate) | 3 files (`Heat_Exchanger_Examples.md, Heat_Exchanger_Features.md, Heat_Exchanger_Properties.md`) | Heat Exchanger |
| **Injection Heater** | Direct Steam Massecuite / Juice Heating | 3 files (`Injection_Heater_Examples.md, Injection_Heater_Features.md, Injection_Heater_Properties.md`) | Injection Heater |
| **Introduction** | Simulation Architecture & System Conventions | 4 files (`Acknowledgement.md, Introduction.md, License_Agreement.md...`) | Introduction |
| **Melter** | Crystal Dissolution & Melt Liquor Preparation | 3 files (`Melter_Examples.md, Melter_Features.md, Melter_Properties.md`) | Melter |
| **Overview** | Process Flowsheet Topology & File Architecture | 3 files (`File_Structure.md, Flow_Diagram.md, Program_Overview.md`) | Overview |
| **Pan** | Vacuum Pan Boiling & Evaporative Crystallization | 3 files (`Pan_Examples.md, Pan_Features.md, Pan_Properties.md`) | Pan |
| **Pressure Reducer** | Steam Pressure Reduction & Desuperheating | 3 files (`Pressure_Reducer_Examples.md, Pressure_Reducer_Features.md, Pressure_Reducer_Properties.md`) | Pressure Reducer |
| **Program Operation** | Stream Mechanics, Connectivity & Boundaries | 8 files (`Cross-Page_and_On-Page_Connectors.md, Data_Import_Export.md, Exporting_Data_to_Excel.md...`) | Program Operation |
| **Pump** | Hydraulic Fluid Power & Head Addition | 3 files (`Pump_Examples.md, Pump_Features.md, Pump_Properties.md`) | Pump |
| **Reactor** | Chemical Reaction & Liming Carbonatation | 3 files (`Reactor_Examples.md, Reactor_Features.md, Reactor_Properties.md`) | Reactor |
| **Receiver** | Surge Vessel & Intermediate Buffer Storage | 3 files (`Receiver_Examples.md, Receiver_Features.md, Receiver_Properties.md`) | Receiver |
| **Separator Filter** | Cake Filtration & Solid-Liquid Clarification | 3 files (`Separator_Filter_Examples.md, Separator_Filter_Features.md, Separator_Filter_Properties.md`) | Separator Filter |
| **Station Modules** | Custom Stencils & Shape Composition | 3 files (`About_Station_Modules.md, Designing_Your_Own_Shapes.md, Grouping_Shapes.md`) | Station Modules |
| **Sucrose Supersaturation** | Physical Chemistry of Supersaturation | 1 files (`Supersaturation.md`) | Sucrose Supersaturation |
| **Surface Condenser** | Indirect Surface Condensing & Condensate Recovery | 3 files (`Surface_Condenser_Examples.md, Surface_Condenser_Features.md, Surface_Condenser_Properties.md`) | Surface Condenser |
| **Tank** | Atmospheric & Pressurized Storage Vessels | 3 files (`Tank_Examples.md, Tank_Features.md, Tank_Properties.md`) | Tank |
| **Theory** | Physical Chemistry, Solubility, BPE, Heat Content | 1 files (`Theory.md`) | Theory |
| **Thermocompressor** | Ejector / Thermo-Vapour Recompression (TVR) | 3 files (`Thermocompressor_Examples.md, Thermocompressor_Features.md, Thermocompressor_Properties.md`) | Thermocompressor |
| **Turbine** | Mechanical Drive Steam Turbines | 3 files (`Turbine_Examples.md, Turbine_Features.md, Turbine_Properties.md`) | Turbine |
| **Turbo Alternator** | Cogeneration & Electric Power Generation | 3 files (`Turbo_Alternator_Examples.md, Turbo_Alternator_Features.md, Turbo_Alternator_Properties.md`) | Turbo Alternator |

---

## 2. Exhaustive Section-by-Section Engineering Breakdown

### Blender
**Category**: Liquid / Material Mixing  
**Path**: `.agents/skills/sugars-helpbook/references/Blender/`  

#### `Blender_Examples.md` — Blender Examples
- **Scope & Behavior**: As shown on the Blender Properties window below, a blend flow is being
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Blender_Features.md` — Blender Features
- **Scope & Behavior**: Blender <span class="hcp2"> Blender stations are used to blend one flow
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Blender_Properties.md` — Blender Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

---

### Centrifugal
**Category**: Solid-Liquid Separation / Purging  
**Path**: `.agents/skills/sugars-helpbook/references/Centrifugal/`  

#### `2-Output_Centrifugal_Evaluation.md` — 2-Output Centrifugal Evaluation
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance

#### `2-Output_Centrifugal_Properties.md` — 2-Output Centrifugal Properties
- **Scope & Behavior**: Actual data from a centrifugal in the factory, or process, being modeled
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation

#### `3-Output_Centrifugal_Evaluation.md` — 3-Output Centrifugal Evaluation
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance

#### `3-Output_Centrifugal_Properties.md` — 3-Output Centrifugal Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency

#### `Centrifugal_Evaluations.md` — Centrifugal Evaluations
- **Scope & Behavior**: Centrifugal evaluations are used by Sugars to evaluate the separation of
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Centrifugal_Examples.md` — Centrifugal Examples
- **Scope & Behavior**: Wash flow into a centrifugal station can be water, syrup, or a
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Centrifugal_Features.md` — Centrifugal Features
- **Scope & Behavior**: Sugars can simulate the operation of 2-Output (both Continuous and
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Centrifugal mother liquor & wash purging efficiency

---

### Compressor
**Category**: Vapour Compression & Gas Handling  
**Path**: `.agents/skills/sugars-helpbook/references/Compressor/`  

#### `Compressor_Examples.md` — Compressor Examples
- **Scope & Behavior**: The figure below shows a mechanical vapor re-compressor (MVR)
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Compressor_Features.md` — Compressor Features
- **Scope & Behavior**: Compressor A compressor station is used to compress vapor by mechanical
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

#### `Compressor_Properties.md` — Compressor Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

---

### Contact Condenser
**Category**: Direct-Contact Barometric Condensing  
**Path**: `.agents/skills/sugars-helpbook/references/Contact_Condenser/`  

#### `Contact_Condenser_Examples.md` — Contact Condenser Examples
- **Scope & Behavior**: condenser is normally set to control the cold-water flow into a
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Contact_Condenser_Features.md` — Contact Condenser Features
- **Scope & Behavior**: Contact Condenser Contact condenser (direct-contact condenser) stations
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Contact_Condenser_Properties.md` — Contact Condenser Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Cooler
**Category**: Air & Water Process Fluid Cooling  
**Path**: `.agents/skills/sugars-helpbook/references/Cooler/`  

#### `Cooler_Examples.md` — Cooler Examples
- **Scope & Behavior**: Vapor Flow Heat Loss Use a cooler station to allow for heat loss in a
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Cooler_Features.md` — Cooler Features
- **Scope & Behavior**: Cooler stations are used to remove heat and/or condense water vapor in a
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Cooler_Properties.md` — Cooler Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Crystallizer
**Category**: Batch & Continuous Cooling Crystallization  
**Path**: `.agents/skills/sugars-helpbook/references/Crystallizer/`  

#### `Crystallizer_Examples.md` — Crystallizer Examples
- **Scope & Behavior**: Massecuite Crystallizer A crystallizer can be used to represent the
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Crystallizer_Features.md` — Crystallizer Features
- **Scope & Behavior**: Both horizontal and vertical crystallizers are used to increase the
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Van Hook supersaturation calculation

#### `Crystallizer_Properties.md` — Crystallizer Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

---

### Distributor
**Category**: Stream Splitting & Vapour Bleeding  
**Path**: `.agents/skills/sugars-helpbook/references/Distributor/`  

#### `Distributor_Examples.md` — Distributor Examples
- **Scope & Behavior**: Two methods are available for defining the quantity of flow in each
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation; Centrifugal mother liquor & wash purging efficiency

#### `Distributor_Features.md` — Distributor Features
- **Scope & Behavior**: Distributor A distributor station is used to split one input flow into
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Distributor_Properties.md` — Distributor Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Dryer
**Category**: Sugar & Pulp Solids Drying  
**Path**: `.agents/skills/sugars-helpbook/references/Dryer/`  

#### `Dryer_Examples.md` — Dryer Examples
- **Scope & Behavior**: station.</span><span class="hcp3"> </span><span class="hcp2"> Steam is
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Dryer_Features.md` — Dryer Features
- **Scope & Behavior**: Dryers are used to remove water from an insoluble solid material. The
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Dryer_Properties.md` — Dryer Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

---

### Error Messages
**Category**: Diagnostic & Convergence Validation  
**Path**: `.agents/skills/sugars-helpbook/references/Error_Messages/`  

#### `Error_Messages.md` — Error Messages
- **Scope & Behavior**: Error messages are given by Sugars if errors are detected during
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Evaporator
**Category**: Multi-Effect Juice Evaporation & Vapour Bleeding  
**Path**: `.agents/skills/sugars-helpbook/references/Evaporator/`  

#### `Evaporator_Examples.md` — Evaporator Examples
- **Scope & Behavior**: Specifying a Total Solids (%) for any one body in a multiple-effect will
- **Calculations & Models**: Kadlec, Bretschneider & Dandor BPE; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

#### `Evaporator_Features.md` — Evaporator Features
- **Scope & Behavior**: Sugars can simulate the operation of many different evaporator types.
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

#### `Evaporator_Properties.md` — Evaporator Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Kadlec, Bretschneider & Dandor BPE; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

---

### Examples
**Category**: Full Factory & Refinery Flowsheet Models  
**Path**: `.agents/skills/sugars-helpbook/references/Examples/`  

#### `4-Effect_Multiple.md` — 4-Effect Multiple
- **Scope & Behavior**: The flow diagram for a model of a four-effect multiple-effect evaporator
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `6-Effect_Multiple.md` — 6-Effect Multiple
- **Scope & Behavior**: thin juice heating, thermocompression, split condensate flashing, and
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Beet_Factory.md` — Beet Factory
- **Scope & Behavior**: The flow diagram for the beet factory example model is a five page
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

#### `Beet_Sugar_End.md` — Beet Sugar End
- **Scope & Behavior**: The flow diagram for a beet factory sugar end with a multiple-effect
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption; Van Hook supersaturation calculation

#### `Cane_Factory-Diffusion.md` — Cane Factory (Diffusion)
- **Scope & Behavior**: same as the milling factory except for the first
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Cane_Factory-Milling.md` — Cane Factory (Milling)
- **Scope & Behavior**: given in the Cane Factory (Milling)
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation

#### `Cane_Sugar_Refinery.md` — Refinery
- **Scope & Behavior**: The affination and purification model for a cane sugar refinery is shown
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Latent heat of vaporization & steam consumption; Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Examples.md` — About Examples
- **Scope & Behavior**: Twelve flow diagram example models are provided with Sugars. Each
- **Calculations & Models**: Latent heat of vaporization & steam consumption

#### `Fermentation_and_Distillation.md` — Fermentation and Distillation
- **Scope & Behavior**: to invert using a reactor station (no. 5100) and fermentation of invert
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Ion_Exchange.md` — Ion Exchange
- **Scope & Behavior**: The flow diagram for the Ion Exchange example of a generic ion exchange
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient

#### `Molasses_Desugarization.md` — Molasses Desugarization
- **Scope & Behavior**: The example model for molasses desugarization is a two page model. Page
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Single_Crystallization.md` — Single Crystallization
- **Scope & Behavior**: The flow diagram for the Single Crystallization example is shown below.
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Latent heat of vaporization & steam consumption; Kadlec, Bretschneider & Dandor BPE; Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Steam_Pulp_Dryer.md` — Steam Pulp Dryer
- **Scope & Behavior**: The flow diagram for the Steam Pulp Dryer example model of a high
- **Calculations & Models**: Latent heat of vaporization & steam consumption

---

### Flash Tank
**Category**: Sensible Heat & Condensate Flash Recovery  
**Path**: `.agents/skills/sugars-helpbook/references/Flash_Tank/`  

#### `Flash_Tank_Examples.md` — Flash Tank Examples
- **Scope & Behavior**: In some cases, the Output Flow Temperature, or Vapor Out Pressure aren't
- **Calculations & Models**: Kadlec, Bretschneider & Dandor BPE

#### `Flash_Tank_Features.md` — Flash Tank Features
- **Scope & Behavior**: Flash Tank A flash tank station is used to cool a material flow stream
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance

#### `Flash_Tank_Properties.md` — Flash Tank Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Kadlec, Bretschneider & Dandor BPE; Crystal content & mother liquor exhaustion balance

---

### Heat Exchanger
**Category**: Indirect Heating (Shell & Tube, Plate)  
**Path**: `.agents/skills/sugars-helpbook/references/Heat_Exchanger/`  

#### `Heat_Exchanger_Examples.md` — Heat Exchanger Examples
- **Scope & Behavior**: below.</span><span style="mso-spacerun: yes;"> </span><span class="hcp2"> The
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Heat_Exchanger_Features.md` — Heat Exchanger Features
- **Scope & Behavior**: Heat Exchanger A heat exchanger station is used to transfer heat between
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Heat_Exchanger_Properties.md` — Heat Exchanger Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Injection Heater
**Category**: Direct Steam Massecuite / Juice Heating  
**Path**: `.agents/skills/sugars-helpbook/references/Injection_Heater/`  

#### `Injection_Heater_Examples.md` — Injection Heater Examples
- **Scope & Behavior**: A model of an injection heater on massecuite before a centrifugal is
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Injection_Heater_Features.md` — Injection Heater Features
- **Scope & Behavior**: Injection Heater An injection heater station is used to heat a flow
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance

#### `Injection_Heater_Properties.md` — Injection Heater Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

---

### Introduction
**Category**: Simulation Architecture & System Conventions  
**Path**: `.agents/skills/sugars-helpbook/references/Introduction/`  

#### `Acknowledgement.md` — <span style="color: 000080; font-size: 12pt;">Acknowledgments</span>
- **Scope & Behavior**: Portions of this program are provided by NIST of the U.S. Department of
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Introduction.md` — Introduction
- **Scope & Behavior**: Sugars<span style="vertical-align: Super; font-size: 6pt;">TM</span> for
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Kadlec, Bretschneider & Dandor BPE; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `License_Agreement.md` — License Agreement
- **Scope & Behavior**: Sugars software is provided pursuant to a signed License Agreement
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Sugars_Service_and_Support.md` — Sugars Service and Support
- **Scope & Behavior**: Sugars is technically supported and serviced by Sugars International

---

### Melter
**Category**: Crystal Dissolution & Melt Liquor Preparation  
**Path**: `.agents/skills/sugars-helpbook/references/Melter/`  

#### `Melter_Examples.md` — Melter Examples
- **Scope & Behavior**: Output Temperature and %DS The output flow from the melter can be
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Melter_Features.md` — Melter Features
- **Scope & Behavior**: Melter A melter station is used to combine flow streams and melt sucrose
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Melter_Properties.md` — Melter Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Overview
**Category**: Process Flowsheet Topology & File Architecture  
**Path**: `.agents/skills/sugars-helpbook/references/Overview/`  

#### `File_Structure.md` — File Structure
- **Scope & Behavior**: Data for each model is stored in a Microsoft Access
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Flow_Diagram.md` — Flow Diagram
- **Scope & Behavior**: Sugars is used to analyze a sugar factory process by constructing a flow
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation

#### `Program_Overview.md` — Program Overview
- **Scope & Behavior**: to provide a full graphical interface for building models of sugar
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Kadlec, Bretschneider & Dandor BPE; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

---

### Pan
**Category**: Vacuum Pan Boiling & Evaporative Crystallization  
**Path**: `.agents/skills/sugars-helpbook/references/Pan/`  

#### `Pan_Examples.md` — Pan Examples
- **Scope & Behavior**: Massecuite Out Required The syrup flow in and massecuite flow out can
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Pan_Features.md` — Pan Features
- **Scope & Behavior**: Sugars can simulate the operation of both batch and continuous pans. The
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Pan_Properties.md` — Pan Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Kadlec, Bretschneider & Dandor BPE; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

---

### Pressure Reducer
**Category**: Steam Pressure Reduction & Desuperheating  
**Path**: `.agents/skills/sugars-helpbook/references/Pressure_Reducer/`  

#### `Pressure_Reducer_Examples.md` — Pressure Reducer Examples
- **Scope & Behavior**: A pressure reducing station is used in the flow diagram below to allow
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Pressure_Reducer_Features.md` — Pressure Reducer Features
- **Scope & Behavior**: Pressure Reducer As its name implies, a pressure reducer station is used
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Pressure_Reducer_Properties.md` — Pressure Reducer Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

---

### Program Operation
**Category**: Stream Mechanics, Connectivity & Boundaries  
**Path**: `.agents/skills/sugars-helpbook/references/Program_Operation/`  

#### `Cross-Page_and_On-Page_Connectors.md` — Cross-Page and On-Page Connectors
- **Scope & Behavior**: shapes that are used to make connections between stations that are on
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Data_Import_Export.md` — Data Import/Export
- **Scope & Behavior**: Importing data from and/or exporting data to an e**X**tensible
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Exporting_Data_to_Excel.md` — Exporting Data to Excel
- **Scope & Behavior**: The Cane Factory (Milling) example model provided with Sugars has an
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `External_Flows.md` — External Flows
- **Scope & Behavior**: sources such as: cane or beets, cold water, chemicals, lime,
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Grouped_Stations.md` — Grouped Stations
- **Scope & Behavior**: Stations can be grouped together to represent an actual station in the
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Internal_Flows.md` — Internal Flows
- **Scope & Behavior**: Internal flows are flows that connect stations, or that go out of the
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Program_Operation.md` — Program Operation
- **Scope & Behavior**: Models are built either by modifying one of the example models, or by
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

#### `Shape_Data_Display.md` — Shape Data Display
- **Scope & Behavior**: Every flow stream and station in a model has a Visio
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation; Latent heat of vaporization & steam consumption

---

### Pump
**Category**: Hydraulic Fluid Power & Head Addition  
**Path**: `.agents/skills/sugars-helpbook/references/Pump/`  

#### `Pump_Examples.md` — Pump Examples
- **Scope & Behavior**: The diagram below shows a juice pump increasing the pressure of a flow

#### `Pump_Features.md` — Pump Features
- **Scope & Behavior**: Pump A pump station is used to increase the pressure of a flow stream.
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

#### `Pump_Properties.md` — Pump Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Reactor
**Category**: Chemical Reaction & Liming Carbonatation  
**Path**: `.agents/skills/sugars-helpbook/references/Reactor/`  

#### `Reactor_Examples.md` — Reactor Examples
- **Scope & Behavior**: New solubility equation coefficients can be specified if the reaction
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Reactor_Features.md` — Reactor Features
- **Scope & Behavior**: Reactor  A reactor station is used to model chemical reactions that
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

#### `Reactor_Properties.md` — Reactor Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation

---

### Receiver
**Category**: Surge Vessel & Intermediate Buffer Storage  
**Path**: `.agents/skills/sugars-helpbook/references/Receiver/`  

#### `Receiver_Examples.md` — Receiver Examples
- **Scope & Behavior**: The figure below shows a receiver station with a pressure feedback flow
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Receiver_Features.md` — Receiver Features
- **Scope & Behavior**: Receiver  A receiver station is used to combine up to ten (10) input
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

#### `Receiver_Properties.md` — Receiver Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Separator Filter
**Category**: Cake Filtration & Solid-Liquid Clarification  
**Path**: `.agents/skills/sugars-helpbook/references/Separator_Filter/`  

#### `Separator_Filter_Examples.md` — Separator/Filter Examples
- **Scope & Behavior**: be specified as a ratio of one of the components in the input flow, or
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Bartens / ICUMSA specific heat & enthalpy summation; Centrifugal mother liquor & wash purging efficiency

#### `Separator_Filter_Features.md` — Separator/Filter Features
- **Scope & Behavior**: The separator/filter station is used to split a material flow stream
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Centrifugal mother liquor & wash purging efficiency; Bartens / ICUMSA specific heat & enthalpy summation

#### `Separator_Filter_Properties.md` — Separator/Filter Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Station Modules
**Category**: Custom Stencils & Shape Composition  
**Path**: `.agents/skills/sugars-helpbook/references/Station_Modules/`  

#### `About_Station_Modules.md` — About Station Modules
- **Scope & Behavior**: construct a flow diagram of the process being evaluated. Shapes for each
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Centrifugal mother liquor & wash purging efficiency

#### `Designing_Your_Own_Shapes.md` — Designing Your Own Shapes
- **Scope & Behavior**: Visio Developer Mode is necessary to design shapes for use with
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Grouping_Shapes.md` — Grouping Shapes
- **Scope & Behavior**: Shapes can be grouped together to add them to a model all at one
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Sucrose Supersaturation
**Category**: Physical Chemistry of Supersaturation  
**Path**: `.agents/skills/sugars-helpbook/references/Sucrose_Supersaturation/`  

#### `Supersaturation.md` — Supersaturation
- **Scope & Behavior**: alt="image\ebx_-1903615507.jpg" />
- **Calculations & Models**: Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Van Hook supersaturation calculation

---

### Surface Condenser
**Category**: Indirect Surface Condensing & Condensate Recovery  
**Path**: `.agents/skills/sugars-helpbook/references/Surface_Condenser/`  

#### `Surface_Condenser_Examples.md` — Surface Condenser Examples
- **Scope & Behavior**: The figure below shows a surface condenser condensing vapor from an
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Surface_Condenser_Features.md` — Surface Condenser Features
- **Scope & Behavior**: Surface Condenser  A surface condenser station is used to condense vapor
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Surface_Condenser_Properties.md` — Surface Condenser Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Tank
**Category**: Atmospheric & Pressurized Storage Vessels  
**Path**: `.agents/skills/sugars-helpbook/references/Tank/`  

#### `Tank_Examples.md` — Tank Examples
- **Scope & Behavior**: Output Flow TDM %  <span class="hcp3">The figure below shows a molasses
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Tank_Features.md` — Tank Features
- **Scope & Behavior**: Tank A tank station is used to combine flow streams, melt sucrose
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation; Van Hook supersaturation calculation

#### `Tank_Properties.md` — Tank Properties
- **Scope & Behavior**: Equipment ID  An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Theory
**Category**: Physical Chemistry, Solubility, BPE, Heat Content  
**Path**: `.agents/skills/sugars-helpbook/references/Theory/`  

#### `Theory.md` — <span id="Theory"></span>Theory
- **Scope & Behavior**: Many equations are used by Sugars to calculate the mass and energy
- **Calculations & Models**: Van Hook supersaturation calculation; Vavrinecz / Wagnerowski sucrose solubility & saturation coefficient; Kadlec, Bretschneider & Dandor BPE; Centrifugal mother liquor & wash purging efficiency; Crystal content & mother liquor exhaustion balance; Bartens / ICUMSA specific heat & enthalpy summation

---

### Thermocompressor
**Category**: Ejector / Thermo-Vapour Recompression (TVR)  
**Path**: `.agents/skills/sugars-helpbook/references/Thermocompressor/`  

#### `Thermocompressor_Examples.md` — Thermocompressor Examples
- **Scope & Behavior**: A thermocompressor station recompressing pan vapor is shown
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Thermocompressor_Features.md` — Thermocompressor Features
- **Scope & Behavior**: thermocompressor station is used to recompress a low pressure suction
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Thermocompressor_Properties.md` — Thermocompressor Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

---

### Turbine
**Category**: Mechanical Drive Steam Turbines  
**Path**: `.agents/skills/sugars-helpbook/references/Turbine/`  

#### `Turbine_Examples.md` — Turbine Examples
- **Scope & Behavior**: The figure below shows a steam turbine producing 4.0 megawatts of power
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Turbine_Features.md` — Turbine Features
- **Scope & Behavior**: Turbine  A turbine station is used to simulate the power produced by the
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Turbine_Properties.md` — Turbine Properties
- **Scope & Behavior**: Equipment ID An equipment ID of up to 11 characters can be used to
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Turbine steam expansion & power generation; Bartens / ICUMSA specific heat & enthalpy summation

---

### Turbo Alternator
**Category**: Cogeneration & Electric Power Generation  
**Path**: `.agents/skills/sugars-helpbook/references/Turbo_Alternator/`  

#### `Turbo_Alternator_Examples.md` — Turbo Alternator Examples
- **Scope & Behavior**: The figure below shows a turbo alternator producing 5.0 megawatts of
- **Calculations & Models**: Bartens / ICUMSA specific heat & enthalpy summation

#### `Turbo_Alternator_Features.md` — Turbo Alternator Features
- **Scope & Behavior**: Turbo Alternator A turbo alternator station is used to simulate the
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.

#### `Turbo_Alternator_Properties.md` — Turbo Alternator Properties
- **Scope & Behavior**: style="border: none;" data-border="0" />
- **Role**: Equipment definition with interactive properties, operational specifications, and mathematical solvers.
- **Calculations & Models**: Turbine steam expansion & power generation; Bartens / ICUMSA specific heat & enthalpy summation

---
