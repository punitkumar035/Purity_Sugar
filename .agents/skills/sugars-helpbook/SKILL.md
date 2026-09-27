---
name: sugars-helpbook
description: Reference library from the SUGARS (SBI) process-simulation help book — Properties, Features, Examples and Evaluations for sugar-factory/refinery unit operations (Pan, Evaporator, Centrifugal, Crystallizer, Cooler, Dryer, Heat Exchanger, Compressor, Thermocompressor, Turbine, Turbo Alternator, Pump, Tank, Reactor, Receiver, Separator/Filter, Condensers, Flash Tank, Injection Heater, Melter, Blender, Distributor, Pressure Reducer), plus core Theory (Vavrinecz sucrose solubility, boiling point elevation, crystal content, heat content, centrifugal calcs, supersaturation) and worked flow-sheet Examples (multi-effect evaporators, beet/cane factories, refinery, fermentation, ion exchange, molasses desugarization, crystallization, dryers). ALWAYS consult for sugar unit-operation design data, properties, governing equations, or mass/energy-balance theory, even without saying "SUGARS", e.g. "pan station balance", "Vavrinecz equation", "boiling point elevation", "centrifugal purge calc", "6-effect evaporator train".
---

# Sugars Helpbook

This skill packages the reference manual ("help book") for the **SUGARS** cane/beet sugar-factory and refinery process-simulation software (SBI). It is a comprehensive, authoritative reference on sugar-industry unit operations — their properties/inputs, features, governing theory, and fully worked examples — independent of whether the user is actually running the SUGARS software.

Use it whenever the user's question touches sugar-plant unit operations, mass/energy balance modeling of a station, or the equations behind sugar process calculations. Treat it as the first place to check before answering from general knowledge, since it contains SUGARS' specific conventions, default assumptions, and equation forms (which may differ in notation from other textbooks).

## How to use this skill

1. **Identify the module or topic** the question is about (e.g. "Pan", "Evaporator", "Centrifugal", "Theory").
2. **Open only the relevant reference file(s)** below — don't load the whole library. Each module typically has up to four files:
   - `*_Properties.md` — input fields / data entry screen for that station (what the user configures)
   - `*_Features.md` — capabilities, options, and configuration choices the station supports
   - `*_Examples.md` — short worked usage notes for that station
   - `*_Evaluations.md` — for Centrifugals only: performance/evaluation screens
3. For **equations and theory** (sucrose solubility, boiling point elevation, crystal content, heat content, centrifugal calculations, supersaturation), go straight to `references/Theory/Theory.md` and `references/Sucrose_Supersaturation/Supersaturation.md`.
4. For **full flow-sheet worked examples** (entire factories/refineries, not single stations), use `references/Examples/`.
5. For **how the software itself works** (file structure, flow diagrams, data import/export, grouped stations, connectors), use `references/Overview/` and `references/Program_Operation/`.
6. Images referenced from the markdown (screenshots, diagrams, equation graphics) live under `assets/images/<Category>/` — view them with the `view` tool if a diagram would help answer the question (e.g. an equation rendered as an image, or a property-screen screenshot).
7. Synthesize the answer in your own words for the user; don't dump raw file contents verbatim unless they explicitly ask for the manual text itself.

## Module index

| Module | Reference files (under `references/<Module>/`) |
|---|---|
| Blender | Blender_Examples, Blender_Features, Blender_Properties |
| Centrifugal | Centrifugal_Features, Centrifugal_Examples, Centrifugal_Evaluations, 2-Output_Centrifugal_Properties, 2-Output_Centrifugal_Evaluation, 3-Output_Centrifugal_Properties, 3-Output_Centrifugal_Evaluation |
| Compressor | Compressor_Examples, Compressor_Features, Compressor_Properties |
| Contact_Condenser | Contact_Condenser_Examples, Contact_Condenser_Features, Contact_Condenser_Properties |
| Cooler | Cooler_Examples, Cooler_Features, Cooler_Properties |
| Crystallizer | Crystallizer_Examples, Crystallizer_Features, Crystallizer_Properties |
| Distributor | Distributor_Examples, Distributor_Features, Distributor_Properties |
| Dryer | Dryer_Examples, Dryer_Features, Dryer_Properties |
| Evaporator | Evaporator_Examples, Evaporator_Features, Evaporator_Properties |
| Flash_Tank | Flash_Tank_Examples, Flash_Tank_Features, Flash_Tank_Properties |
| Heat_Exchanger | Heat_Exchanger_Examples, Heat_Exchanger_Features, Heat_Exchanger_Properties |
| Injection_Heater | Injection_Heater_Examples, Injection_Heater_Features, Injection_Heater_Properties |
| Melter | Melter_Examples, Melter_Features, Melter_Properties |
| Pan | Pan_Examples, Pan_Features, Pan_Properties |
| Pressure_Reducer | Pressure_Reducer_Examples, Pressure_Reducer_Features, Pressure_Reducer_Properties |
| Pump | Pump_Examples, Pump_Features, Pump_Properties |
| Reactor | Reactor_Examples, Reactor_Features, Reactor_Properties |
| Receiver | Receiver_Examples, Receiver_Features, Receiver_Properties |
| Separator_Filter | Separator_Filter_Examples, Separator_Filter_Features, Separator_Filter_Properties |
| Surface_Condenser | Surface_Condenser_Examples, Surface_Condenser_Features, Surface_Condenser_Properties |
| Tank | Tank_Examples, Tank_Features, Tank_Properties |
| Thermocompressor | Thermocompressor_Examples, Thermocompressor_Features, Thermocompressor_Properties |
| Turbine | Turbine_Examples, Turbine_Features, Turbine_Properties |
| Turbo_Alternator | Turbo_Alternator_Examples, Turbo_Alternator_Features, Turbo_Alternator_Properties |

## Theory & fundamentals

- `references/Theory/Theory.md` — sucrose solubility (Vavrinecz/ICUMSA equation), saturation coefficient, crystal content, heat content, boiling point elevation, centrifugal calculations. This is the core equations reference.
- `references/Sucrose_Supersaturation/Supersaturation.md` — supersaturation calculation and sucrose solubility curve.
- `references/Error_Messages/Error_Messages.md` — meaning of SUGARS software error/warning messages.

## Worked flow-sheet examples

`references/Examples/` — full-factory examples: 4-Effect_Multiple, 6-Effect_Multiple, Beet_Factory, Beet_Sugar_End, Cane_Factory-Diffusion, Cane_Factory-Milling, Cane_Sugar_Refinery, Fermentation_and_Distillation, Ion_Exchange, Molasses_Desugarization, Single_Crystallization, Steam_Pulp_Dryer.

## Software overview & operation (SUGARS-specific, not general process theory)

- `references/Overview/` — Program_Overview, Flow_Diagram, File_Structure
- `references/Program_Operation/` — Program_Operation, Internal_Flows, External_Flows, Cross-Page_and_On-Page_Connectors, Grouped_Stations, Data_Import_Export, Exporting_Data_to_Excel, Shape_Data_Display
- `references/Station_Modules/` — About_Station_Modules, Designing_Your_Own_Shapes, Grouping_Shapes
- `references/Introduction/` — Introduction, Acknowledgement, License_Agreement, Sugars_Service_and_Support

## Notes

- All content is converted from the original SUGARS help book (`sugars.chm`, RoboHelp/HTML Help format) to Markdown for easy searching; equation graphics and screenshots are preserved as images under `assets/images/`.
- Some internal cross-reference links inside files (e.g. links to anchors in `Theory.htm`) point back to the original `.htm` filename — they still correctly identify the section heading to search for within the corresponding `.md` file.
