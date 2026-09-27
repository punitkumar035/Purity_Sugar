Attribute VB_Name = "StationDialogManager"
'
' ╔══════════════════════════════════════════════════════════════════╗
' ║  Purity for Sugar  —  StationDialogManager.bas                  ║
' ║  Phase 01  |  v1.0  |  Field specifications for all 24 types    ║
' ╚══════════════════════════════════════════════════════════════════╝
'
' SOURCE RULES: RULES_v4.md §14 (Station Properties Windows — All 24 Types)
'
' Every field, border type, and constraint in this file is sourced
' from a specific *_Properties.htm file in sugars.zip.
'
' BORDER TYPES (§14 header):
'   MX_BLUE    — Normal field, always accessible
'   MX_MAGENTA — Exactly ONE must be selected; selecting one greys the rest
'   MX_MAROON  — ONE OR NONE may be selected
'
' ──────────────────────────────────────────────────────────────────
Option Explicit

' ── Border type identifiers ───────────────────────────────────────
Public Const MX_BLUE    As String = "B"
Public Const MX_MAGENTA As String = "M"
Public Const MX_MAROON  As String = "R"

' ── Field type codes ──────────────────────────────────────────────
Public Const FT_NUMBER  As Integer = 1   ' Numeric entry
Public Const FT_TEXT    As Integer = 2   ' Free-text entry
Public Const FT_SELECT  As Integer = 3   ' Drop-down selection
Public Const FT_CHECK   As Integer = 4   ' Checkbox (0/1)
Public Const FT_SECTION As Integer = 5   ' Visual separator, no input
Public Const FT_CALCONLY As Integer = 6  ' Calculated — display only

' ── FieldSpec type ────────────────────────────────────────────────
' One entry on a Properties window.
' PropKey maps directly to Visio Shape Data row: Prop.<PropKey>
Public Type FieldSpec
    PropKey   As String     ' Shape Data key (no "Prop." prefix)
    Label     As String     ' Display label shown to user
    FieldType As Integer    ' FT_* constant
    Border    As String     ' MX_BLUE / MX_MAGENTA / MX_MAROON
    GroupID   As Integer    ' Mutex group number (1,2,…). 0 = no group.
    Options   As String     ' For FT_SELECT: comma-separated choices
    Hint      As String     ' Short description / constraint note
    Required  As Boolean    ' True = blank not acceptable before saving
    CalcOnly  As Boolean    ' True = shown after balance, not entered
End Type


'═══════════════════════════════════════════════════════════════════
' BuildFieldSpecs
' Returns the complete ordered field list for a station type.
' CommonFields (StationName, EquipmentID) are always prepended.
'═══════════════════════════════════════════════════════════════════
Public Function BuildFieldSpecs(stationType As String) As FieldSpec()
    Dim c() As FieldSpec : c = CommonFields()
    Dim s() As FieldSpec

    Select Case LCase(stationType)

    ' ─────────────────────────────────────────────────────────────
    ' EVAPORATOR  [Evaporator_Properties.htm]
    ' Magenta group 1: HTC | VaporPressure | PressureFeedback | FlowOutTemp
    ' ─────────────────────────────────────────────────────────────
    Case "evaporator"
        ReDim s(14)
        s(0)  = Sec("Control Mode — choose exactly one (Magenta)")
        s(1)  = Fld("HeatTransferCoef",  "Heat Transfer Coefficient (W/m²·K)", FT_NUMBER, MX_MAGENTA,1,"Cannot combine with Pressure/Temperature/Feedback")
        s(2)  = Fld("HeatingSurface",    "Heating Surface (m²)",               FT_NUMBER, MX_BLUE,  0,"Required when Coefficient is active")
        s(3)  = Fld("VaporPressure",     "Vapor Out Pressure (kPa)",           FT_NUMBER, MX_MAGENTA,1,"")
        s(4)  = Fld("SatTemperature",    "Saturation Temperature (°C)",        FT_NUMBER, MX_BLUE,  0,"Companion entry when Pressure selected")
        s(5)  = Fld("PressureFeedback",  "Pressure Feedback",                  FT_CHECK,  MX_MAGENTA,1,"Uses downstream condenser/receiver pressure")
        s(6)  = Fld("FlowOutTemperature","Flow Out Temperature (°C)",          FT_NUMBER, MX_MAGENTA,1,"")
        s(7)  = Sec("Other Parameters")
        s(8)  = Fld("HeatLoss",          "Heat Loss (%)",                      FT_NUMBER, MX_BLUE,  0,"% of heat transferred that is lost.  e.g. 2.0")
        s(9)  = Fld("CondensateDrop",    "Condensate Drop (K)",                FT_NUMBER, MX_BLUE,  0,"T drop of condensate below steam saturation T")
        s(10) = Fld("EffectNumber",      "Effect Number",                      FT_NUMBER, MX_BLUE,  0,"1=first (motive steam). Must be in sequence with station numbers. §16")
        s(11) = Fld("TotalSolids",       "Total Solids Out (%)",               FT_NUMBER, MX_BLUE,  0,"Specifies DS out; makes 1st-effect steam required. Only one per multiple. §16")
        s(12) = Fld("EntrainmentLoss",   "Entrainment Sugar Loss (ppm)",       FT_NUMBER, MX_BLUE,  0,"Sugar carried in vapor; droplets have same DS/purity as syrup out")
        s(13) = Fld("BPEFactor",         "BPE Factor",                         FT_NUMBER, MX_BLUE,  0,"Adjusts boiling point elevation calculation")
        s(14) = Fld("ColorRise",         "Color Rise (% or CU)",               FT_NUMBER, MX_BLUE,  0,"Color increase across this effect")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' PAN  [Pan_Properties.htm]
    ' Magenta group 1: VaporPressure | PressureFeedback | MassecuiteOutTemp
    ' Maroon group 2: TotalSolids | TargetMLPurity
    ' ─────────────────────────────────────────────────────────────
    Case "pan"
        ReDim s(12)
        s(0)  = Sec("Temperature Control — choose exactly one (Magenta)")
        s(1)  = Fld("VaporPressure",     "Vapor Out Pressure (kPa)",           FT_NUMBER, MX_MAGENTA,1,"")
        s(2)  = Fld("SatTemperature",    "Saturation Temperature (°C)",        FT_NUMBER, MX_BLUE,  0,"Companion entry when Pressure selected")
        s(3)  = Fld("PressureFeedback",  "Pressure Feedback",                  FT_CHECK,  MX_MAGENTA,1,"")
        s(4)  = Fld("MassecuiteOutTemp", "Massecuite Out Temperature (°C)",    FT_NUMBER, MX_MAGENTA,1,"")
        s(5)  = Sec("Massecuite Specification — choose one or none (Maroon)")
        s(6)  = Fld("TotalSolids",       "Total Solids / DS Out (%)",          FT_NUMBER, MX_MAROON, 2,"e.g. 94.50")
        s(7)  = Fld("TargetMLPurity",    "Target Mother Liquor Purity (%)",    FT_NUMBER, MX_MAROON, 2,"Cannot use with Total Solids")
        s(8)  = Fld("DSHighLimit",       "Massecuite DS High Limit (%)",       FT_NUMBER, MX_BLUE,  0,"Active when Target ML Purity used.  e.g. 94.00")
        s(9)  = Fld("DSLowLimit",        "Massecuite DS Low Limit (%)",        FT_NUMBER, MX_BLUE,  0,"Active when Target ML Purity used.  e.g. 88.00")
        s(10) = Sec("Always Required — Pan Steam (port 1) is ALWAYS a required flow (§9)")
        s(11) = Fld("Supersaturation",   "Supersaturation (Ss)",               FT_NUMBER, MX_BLUE,  0,"ICUMSA Van Hook definition.  e.g. 1.15")
        s(12) = Fld("HeatLoss",          "Heat Loss (%)",                      FT_NUMBER, MX_BLUE,  0,"Batch: 8–12%.  Continuous: lower.")
        Dim pa() As FieldSpec
        pa = Append(s, Fld("CondensateDrop",    "Condensate Drop (K)",           FT_NUMBER, MX_BLUE,0,""))
        pa = Append(pa, Fld("ColorRise",         "Color Rise (% or CU)",          FT_NUMBER, MX_BLUE,0,""))
        pa = Append(pa, Fld("EntrainmentLoss",   "Entrainment Sugar Loss (ppm)",  FT_NUMBER, MX_BLUE,0,"Droplets have same DS/purity as mother liquor"))
        pa = Append(pa, Fld("SolCoefA",          "Solubility Coefficient a",      FT_NUMBER, MX_BLUE,0,"Override only if massecuite differs from incoming syrup"))
        pa = Append(pa, Fld("SolCoefB",          "Solubility Coefficient b",      FT_NUMBER, MX_BLUE,0,""))
        pa = Append(pa, Fld("SolCoefC",          "Solubility Coefficient c",      FT_NUMBER, MX_BLUE,0,"0 = use Wagnerowski. Only valid NSW 1.6–3.5 (§25.3)"))
        BuildFieldSpecs = Merge(c, pa) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' CRYSTALLIZER  [Crystallizer_Properties.htm]
    ' ─────────────────────────────────────────────────────────────
    Case "crystallizer"
        ReDim s(5)
        s(0) = Fld("Supersaturation",  "Supersaturation (Ss)",          FT_NUMBER, MX_BLUE,0,"Required. Use Calculate button if not known.  e.g. 1.10")
        s(1) = Fld("TemperatureOut",   "Temperature Out (°C)",           FT_NUMBER, MX_BLUE,0,"Must be less than temperature in.  e.g. 54.0")
        s(2) = Fld("ColorRise",        "Color Rise (% or CU)",           FT_NUMBER, MX_BLUE,0,"e.g. 5.0% or 300 CU")
        s(3) = Fld("SolCoefA",         "Solubility Coefficient a",       FT_NUMBER, MX_BLUE,0,"Override if different from input flow")
        s(4) = Fld("SolCoefB",         "Solubility Coefficient b",       FT_NUMBER, MX_BLUE,0,"")
        s(5) = Fld("SolCoefC",         "Solubility Coefficient c",       FT_NUMBER, MX_BLUE,0,"")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' CENTRIFUGAL  [Centrifugal_Properties.htm, Centrifugal_Evaluations.htm]
    ' §15: Two-step evaluation — massecuite data first, then output data
    ' 3 Magenta fields: WashFlow, GreenDS, SugarDS — any two must be entered
    ' ─────────────────────────────────────────────────────────────
    Case "centrifugal"
        ReDim s(14)
        s(0)  = Fld("CentrifugalType",   "Type",                               FT_SELECT, MX_BLUE,  0,"2-Output,3-Output","2-Output=continuous/batch; 3-Output=batch only")
        s(1)  = Sec("STEP 1 — Massecuite Evaluation Data (§15.1)")
        s(2)  = Fld("MassecuiteDS",      "Massecuite DS (%)",                  FT_NUMBER, MX_BLUE,  0,"From actual factory sample.  e.g. 93.00")
        s(3)  = Fld("MassecuitePurity",  "Massecuite Purity (%)",              FT_NUMBER, MX_BLUE,  0,"e.g. 86.44")
        s(4)  = Fld("MassecuiteTemp",    "Massecuite Temperature (°C)",        FT_NUMBER, MX_BLUE,  0,"e.g. 81.0")
        s(5)  = Fld("MassecuiteSs",      "Massecuite Supersaturation (Ss)",    FT_NUMBER, MX_BLUE,  0,"e.g. 1.10")
        s(6)  = Fld("MassecuiteFlow",    "Massecuite Flow (m³/h or t/h)",      FT_NUMBER, MX_BLUE,  0,"For Wash/Massecuite ratio calculation")
        s(7)  = Sec("STEP 2 — Performance Data — 3 Magenta fields, enter any TWO (§15.2)")
        s(8)  = Fld("WashFlow",          "Wash Flow (m³/h or kg/h)",           FT_NUMBER, MX_MAGENTA,1,"")
        s(9)  = Fld("GreenDS",           "Green (Molasses) DS (%)",            FT_NUMBER, MX_MAGENTA,1,"")
        s(10) = Fld("SugarDS",           "Sugar DS (%)",                       FT_NUMBER, MX_MAGENTA,1,"Solver calculates the unselected Magenta field")
        s(11) = Sec("Green Out")
        s(12) = Fld("GreenPurity",       "Green Purity (%)",                   FT_NUMBER, MX_BLUE,  0,"")
        s(13) = Fld("GreenTemperature",  "Green Temperature (°C)",             FT_NUMBER, MX_BLUE,  0,"")
        s(14) = Sec("Sugar Out")
        Dim cf() As FieldSpec
        cf = Append(s, Fld("SugarPurity",     "Sugar Purity (%)",             FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Fld("SugarTemperature","Sugar Temperature (°C)",       FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Sec("Wash Input"))
        cf = Append(cf, Fld("WashTemperature", "Wash Temperature (°C)",        FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Fld("WashQuality",     "Wash Water/Steam Quality (%)", FT_NUMBER, MX_BLUE,0,"100=all steam  0=all water"))
        cf = Append(cf, Fld("WashSyrupDS",     "Wash Syrup DS (%)",            FT_NUMBER, MX_BLUE,0,"If syrup wash"))
        cf = Append(cf, Fld("WashSyrupPurity", "Wash Syrup Purity (%)",        FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Sec("3-Output Only — all three fields required"))
        cf = Append(cf, Fld("WashOutDS",       "Wash Out DS (%)",              FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Fld("WashOutPurity",   "Wash Out Purity (%)",          FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Fld("WashOutTemp",     "Wash Out Temperature (°C)",    FT_NUMBER, MX_BLUE,0,""))
        cf = Append(cf, Sec("Iteration Method — §15.3"))
        cf = Append(cf, Fld("UseResidualData", "Use Residual Data for Iterations (default)", FT_CHECK, MX_BLUE,0,"Default. Holds mother liquor residue on crystals."))
        BuildFieldSpecs = Merge(c, cf) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' BLENDER  [Blender_Properties.htm]
    ' Magenta group 1: Ratio | BlendQty | NSWOut | QuantityOut |
    '                  DSOut | PurityOut | TempOut | ComponentPct
    ' Blend flow (port 1) is ALWAYS required (§9.1)
    ' ─────────────────────────────────────────────────────────────
    Case "blender"
        ReDim s(8)
        s(0) = Sec("NOTE: Blend flow (port 1) is ALWAYS a required flow (§9.1)")
        s(1) = Sec("Blend Control — choose exactly one (Magenta)")
        s(2) = Fld("Ratio",          "Ratio (blend / primary component)",FT_NUMBER, MX_MAGENTA,1,"e.g. 0.3")
        s(3) = Fld("RatioComponent", "Component for Ratio",              FT_SELECT, MX_BLUE,  0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor","Used with Ratio field")
        s(4) = Fld("BlendQuantity",  "Blend Quantity (kg/h)",            FT_NUMBER, MX_MAGENTA,1,"Fixed weight added to primary flow")
        s(5) = Fld("NSWOut",         "Non-Sugar to Water Ratio Out",     FT_NUMBER, MX_MAGENTA,1,"Target NSW in output")
        s(6) = Fld("QuantityOut",    "Output Quantity (kg/h)",           FT_NUMBER, MX_MAGENTA,1,"Target total output flow")
        s(7) = Fld("DSOut",          "Dry Substance Out (%)",            FT_NUMBER, MX_MAGENTA,1,"Target DS in output")
        s(8) = Fld("PurityOut",      "Purity Out (%)",                   FT_NUMBER, MX_MAGENTA,1,"Target purity in output")
        Dim bl() As FieldSpec
        bl = Append(s, Fld("TemperatureOut",  "Temperature Out (°C)",     FT_NUMBER, MX_MAGENTA,1,""))
        bl = Append(bl, Fld("ComponentOut",  "Component Out",             FT_SELECT, MX_MAGENTA,1,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2","Used with Component % field"))
        bl = Append(bl, Fld("ComponentPct",  "Component Percent (%)",     FT_NUMBER, MX_BLUE,  0,"Target % of selected component in output"))
        BuildFieldSpecs = Merge(c, bl) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' DISTRIBUTOR  [Distributor_Properties.htm]
    ' Up to 10 output ports (0–9). Overflow → lowest unspecified port.
    ' Cannot mix % mode and required flows.
    ' ─────────────────────────────────────────────────────────────
    Case "distributor"
        ReDim s(11)
        s(0)  = Sec("Quantity Mode — choose one (Magenta)")
        s(1)  = Fld("UseQuantityKGH", "Quantity kg/h mode",     FT_CHECK,  MX_MAGENTA,1,"Cannot use % if any output is a required flow")
        s(2)  = Fld("UseQuantityPCT", "Quantity % mode",        FT_CHECK,  MX_MAGENTA,1,"All percentages must sum to 100%")
        s(3)  = Sec("Output Port Quantities — overflow → lowest unspecified port (§14 Distributor)")
        s(4)  = Fld("Quantity0",  "Output Port 0", FT_NUMBER, MX_BLUE,0,"kg/h or %")
        s(5)  = Fld("Quantity1",  "Output Port 1", FT_NUMBER, MX_BLUE,0,"")
        s(6)  = Fld("Quantity2",  "Output Port 2", FT_NUMBER, MX_BLUE,0,"")
        s(7)  = Fld("Quantity3",  "Output Port 3", FT_NUMBER, MX_BLUE,0,"")
        s(8)  = Fld("Quantity4",  "Output Port 4", FT_NUMBER, MX_BLUE,0,"")
        s(9)  = Fld("Quantity5",  "Output Port 5", FT_NUMBER, MX_BLUE,0,"")
        s(10) = Fld("Quantity6",  "Output Port 6", FT_NUMBER, MX_BLUE,0,"")
        s(11) = Fld("Quantity7",  "Output Port 7", FT_NUMBER, MX_BLUE,0,"")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' HEAT EXCHANGER  [Heat_Exchanger_Properties.htm]
    ' Magenta group 1: TempOut | TempRise | Approach (port 0)
    ' Maroon group 2: HeatTransferCoef | Effectiveness
    ' ─────────────────────────────────────────────────────────────
    Case "heat_exchanger"
        ReDim s(11)
        s(0)  = Sec("Port 0 Temperature Control — choose exactly one (Magenta)")
        s(1)  = Fld("TemperatureOut",  "Temperature Out, Port 0 (°C)",   FT_NUMBER, MX_MAGENTA,1,"")
        s(2)  = Fld("TemperatureRise", "Temperature Rise, Port 0 (K)",   FT_NUMBER, MX_MAGENTA,1,"")
        s(3)  = Fld("Approach",        "Approach Temperature (°C)",      FT_NUMBER, MX_MAGENTA,1,"T1out − T0out. Can be negative.")
        s(4)  = Fld("Port1Required",   "Port 1 Input Flow Required",     FT_CHECK,  MX_BLUE,  0,"Default ON. Uncheck if port 1 quantity is known.")
        s(5)  = Fld("TempOutPort1",    "Temperature Out, Port 1 (°C)",   FT_NUMBER, MX_BLUE,  0,"Enter when both flow T known — calculates effectiveness/HTC")
        s(6)  = Sec("Heat Transfer — choose one or none (Maroon)")
        s(7)  = Fld("HeatTransferCoef","Heat Transfer Coefficient (W/m²·K)",FT_NUMBER,MX_MAROON,2,"Requires Heating Surface")
        s(8)  = Fld("Effectiveness",   "Effectiveness (%)",              FT_NUMBER, MX_MAROON, 2,"Uses actual T, not saturation T (§14 HX)")
        s(9)  = Fld("HeatingSurface",  "Heating Surface (m²)",           FT_NUMBER, MX_BLUE,  0,"Required with Coefficient.  e.g. 35.0")
        s(10) = Fld("HeatLoss",        "Heat Loss (%)",                  FT_NUMBER, MX_BLUE,  0,"")
        s(11) = Fld("CondensateDrop",  "Condensate Drop (K)",            FT_NUMBER, MX_BLUE,  0,"")
        Dim hx() As FieldSpec
        hx = Append(s, Fld("FlowDirection", "Flow Direction", FT_SELECT, MX_BLUE, 0,"Counter,Parallel",""))
        hx = Append(hx, Fld("HXType",       "Type",           FT_SELECT, MX_BLUE, 0,"Condensing,Non-Condensing","Condensing: saturation T used for LMTD (§14 HX)"))
        BuildFieldSpecs = Merge(c, hx) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' INJECTION HEATER  [Injection_Heater_Properties.htm]
    ' Magenta group 1: TempOut | TempRise
    ' Heating flow (port 1) is always required (§9.1)
    ' ─────────────────────────────────────────────────────────────
    Case "injection_heater"
        ReDim s(3)
        s(0) = Sec("NOTE: Heating flow (port 1) is always required (§9.1)")
        s(1) = Fld("TemperatureOut",  "Temperature Out (°C)",  FT_NUMBER, MX_MAGENTA,1,"Heating flow quantity will be calculated")
        s(2) = Fld("TemperatureRise", "Temperature Rise (K)",  FT_NUMBER, MX_MAGENTA,1,"")
        s(3) = Fld("HeatLoss",        "Heat Loss (%)",          FT_NUMBER, MX_BLUE,  0,"")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' FLASH TANK  [Flash_Tank_Properties.htm]
    ' Magenta group 1: VaporPressure | PressureFeedback | OutputFlowTemp
    ' No crystal growth (§11)
    ' ─────────────────────────────────────────────────────────────
    Case "flash_tank"
        ReDim s(5)
        s(0) = Sec("Vapor Out Control — choose exactly one (Magenta)")
        s(1) = Fld("VaporPressure",   "Vapor Out Pressure (kPa)",        FT_NUMBER, MX_MAGENTA,1,"")
        s(2) = Fld("SatTemperature",  "Saturation Temperature (°C)",     FT_NUMBER, MX_BLUE,  0,"Companion entry when Pressure selected")
        s(3) = Fld("PressureFeedback","Pressure Feedback",               FT_CHECK,  MX_MAGENTA,1,"Pressure set by downstream receiver")
        s(4) = Fld("OutputFlowTemp",  "Output Flow Temperature (°C)",    FT_NUMBER, MX_MAGENTA,1,"")
        s(5) = Fld("EntrainmentLoss", "Entrainment Sugar Loss (ppm)",    FT_NUMBER, MX_BLUE,  0,"Droplets have same DS/purity as liquid out")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' TANK  [Tank_Properties.htm]
    ' Magenta group 1: FlowToStorage | FlowFromStorage
    ' Output always at atmospheric pressure (§10.1)
    ' ─────────────────────────────────────────────────────────────
    Case "tank"
        ReDim s(7)
        s(0) = Sec("Storage Flow — choose one or neither (Magenta)")
        s(1) = Fld("FlowToStorage",   "Flow to Storage (m³/h)",          FT_NUMBER, MX_MAGENTA,1,"Tank level rises")
        s(2) = Fld("FlowFromStorage", "Flow from Storage (m³/h)",        FT_NUMBER, MX_MAGENTA,1,"Tank level falls")
        s(3) = Sec("Output Control")
        s(4) = Fld("HoldTDM",         "Hold TDM at (%)",                 FT_NUMBER, MX_BLUE,  0,"Active when port 9 connected.  e.g. 67.00")
        s(5) = Fld("TemperatureOut",  "Temperature Out (°C)",            FT_NUMBER, MX_BLUE,  0,"Active when port 10 (heating) connected")
        s(6) = Fld("ColorRise",       "Color Rise (% or CU)",            FT_NUMBER, MX_BLUE,  0,"")
        s(7) = Fld("HeatingType",     "Heating Type",                    FT_SELECT, MX_BLUE,  0,"Injection,Coil","Injection: heating mixes in; Coil: condensate leaves")
        Dim tk() As FieldSpec
        tk = Append(s, Fld("HeatLoss",      "Heat Loss (%)",             FT_NUMBER, MX_BLUE,0,""))
        tk = Append(tk, Fld("RequiredFlowID","Required Flow input port", FT_TEXT,   MX_BLUE,0,"Auto-shown when output required by another station"))
        BuildFieldSpecs = Merge(c, tk) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' REACTOR  [Reactor_Properties.htm]
    ' Can react up to 3 component pairs.
    ' Can also change solubility coefficients or colour WITHOUT reaction.
    ' ─────────────────────────────────────────────────────────────
    Case "reactor"
        ReDim s(10)
        s(0)  = Sec("Reaction 1  (up to 3 reactions supported — §14 Reactor)")
        s(1)  = Fld("InputComponent1", "Input Component 1",     FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor","MW must be in Model Properties (§17)")
        s(2)  = Fld("InputMole1",      "Input Mole % 1",        FT_NUMBER, MX_BLUE,0,"% of component that reacts.  e.g. 100")
        s(3)  = Fld("OutputComponent1","Output Component 1",    FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor","Product of reaction")
        s(4)  = Fld("OutputMole1",     "Output Mole % 1",       FT_NUMBER, MX_BLUE,0,"e.g. 100")
        s(5)  = Sec("Reaction Characteristics")
        s(6)  = Fld("ReactionEff",     "Reaction Efficiency (%)",FT_NUMBER, MX_BLUE,0,"e.g. 90 for carbonation")
        s(7)  = Fld("HeatReaction",    "Heat of Reaction (kJ/kg)",FT_NUMBER, MX_BLUE,0,"+ve=exothermic (T rises)  -ve=endothermic")
        s(8)  = Fld("ColorChange",     "Color Change (CU)",     FT_NUMBER, MX_BLUE,0,"+ve or -ve. Applied to N.S. #1 only (§12.5)")
        s(9)  = Sec("Solubility Coefficients for Output  (0=unchanged; usable without any reaction — §14 Reactor)")
        s(10) = Fld("SolCoefA",        "Coefficient a",         FT_NUMBER, MX_BLUE,0,"")
        Dim rx() As FieldSpec
        rx = Append(s, Fld("SolCoefB",  "Coefficient b",        FT_NUMBER, MX_BLUE,0,""))
        rx = Append(rx, Fld("SolCoefC", "Coefficient c  (0=Wagnerowski valid NSW 1.6–3.5 only)",FT_NUMBER, MX_BLUE,0,""))
        BuildFieldSpecs = Merge(c, rx) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' SEPARATOR / FILTER  [Separator_Filter_Properties.htm]
    ' Magenta group 1: NoRatio | DiluentRatio
    ' Up to 4 named component separations + Other Components
    ' ─────────────────────────────────────────────────────────────
    Case "separator_filter"
        ReDim s(5)
        s(0) = Sec("Diluent Flow Control — choose one (Magenta)")
        s(1) = Fld("NoRatio",          "No Ratio — diluent quantity is independent",  FT_CHECK,  MX_MAGENTA,1,"Use when diluent quantity is known")
        s(2) = Fld("DiluentRatio",     "Ratio  (diluent / input flow)",               FT_NUMBER, MX_MAGENTA,1,"e.g. 0.200")
        s(3) = Fld("DiluentComponent", "Ratio Component",                             FT_SELECT, MX_BLUE,  0,"Total,Water,DissolvedSucrose,NonSucrose1,Fiber","Component used as ratio base")
        s(4) = Fld("OutFlow1Pct",      "Out Flow No. 1 (% of diluent)",              FT_NUMBER, MX_BLUE,  0,"Remainder → Out Flow No. 2.  e.g. 30.0")
        s(5) = Sec("Component Separation — up to 4 named + Other (§14 Separator)")
        Dim sf() As FieldSpec
        sf = Append(s, Fld("Component1",    "Component 1", FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor",""))
        sf = Append(sf, Fld("Component1Pct","Component 1 → Out 1 (%)", FT_NUMBER, MX_BLUE,0,"% going to output 1; remainder to output 2"))
        sf = Append(sf, Fld("Component2",   "Component 2", FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor",""))
        sf = Append(sf, Fld("Component2Pct","Component 2 → Out 1 (%)", FT_NUMBER, MX_BLUE,0,""))
        sf = Append(sf, Fld("Component3",   "Component 3", FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor",""))
        sf = Append(sf, Fld("Component3Pct","Component 3 → Out 1 (%)", FT_NUMBER, MX_BLUE,0,""))
        sf = Append(sf, Fld("Component4",   "Component 4", FT_SELECT, MX_BLUE,0,"Total,Water,DissolvedSucrose,NonSucrose1,NonSucrose2,SucrosecrystALS,Fiber,CaO,CaCO3,CO2,NH3,WaterVapor",""))
        sf = Append(sf, Fld("Component4Pct","Component 4 → Out 1 (%)", FT_NUMBER, MX_BLUE,0,""))
        sf = Append(sf, Fld("OtherCompPct", "Other Components → Out 1 (%)", FT_NUMBER, MX_BLUE,0,"All remaining components"))
        sf = Append(sf, Fld("ColorPct",     "Color (%)",   FT_NUMBER, MX_BLUE,0,"100=normal split; <100=more colour to Out 2 (§12.3)"))
        BuildFieldSpecs = Merge(c, sf) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' DRYER  [Dryer_Properties.htm]
    ' Vapor out CANNOT be required (§9.3).
    ' ─────────────────────────────────────────────────────────────
    Case "dryer"
        ReDim s(4)
        s(0) = Fld("DryMatterOut",   "Output Dry Matter (%)",            FT_NUMBER, MX_BLUE,0,"100 minus moisture%.  e.g. 99.98")
        s(1) = Fld("TemperatureOut", "Temperature Out (°C)",             FT_NUMBER, MX_BLUE,0,"Flashing if < input temperature")
        s(2) = Fld("DryMatterLoss",  "Dry Matter Loss (ppm)",            FT_NUMBER, MX_BLUE,0,"Of total DM in feed (sucrose + non-sucrose)")
        s(3) = Fld("HeatLoss",       "Heat Loss (%)",                    FT_NUMBER, MX_BLUE,0,"% of heat transferred that is lost")
        s(4) = Fld("CondHeatEff",    "Condensate Heating Effectiveness (%)",FT_NUMBER,MX_BLUE,0,"0 for steam/vapor; 10–50% for liquid heating")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' COOLER  [Cooler_Properties.htm]
    ' Magenta group 1: TempDrop | TempOut | HeatLossPct | HeatLossKJKG
    ' No crystal growth — flow may become supersaturated (§11)
    ' ─────────────────────────────────────────────────────────────
    Case "cooler"
        ReDim s(4)
        s(0) = Sec("Cooling Control — choose exactly one (Magenta). No crystal growth. §11")
        s(1) = Fld("TemperatureDrop","Temperature Drop (K)",     FT_NUMBER, MX_MAGENTA,1,"Flow may become supersaturated")
        s(2) = Fld("TemperatureOut", "Temperature Out (°C)",     FT_NUMBER, MX_MAGENTA,1,"")
        s(3) = Fld("HeatLossPct",   "Heat Loss (%)",             FT_NUMBER, MX_MAGENTA,1,"% of total heat in input flow")
        s(4) = Fld("HeatLossKJKG",  "Heat Loss (kJ/kg or BTU/lb)",FT_NUMBER,MX_MAGENTA,1,"Absolute enthalpy loss")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' MELTER  [Melter_Properties.htm]
    ' Up to 10 process inputs (ports 0–9), 1 heating input (port 10)
    ' Output always at atmospheric (§10.1). Crystals dissolve to Ss=1 (§11)
    ' ─────────────────────────────────────────────────────────────
    Case "melter"
        ReDim s(5)
        s(0) = Fld("HoldTDM",        "Hold TDM at (%)",          FT_NUMBER, MX_BLUE,0,"Active when port 9 connected.  e.g. 67.00")
        s(1) = Fld("TemperatureOut", "Temperature Out (°C)",     FT_NUMBER, MX_BLUE,0,"Active when port 10 (heating) connected")
        s(2) = Fld("ColorRise",      "Color Rise (% or CU)",     FT_NUMBER, MX_BLUE,0,"")
        s(3) = Fld("HeatingType",    "Heating Type",             FT_SELECT, MX_BLUE,0,"Injection,Coil","Injection: heating mixes in; Coil: condensate leaves")
        s(4) = Fld("HeatLoss",       "Heat Loss (%)",            FT_NUMBER, MX_BLUE,0,"")
        s(5) = Fld("RequiredFlowID", "Required Flow input port", FT_TEXT,   MX_BLUE,0,"Auto-shown when output required by another station")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' RECEIVER  [Receiver_Properties.htm]
    ' No input data needed if output is not required.
    ' Output pressure = MINIMUM of all input pressures (§10.2)
    ' ─────────────────────────────────────────────────────────────
    Case "receiver"
        ReDim s(0)
        s(0) = Fld("RequiredFlowID","Required Flow input port",  FT_TEXT,   MX_BLUE,0,"Auto-shown when output required and >1 input can satisfy it")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' PUMP  [Pump_Properties.htm]
    ' Magenta group 1: PressureOut | PressureRise
    ' ─────────────────────────────────────────────────────────────
    Case "pump"
        ReDim s(1)
        s(0) = Fld("PressureOut",  "Discharge Pressure (kPa)",  FT_NUMBER, MX_MAGENTA,1,"Absolute discharge pressure.  e.g. 320")
        s(1) = Fld("PressureRise", "Pressure Rise (kPa)",       FT_NUMBER, MX_MAGENTA,1,"Rise above suction pressure")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' TURBINE  [Turbine_Properties.htm]
    ' Maroon group 1: TempOut | IsentropicEff
    ' Magenta group 2: DischargePressure | PressureDrop | PressureFeedback
    ' ─────────────────────────────────────────────────────────────
    Case "turbine"
        ReDim s(7)
        s(0) = Sec("Thermal — choose one or none (Maroon)")
        s(1) = Fld("TemperatureOut",   "Temperature Out (°C)",       FT_NUMBER, MX_MAROON, 1,"If set → solver calculates Isentropic Efficiency")
        s(2) = Fld("IsentropicEff",    "Isentropic Efficiency (%)",  FT_NUMBER, MX_MAROON, 1,"If set → solver calculates Temperature Out")
        s(3) = Sec("Pressure — choose exactly one (Magenta)")
        s(4) = Fld("DischargePressure","Discharge Pressure (kPa)",   FT_NUMBER, MX_MAGENTA,2,"")
        s(5) = Fld("PressureDrop",     "Pressure Drop (kPa)",        FT_NUMBER, MX_MAGENTA,2,"Allows pressure feedback to pass through")
        s(6) = Fld("PressureFeedback", "Pressure Feedback",          FT_CHECK,  MX_MAGENTA,2,"")
        s(7) = Sec("Power")
        Dim tb() As FieldSpec
        tb = Append(s, Fld("PowerOutput",    "Power Output (kW)",             FT_NUMBER, MX_BLUE,0,"Makes steam input required. 0=not specified."))
        tb = Append(tb, Fld("MechanicalEff", "Mechanical Efficiency (%)",     FT_NUMBER, MX_BLUE,0,""))
        tb = Append(tb, Fld("SteamConsump",  "Specific Steam Consumption",    FT_CALCONLY,MX_BLUE,0,"Calculated after balance — display only")) : tb(UBound(tb)).CalcOnly = True
        tb = Append(tb, Fld("GenMechPower",  "Generated Mechanical Power (kW)",FT_CALCONLY,MX_BLUE,0,"Calculated after balance — display only"))  : tb(UBound(tb)).CalcOnly = True
        BuildFieldSpecs = Merge(c, tb) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' THERMOCOMPRESSOR  [Thermocompressor_Properties.htm]
    ' Maroon group 1: PressureOut | PressureFeedback
    ' Magenta group 2: Efficiency | EntrainmentRatio | DischargeTemp
    ' ─────────────────────────────────────────────────────────────
    Case "thermocompressor"
        ReDim s(5)
        s(0) = Sec("Outlet Pressure — choose one or none (Maroon)")
        s(1) = Fld("PressureOut",      "Pressure Out (kPa)",          FT_NUMBER, MX_MAROON, 1,"")
        s(2) = Fld("PressureFeedback", "Pressure Feedback",           FT_CHECK,  MX_MAROON, 1,"")
        s(3) = Sec("Performance — choose exactly one (Magenta)")
        s(4) = Fld("Efficiency",       "Efficiency (%)",              FT_NUMBER, MX_MAGENTA,2,"Truffault formula with 5% nozzle wear allowance")
        s(5) = Fld("EntrainmentRatio", "Entrainment Ratio",           FT_NUMBER, MX_MAGENTA,2,"kg suction vapor / kg motive steam")
        Dim tc() As FieldSpec
        tc = Append(s, Fld("DischargeTemp", "Discharge Temperature (°C)", FT_NUMBER, MX_MAGENTA, 2,""))
        BuildFieldSpecs = Merge(c, tc) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' COMPRESSOR  [Compressor_Properties.htm]
    ' Magenta group 1: DischargePressure | PressureFeedback
    ' Vapor condensation NOT allowed.
    ' ─────────────────────────────────────────────────────────────
    Case "compressor"
        ReDim s(2)
        s(0) = Fld("DischargePressure","Discharge Pressure (kPa)",  FT_NUMBER, MX_MAGENTA,1,"0.0 = use pressure feedback if output goes to receiver")
        s(1) = Fld("PressureFeedback", "Pressure Feedback",         FT_CHECK,  MX_MAGENTA,1,"")
        s(2) = Fld("DischargeTemp",    "Discharge Temperature (°C)",FT_NUMBER, MX_BLUE,  0,"Vapor condensation is not allowed (solver enforces)")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' CONTACT CONDENSER  [Contact_Condenser_Properties.htm]
    ' Cold water (port 1) ALWAYS required (§9.1)
    ' Output always at atmospheric (§10.1)
    ' Magenta group 1: MinCWMode | TempOut | Approach
    ' Maroon group 2: CWQuantity | CWRatio
    ' ─────────────────────────────────────────────────────────────
    Case "contact_condenser"
        ReDim s(6)
        s(0) = Sec("NOTE: Cold water (port 1) is ALWAYS required (§9.1). Output at atmospheric (§10.1).")
        s(1) = Fld("InternalPressure","Internal Pressure (kPa)",    FT_NUMBER, MX_BLUE,  0,"For pressure feedback to upstream station")
        s(2) = Sec("Output Temperature — choose exactly one (Magenta)")
        s(3) = Fld("MinCWMode",       "Minimum Cooling Water Mode", FT_CHECK,  MX_MAGENTA,1,"Calculates minimum water to condense all vapor")
        s(4) = Fld("TemperatureOut",  "Temperature Out (°C)",       FT_NUMBER, MX_MAGENTA,1,"Combined output temperature")
        s(5) = Fld("Approach",        "Approach Temperature (°C)",  FT_NUMBER, MX_MAGENTA,1,"Vapor sat T minus water out T")
        s(6) = Sec("Cooling Water Override — choose one or none (Maroon)")
        Dim cc() As FieldSpec
        cc = Append(s, Fld("CWQuantity","Cooling Water Quantity (kg/h)", FT_NUMBER, MX_MAROON,2,""))
        cc = Append(cc, Fld("CWRatio",  "Cooling Water Ratio to Vapor",  FT_NUMBER, MX_MAROON,2,""))
        BuildFieldSpecs = Merge(c, cc) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' SURFACE CONDENSER  [Surface_Condenser_Properties.htm]
    ' Magenta group 1: TempOut | TempDrop
    ' Maroon group 2: HeatTransferCoef | Effectiveness
    ' Can be turned OFF by unchecking all fields (§14 Surface Condenser)
    ' ─────────────────────────────────────────────────────────────
    Case "surface_condenser"
        ReDim s(6)
        s(0) = Sec("Condensate Temperature — choose one or none (Magenta)")
        s(1) = Fld("TemperatureOut",  "Temperature Out (°C)",        FT_NUMBER, MX_MAGENTA,1,"Makes cooling water required")
        s(2) = Fld("TemperatureDrop", "Temperature Drop (°C)",       FT_NUMBER, MX_MAGENTA,1,"Drop from saturation T")
        s(3) = Fld("CWRequired",      "Cooling Flow Required",       FT_CHECK,  MX_BLUE,  0,"Default ON. Uncheck if cooling water quantity is known.")
        s(4) = Fld("InternalPressure","Internal Pressure (kPa)",     FT_NUMBER, MX_BLUE,  0,"For pressure feedback to upstream station")
        s(5) = Sec("Heat Transfer — choose one or none (Maroon)")
        s(6) = Fld("HeatTransferCoef","Heat Transfer Coefficient (W/m²·K)",FT_NUMBER,MX_MAROON,2,"")
        Dim sc() As FieldSpec
        sc = Append(s, Fld("Effectiveness",  "Effectiveness (%)",    FT_NUMBER, MX_MAROON,2,""))
        sc = Append(sc, Fld("HeatingSurface","Heating Surface (m²)", FT_NUMBER, MX_BLUE,  0,"Required with Coefficient"))
        sc = Append(sc, Fld("HeatLoss",      "Heat Loss (%)",        FT_NUMBER, MX_BLUE,  0,""))
        sc = Append(sc, Fld("FlowDirection", "Flow Direction",       FT_SELECT, MX_BLUE,  0,"Countercurrent,Parallel",""))
        BuildFieldSpecs = Merge(c, sc) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' PRESSURE REDUCER  [Pressure_Reducer_Properties.htm]
    ' Magenta group 1: PressureOut | PressureDrop
    ' ─────────────────────────────────────────────────────────────
    Case "pressure_reducer"
        ReDim s(1)
        s(0) = Fld("PressureOut",  "Pressure Out (kPa)",   FT_NUMBER, MX_MAGENTA,1,"")
        s(1) = Fld("PressureDrop", "Pressure Drop (kPa)",  FT_NUMBER, MX_MAGENTA,1,"Allows pressure feedback to pass through")
        BuildFieldSpecs = Merge(c, s) : Exit Function

    ' ─────────────────────────────────────────────────────────────
    ' TURBO ALTERNATOR  [Turbo_Alternator_Properties.htm]
    ' Maroon group 1: TempOut | IsentropicEff
    ' Magenta group 2: PressureOut | PressureDrop | PressureFeedback
    ' ─────────────────────────────────────────────────────────────
    Case "turbo_alternator"
        ReDim s(7)
        s(0) = Sec("Thermal — choose one or none (Maroon)")
        s(1) = Fld("TemperatureOut",   "Temperature Out (°C)",         FT_NUMBER, MX_MAROON, 1,"If set → solver calculates Isentropic Efficiency")
        s(2) = Fld("IsentropicEff",    "Isentropic Efficiency (%)",    FT_NUMBER, MX_MAROON, 1,"If set → solver calculates Temperature Out")
        s(3) = Sec("Pressure — choose exactly one (Magenta)")
        s(4) = Fld("PressureOut",      "Pressure Out (kPa)",           FT_NUMBER, MX_MAGENTA,2,"")
        s(5) = Fld("PressureDrop",     "Pressure Drop (kPa)",          FT_NUMBER, MX_MAGENTA,2,"")
        s(6) = Fld("PressureFeedback", "Pressure Feedback",            FT_CHECK,  MX_MAGENTA,2,"")
        s(7) = Sec("Electrical Power")
        Dim ta() As FieldSpec
        ta = Append(s, Fld("ElecPowerOutput","Electrical Power Output (kW)", FT_NUMBER, MX_BLUE,0,"Makes steam input required. 0=not specified."))
        ta = Append(ta, Fld("MechanicalEff", "Mechanical Efficiency (%)",    FT_NUMBER, MX_BLUE,0,""))
        ta = Append(ta, Fld("ElectricalEff", "Electrical Efficiency (%)",    FT_NUMBER, MX_BLUE,0,""))
        ta = Append(ta, Fld("SteamConsump",  "Specific Steam Consumption",   FT_CALCONLY,MX_BLUE,0,"Calculated after balance — display only"))  : ta(UBound(ta)).CalcOnly = True
        ta = Append(ta, Fld("GenElecPower",  "Generated Electrical Power (kW)",FT_CALCONLY,MX_BLUE,0,"Calculated after balance — display only")) : ta(UBound(ta)).CalcOnly = True
        BuildFieldSpecs = Merge(c, ta) : Exit Function

    ' ── Fallback ──────────────────────────────────────────────────
    Case Else
        BuildFieldSpecs = c
    End Select
End Function


'═══════════════════════════════════════════════════════════════════
' COMMON FIELDS — prepended to every station (§14 header)
' Station Name: required, max 20 chars
' Equipment ID: optional, max 11 chars (required for XML import/export)
'═══════════════════════════════════════════════════════════════════
Public Function CommonFields() As FieldSpec()
    Dim f(1) As FieldSpec
    f(0)          = Fld("StationName", "Station Name  (max 20 chars)", FT_TEXT, MX_BLUE, 0, "Required.")
    f(0).Required = True
    f(1)          = Fld("EquipmentID", "Equipment ID  (max 11 chars, optional)", FT_TEXT, MX_BLUE, 0, "Plant tag e.g. 1E-101A. Required for XML import/export.")
    CommonFields  = f
End Function


'═══════════════════════════════════════════════════════════════════
' FIELD CONSTRUCTORS
'═══════════════════════════════════════════════════════════════════

' Generic field constructor
Private Function Fld(key As String, lbl As String, _
                     ft As Integer, border As String, _
                     grpID As Integer, hint As String, _
                     Optional opts As String = "") As FieldSpec
    Dim f As FieldSpec
    f.PropKey   = key  : f.Label    = lbl
    f.FieldType = ft   : f.Border   = border
    f.GroupID   = grpID : f.Hint    = hint
    f.Options   = opts
    Fld = f
End Function

' Section separator (no input)
Private Function Sec(lbl As String) As FieldSpec
    Dim f As FieldSpec
    f.Label = lbl : f.FieldType = FT_SECTION
    Sec = f
End Function


'═══════════════════════════════════════════════════════════════════
' ARRAY HELPERS
'═══════════════════════════════════════════════════════════════════

Public Function Append(arr() As FieldSpec, f As FieldSpec) As FieldSpec()
    Dim n As Long : n = UBound(arr) + 1
    ReDim Preserve arr(n)
    arr(n) = f
    Append = arr
End Function

Public Function Merge(a() As FieldSpec, b() As FieldSpec) As FieldSpec()
    Dim na As Long : na = UBound(a) + 1
    Dim nb As Long : nb = UBound(b) + 1
    Dim r() As FieldSpec
    ReDim r(na + nb - 1)
    Dim i As Long
    For i = 0 To na - 1 : r(i)      = a(i) : Next i
    For i = 0 To nb - 1 : r(na + i) = b(i) : Next i
    Merge = r
End Function
