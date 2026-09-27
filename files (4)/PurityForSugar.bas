Attribute VB_Name = "PurityForSugar"
'
' ╔══════════════════════════════════════════════════════════════════╗
' ║  Purity for Sugar  —  PurityForSugar.bas                        ║
' ║  Phase 01  |  v1.0  |  Main VBA module                         ║
' ╚══════════════════════════════════════════════════════════════════╝
'
' All Public subs are callable from Developer tab → Macros.
'
' SOURCE RULES: RULES_v4.md
'   §2  Model building — step-by-step
'   §3  Colour scheme — RED / BLUE / YELLOW (inline RGB strings)
'   §4  Station numbering (1–9999, unique, lower = first)
'   §5  Flow streams (types, indicators, properties)
'   §6  15-component model
'   §9  Required flows
'   §10 Pressure rules
'   §14 Station Properties windows
'   §17 Model Properties window
'   §19 SUGARS Ribbon menu
'   §26 Solver architecture
'   §28 VBA rules (§28.4 no RGB in Const; §28.5 no UserForms)
'   §29 API contract (schema_version "1.0", HTTP 200 always)
'
' ──────────────────────────────────────────────────────────────────
Option Explicit

'═══════════════════════════════════════════════════════════════════
' CONSTANTS
'═══════════════════════════════════════════════════════════════════

' Engine (§29)
Private Const ENGINE_URL     As String = "http://localhost:8765"
Private Const SCHEMA_VERSION As String = "1.0"
Private Const PING_TIMEOUT   As Long   = 2000    ' ms
Private Const SOLVE_TIMEOUT  As Long   = 60000   ' ms

' Colour names used with SetShapeColour (actual RGB values in that Sub)
' §3: RED on drop, BLUE after number, YELLOW after Properties OK
' §28.4: RGB() must NOT appear in Const declarations — use inline in code


'═══════════════════════════════════════════════════════════════════
' §19 RIBBON ENTRY POINTS
' All mapped to Sugars ribbon items from RULES_v4 §19.
'═══════════════════════════════════════════════════════════════════

'── 1. Model Properties ──────────────────────────────────────────
Public Sub ShowModelProperties()
    Dim doc As Visio.Document : Set doc = ActiveDocument
    If doc Is Nothing Then MsgBox "No active document.", vbExclamation : Exit Sub
    OpenModelPropertiesDialog doc
End Sub

'── 2. Full Balance (main simulation) ────────────────────────────
Public Sub RunSimulation()
    Dim doc As Visio.Document : Set doc = ActiveDocument
    If doc Is Nothing Then MsgBox "No active document.", vbExclamation : Exit Sub

    If Not EngineIsRunning() Then
        MsgBox "The calculation engine is NOT running." & vbCrLf & vbCrLf & _
               "Start it first:" & vbCrLf & _
               "   purity_engine.exe" & vbCrLf & _
               "   — or —" & vbCrLf & _
               "   python server.py (Phase 03)", _
               vbExclamation, "Purity for Sugar"
        Exit Sub
    End If

    ' Validate and serialise
    Dim errMsg  As String
    Dim payload As String
    payload = SerializeGraph(doc, errMsg)
    If errMsg <> "" Then
        MsgBox "Cannot run — fix these errors first:" & vbCrLf & vbCrLf & errMsg, _
               vbCritical, "Purity for Sugar — Validation Errors"
        Exit Sub
    End If

    Application.StatusBar = "Purity for Sugar: running balance…"
    Dim resp As String
    resp = HttpPost(ENGINE_URL & "/solve", payload, SOLVE_TIMEOUT)
    Application.StatusBar = False

    If resp = "" Then
        MsgBox "No response from engine. Verify it is running on localhost:8765.", _
               vbExclamation, "Purity for Sugar"
        Exit Sub
    End If

    ' §29.3: HTTP 200 for ALL solver outcomes; status in JSON body
    Dim st As String : st = LCase(JsonGetStr(resp, "status"))
    Select Case st
    Case "converged"
        ApplyResultsToDocument doc, resp
        MsgBox "BALANCE CONVERGED" & vbCrLf & vbCrLf & _
               "Iterations:  " & JsonGetStr(resp, "iterations")  & vbCrLf & _
               "Final error: " & JsonGetStr(resp, "final_error") & vbCrLf & vbCrLf & _
               "Flow connectors are colour-coded by DS%." & vbCrLf & _
               "Double-click any flow line to see results.", _
               vbInformation, "Purity for Sugar"
    Case "diverged"
        MsgBox "Balance did NOT converge:" & vbCrLf & vbCrLf & _
               JsonGetStr(resp, "error_message"), _
               vbExclamation, "Purity for Sugar"
    Case "invalid"
        MsgBox "Model error prevented balance:" & vbCrLf & vbCrLf & _
               JsonGetStr(resp, "error_message"), _
               vbCritical, "Purity for Sugar"
    Case Else
        MsgBox "Unexpected engine response:" & vbCrLf & Left(resp, 500), _
               vbExclamation, "Purity for Sugar"
    End Select
End Sub

'── 3. Single Balance (one iteration — observe changes) ──────────
Public Sub RunSingleBalance()
    ' Runs exactly ONE iteration so the user can observe convergence.
    ' Maps to "Single" icon in §19.
    Dim doc As Visio.Document : Set doc = ActiveDocument
    If doc Is Nothing Then Exit Sub
    If Not EngineIsRunning() Then MsgBox "Engine not running.", vbExclamation : Exit Sub

    Dim errMsg As String
    Dim payload As String : payload = SerializeGraph(doc, errMsg)
    If errMsg <> "" Then MsgBox errMsg, vbCritical : Exit Sub

    ' Inject single-pass flag into JSON
    payload = Left(payload, Len(payload) - 1) & _
              "," & JStr("single_pass", "true") & "}"

    Application.StatusBar = "Purity for Sugar: single iteration…"
    Dim resp As String : resp = HttpPost(ENGINE_URL & "/solve", payload, SOLVE_TIMEOUT)
    Application.StatusBar = False

    If resp <> "" Then
        ApplyResultsToDocument doc, resp
        MsgBox "Single iteration complete." & vbCrLf & _
               "Status: " & JsonGetStr(resp, "status") & vbCrLf & _
               "Error:  " & JsonGetStr(resp, "final_error"), _
               vbInformation, "Purity for Sugar"
    End If
End Sub

'── 4. Show Results summary ───────────────────────────────────────
Public Sub ShowResults()
    Dim stored As String : stored = GetStoredResults(ActiveDocument)
    If stored = "" Then
        MsgBox "No results yet — run a balance first.", vbInformation, "Purity for Sugar"
        Exit Sub
    End If
    Dim st As String  : st   = JsonGetStr(stored, "status")
    Dim it As String  : it   = JsonGetStr(stored, "iterations")
    Dim fe As String  : fe   = JsonGetStr(stored, "final_error")
    MsgBox "Last balance result:" & vbCrLf & vbCrLf & _
           "Status:     " & UCase(st) & vbCrLf & _
           "Iterations: " & it        & vbCrLf & _
           "Final error:" & fe        & vbCrLf & vbCrLf & _
           "Double-click any flow connector to see its properties." & vbCrLf & _
           "Use Export to Excel for the full stream table.", _
           vbInformation, "Purity for Sugar — Last Results"
End Sub

'── 5. Summary report (all flow streams) ─────────────────────────
Public Sub ShowSummary()
    ' §19: Summary — "Provide a report listing every flow stream"
    Dim doc As Visio.Document : Set doc = ActiveDocument
    If doc Is Nothing Then Exit Sub

    Dim lines As String
    lines = "FLOW STREAM SUMMARY" & vbCrLf & _
            String(50, "=") & vbCrLf & vbCrLf

    Dim pg  As Visio.Page
    Dim shp As Visio.Shape
    Dim cnt As Long
    For Each pg In doc.Pages
        For Each shp In pg.Shapes
            If IsFlowConnector(shp) Then
                cnt = cnt + 1
                Dim ds As String  : ds   = GetProp(shp, "DS")
                Dim pur As String : pur  = GetProp(shp, "Purity")
                Dim t As String   : t    = GetProp(shp, "Temperature")
                Dim kg As String  : kg   = GetProp(shp, "WeightFlowRate")
                lines = lines & "Flow " & cnt & _
                        "   " & FmtN(kg, "0.0") & " kg/h" & _
                        "   DS=" & FmtN(ds, "0.00") & "%" & _
                        "   Pur=" & FmtN(pur, "0.0") & "%" & _
                        "   T=" & FmtN(t, "0.0") & Chr(176) & "C" & vbCrLf
            End If
        Next shp
    Next pg

    If cnt = 0 Then
        MsgBox "No flow connectors found. Build the flow diagram first.", _
               vbInformation, "Purity for Sugar"
    Else
        MsgBox lines, vbInformation, "Purity for Sugar — Summary"
    End If
End Sub

'── 6. Export to Excel ────────────────────────────────────────────
Public Sub ExportToExcel()
    Dim stored As String : stored = GetStoredResults(ActiveDocument)
    If stored = "" Then
        MsgBox "No results to export — run a balance first.", vbInformation
        Exit Sub
    End If
    Application.StatusBar = "Purity for Sugar: exporting…"
    Dim resp As String
    resp = HttpPost(ENGINE_URL & "/export/excel", stored, SOLVE_TIMEOUT)
    Application.StatusBar = False
    If resp = "" Then
        MsgBox "Export failed — engine not responding.", vbExclamation : Exit Sub
    End If
    Dim xlPath As String
    xlPath = Environ("TEMP") & "\purity_export_" & _
             Format(Now, "yyyymmdd_hhmmss") & ".xlsx"
    Dim bytes() As Byte : bytes = Base64Decode(resp)
    Dim fno As Integer  : fno   = FreeFile
    Open xlPath For Binary As #fno : Put #fno, , bytes : Close #fno
    Shell "explorer.exe """ & xlPath & """"
    MsgBox "Excel file saved to:" & vbCrLf & xlPath, vbInformation, "Purity for Sugar"
End Sub

'── 7. Net Process Revenues ───────────────────────────────────────
Public Sub ShowRevenues()
    ' §19: Revenues = sum(output flow values) − sum(external flow costs)
    MsgBox "Revenues calculation requires Phase 03 engine." & vbCrLf & vbCrLf & _
           "To prepare: double-click each external flow line and enter a" & vbCrLf & _
           "cost value; double-click each leaving flow and enter a value.", _
           vbInformation, "Purity for Sugar — Revenues"
End Sub

'── 8. Renumber Stations ──────────────────────────────────────────
Public Sub RenumberStations()
    ' §19: "Change the station number of one, or more, stations."
    Dim shp As Visio.Shape
    On Error Resume Next
    Set shp = ActivePage.Selection(1)
    On Error GoTo 0
    If shp Is Nothing Or Not IsStation(shp) Then
        MsgBox "Select one station shape first, then run this macro.", _
               vbInformation, "Renumber Station — Purity for Sugar"
        Exit Sub
    End If
    Dim old As String : old = GetProp(shp, "StationNumber")
    Dim nw  As String
    nw = InputBox("Enter new station number for " & _
                  TypeDisplayName(MasterNameToType(shp.Master.Name)) & _
                  " (currently " & old & "):", _
                  "Renumber Station — Purity for Sugar", old)
    If StrPtr(nw) = 0 Or Trim(nw) = old Then Exit Sub
    If Not IsNumeric(nw) Or CLng(nw) < 1 Or CLng(nw) > 9999 Then
        MsgBox "Invalid number.", vbExclamation : Exit Sub
    End If
    If IsStationNumberInUse(CLng(nw), shp) Then
        MsgBox "Number " & nw & " is already in use.", vbExclamation : Exit Sub
    End If
    SetProp shp, "StationNumber", Trim(nw)
    shp.Text = Trim(nw)
    MsgBox "Station renumbered from " & old & " to " & Trim(nw) & ".", _
           vbInformation, "Purity for Sugar"
End Sub

'── 9. Last Error / Warning ───────────────────────────────────────
Public Sub ShowLastError()
    ' §19: "Display error or warning messages from the last balance"
    Dim stored As String : stored = GetStoredResults(ActiveDocument)
    If stored = "" Then
        MsgBox "No balance has been run yet.", vbInformation, "Purity for Sugar"
        Exit Sub
    End If
    Dim errMsg As String : errMsg = JsonGetStr(stored, "error_message")
    If errMsg = "" Then errMsg = "(no errors or warnings)"
    MsgBox "Last balance error / warning:" & vbCrLf & vbCrLf & errMsg, _
           vbInformation, "Purity for Sugar — Last Error/Warning"
End Sub

'── 10. Check Engine Status ───────────────────────────────────────
Public Sub CheckEngineStatus()
    If EngineIsRunning() Then
        Dim r As String : r = HttpGet(ENGINE_URL & "/status")
        MsgBox "Engine is RUNNING" & vbCrLf & _
               "Version: " & JsonGetStr(r, "version") & vbCrLf & _
               "URL: " & ENGINE_URL, _
               vbInformation, "Purity for Sugar"
    Else
        MsgBox "Engine is NOT running." & vbCrLf & vbCrLf & _
               "Start with:  purity_engine.exe" & vbCrLf & _
               "Expected at: " & ENGINE_URL, _
               vbExclamation, "Purity for Sugar"
    End If
End Sub


'═══════════════════════════════════════════════════════════════════
' STATION PROPERTIES WINDOW
' Called by Document_ShapeDoubleClicked via ThisDocument.
' §3: Shape turns YELLOW only AFTER user clicks OK (saves data).
'═══════════════════════════════════════════════════════════════════
Public Sub OpenStationProperties(shp As Visio.Shape, stType As String)
    Dim sNum As String : sNum = GetProp(shp, "StationNumber")
    Dim ttl  As String : ttl  = TypeDisplayName(stType) & _
                                " — Station " & sNum & _
                                " — Purity for Sugar"

    ' ── Station Name (required, max 20 chars) ─────────────────────
    Dim sName As String : sName = GetProp(shp, "StationName")
    Do
        sName = InputBox("Station Name  (required, max 20 chars):", ttl, sName)
        If StrPtr(sName) = 0 Then Exit Sub     ' Cancel = do not save
        sName = Trim(sName)
        If sName <> "" Then Exit Do
        MsgBox "Station Name cannot be blank.", vbExclamation, ttl
    Loop
    If Len(sName) > 20 Then sName = Left(sName, 20)
    SetProp shp, "StationName", sName

    ' ── Equipment ID (optional, max 11 chars) ─────────────────────
    Dim eqID As String : eqID = GetProp(shp, "EquipmentID")
    eqID = InputBox("Equipment ID  (optional, max 11 chars)" & vbCrLf & _
                    "e.g. 1E-101A   — press OK to skip.", ttl, eqID)
    If StrPtr(eqID) <> 0 Then
        eqID = Trim(eqID)
        If Len(eqID) > 11 Then eqID = Left(eqID, 11)
        SetProp shp, "EquipmentID", eqID
    End If

    ' ── Type-specific fields ──────────────────────────────────────
    ShowTypeFields shp, stType, ttl

    ' ── Turn YELLOW — data has been entered (§3) ──────────────────
    ' "The station turns yellow to indicate that data for the station
    '  was entered after clicking on the OK button." — Program_Overview.htm
    SetShapeColour shp, "yellow"
End Sub


'═══════════════════════════════════════════════════════════════════
' TYPE-SPECIFIC FIELD INPUT SEQUENCES
' Each station type shows its key fields in order from §14.
' All entries are optional at this stage (can be blank).
' The solver does pre-solve validation of required fields.
'═══════════════════════════════════════════════════════════════════
Private Sub ShowTypeFields(shp As Visio.Shape, _
                            stType As String, ttl As String)
    Select Case stType

    Case "evaporator"
        Inf ttl, "Choose exactly one control mode (Magenta):" & vbCrLf & _
                 "  HTC, Vapor Pressure, Pressure Feedback, or Flow Out Temp" & vbCrLf & _
                 "Effect numbers must follow station number sequence (§16)." & vbCrLf & _
                 "Only ONE Total Solids entry per multiple-effect (§16)."
        Ask shp, "VaporPressure",      "Vapor Out Pressure (kPa)  [Magenta]:", ttl
        Ask shp, "FlowOutTemperature", "Flow Out Temperature (°C)  [Magenta — or leave blank]:", ttl
        Ask shp, "HeatLoss",           "Heat Loss (%)  e.g. 2.0:", ttl
        Ask shp, "CondensateDrop",     "Condensate Drop (K)  e.g. 4.0:", ttl
        Ask shp, "EffectNumber",       "Effect Number  (1 = first):", ttl
        Ask shp, "TotalSolids",        "Total Solids Out (%)  [one per multiple — leave blank if not specifying]:", ttl
        Ask shp, "EntrainmentLoss",    "Entrainment Sugar Loss (ppm)  e.g. 80:", ttl
        Ask shp, "ColorRise",          "Color Rise (% or CU):", ttl

    Case "pan"
        Inf ttl, "Pan steam (port 1) is ALWAYS a required flow (§9.1)." & vbCrLf & _
                 "Choose exactly one temperature control (Magenta)." & vbCrLf & _
                 "Choose one or none for massecuite DS (Maroon)."
        Ask shp, "VaporPressure",      "Vapor Out Pressure (kPa)  [Magenta]:", ttl
        Ask shp, "MassecuiteOutTemp",  "Massecuite Out Temperature (°C)  [Magenta — or blank]:", ttl
        Ask shp, "Supersaturation",    "Supersaturation Ss  e.g. 1.15:", ttl
        Ask shp, "TotalSolids",        "Total Solids / DS Out (%)  [Maroon — or blank]:", ttl
        Ask shp, "HeatLoss",           "Heat Loss (%)  Batch 8–12%, Continuous lower:", ttl
        Ask shp, "ColorRise",          "Color Rise (% or CU):", ttl
        Ask shp, "EntrainmentLoss",    "Entrainment Sugar Loss (ppm):", ttl

    Case "crystallizer"
        Ask shp, "Supersaturation",    "Supersaturation Ss  (required)  e.g. 1.10:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  — must be less than T in:", ttl
        Ask shp, "ColorRise",          "Color Rise (% or CU):", ttl

    Case "centrifugal"
        Inf ttl, "Centrifugal: TWO-STEP evaluation (§15)." & vbCrLf & vbCrLf & _
                 "STEP 1 — Enter actual massecuite sample data." & vbCrLf & _
                 "STEP 2 — Enter actual output data from the operating centrifugal." & vbCrLf & vbCrLf & _
                 "3 Magenta fields: Wash Flow, Green DS, Sugar DS." & vbCrLf & _
                 "Enter any TWO — the solver calculates the third."
        Ask shp, "MassecuiteDS",       "STEP 1 — Massecuite DS (%)  e.g. 93.00:", ttl
        Ask shp, "MassecuitePurity",   "Massecuite Purity (%)  e.g. 86.44:", ttl
        Ask shp, "MassecuiteTemp",     "Massecuite Temperature (°C)  e.g. 81.0:", ttl
        Ask shp, "MassecuiteSs",       "Massecuite Supersaturation Ss  e.g. 1.10:", ttl
        Ask shp, "MassecuiteFlow",     "Massecuite Flow (m³/h or t/h)  e.g. 25.0:", ttl
        Ask shp, "WashTemperature",    "STEP 2 — Wash Temperature (°C)  e.g. 98.0:", ttl
        Ask shp, "GreenDS",            "Green DS (%)  [Magenta]  e.g. 83.25:", ttl
        Ask shp, "GreenPurity",        "Green Purity (%)  e.g. 59.90:", ttl
        Ask shp, "SugarDS",            "Sugar DS (%)  [Magenta]  e.g. 98.50:", ttl
        Ask shp, "SugarPurity",        "Sugar Purity (%)  e.g. 94.50:", ttl

    Case "blender"
        Inf ttl, "Blend flow (port 1) is ALWAYS required (§9.1)." & vbCrLf & _
                 "Choose exactly one control method (Magenta)."
        Ask shp, "Ratio",              "Ratio (blend / primary)  [Magenta — or blank]  e.g. 0.3:", ttl
        Ask shp, "DSOut",              "DS Out (%)  [Magenta — or blank]:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Magenta — or blank]:", ttl

    Case "distributor"
        Inf ttl, "Overflow goes to the lowest-numbered unspecified port (§14)." & vbCrLf & _
                 "Cannot mix % mode and required flows."
        Ask shp, "Quantity0",          "Output Port 0 quantity  (kg/h or %):", ttl
        Ask shp, "Quantity1",          "Output Port 1 quantity:", ttl
        Ask shp, "Quantity2",          "Output Port 2 quantity:", ttl
        Ask shp, "Quantity3",          "Output Port 3 quantity:", ttl
        Ask shp, "Quantity4",          "Output Port 4 quantity:", ttl

    Case "heat_exchanger"
        Ask shp, "TemperatureOut",     "Temperature Out, Port 0 (°C)  [Magenta]:", ttl
        Ask shp, "Approach",           "Approach Temperature (°C)  [T1out−T0out; can be negative]:", ttl
        Ask shp, "HeatLoss",           "Heat Loss (%):", ttl
        Ask shp, "FlowDirection",      "Flow Direction  (Counter or Parallel):", ttl
        Ask shp, "HXType",             "Type  (Condensing or Non-Condensing):", ttl

    Case "injection_heater"
        Inf ttl, "Heating flow (port 1) is ALWAYS required (§9.1)."
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Magenta]:", ttl
        Ask shp, "TemperatureRise",    "Temperature Rise (K)  [Magenta — or blank if using T Out]:", ttl
        Ask shp, "HeatLoss",           "Heat Loss (%):", ttl

    Case "flash_tank"
        Inf ttl, "No crystal growth in Flash Tank (§11)." & vbCrLf & _
                 "Only vapor out OR liquid out can be required — not both."
        Ask shp, "VaporPressure",      "Vapor Out Pressure (kPa)  [Magenta]:", ttl
        Ask shp, "OutputFlowTemp",     "Output Flow Temperature (°C)  [Magenta — or blank]:", ttl
        Ask shp, "EntrainmentLoss",    "Entrainment Sugar Loss (ppm):", ttl

    Case "tank"
        Inf ttl, "Output always at atmospheric pressure (§10.1)." & vbCrLf & _
                 "Crystals dissolve to Ss=1; no growth (§11)."
        Ask shp, "HoldTDM",            "Hold TDM at (%)  [active when port 9 connected]  e.g. 67.00:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [active when port 10 connected]:", ttl
        Ask shp, "ColorRise",          "Color Rise (% or CU):", ttl
        Ask shp, "HeatingType",        "Heating Type  (Injection or Coil):", ttl

    Case "reactor"
        Inf ttl, "Can change solubility coefficients or colour WITHOUT any reaction. §14 Reactor."
        Ask shp, "InputComponent1",    "Input Component 1  e.g. CaO:", ttl
        Ask shp, "InputMole1",         "Input Mole % 1  e.g. 100:", ttl
        Ask shp, "OutputComponent1",   "Output Component 1  e.g. CaCO3:", ttl
        Ask shp, "OutputMole1",        "Output Mole % 1  e.g. 100:", ttl
        Ask shp, "ReactionEff",        "Reaction Efficiency (%)  e.g. 90:", ttl
        Ask shp, "HeatReaction",       "Heat of Reaction (kJ/kg)  +ve=exothermic:", ttl
        Ask shp, "ColorChange",        "Color Change (CU)  +ve or -ve. N.S.#1 only (§12.5):", ttl
        Ask shp, "SolCoefA",           "Solubility Coefficient a  (0=unchanged):", ttl
        Ask shp, "SolCoefB",           "Solubility Coefficient b:", ttl
        Ask shp, "SolCoefC",           "Solubility Coefficient c  (0=Wagnerowski):", ttl

    Case "separator_filter"
        Ask shp, "DiluentRatio",       "Diluent Ratio  [or 0 = No Ratio mode]  e.g. 0.200:", ttl
        Ask shp, "OutFlow1Pct",        "Out Flow No. 1 (% of diluent)  e.g. 30.0:", ttl
        Ask shp, "Component1Pct",      "Component 1 → Out 1 (%):", ttl
        Ask shp, "OtherCompPct",       "Other Components → Out 1 (%):", ttl
        Ask shp, "ColorPct",           "Color (%)  100=normal split; <100=more colour to Out 2:", ttl

    Case "dryer"
        Ask shp, "DryMatterOut",       "Output Dry Matter (%)  e.g. 99.98  (=100 minus moisture):", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C):", ttl
        Ask shp, "DryMatterLoss",      "Dry Matter Loss (ppm):", ttl
        Ask shp, "HeatLoss",           "Heat Loss (%):", ttl

    Case "cooler"
        Inf ttl, "No crystal growth — flow may become supersaturated (§11)."
        Ask shp, "TemperatureDrop",    "Temperature Drop (K)  [Magenta]:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Magenta — or blank]:", ttl

    Case "melter"
        Inf ttl, "Output at atmospheric. Crystals dissolve to Ss=1 (§10.1, §11)." & vbCrLf & _
                 "Heating flow (port 10) is always required when connected (§9.1)."
        Ask shp, "HoldTDM",            "Hold TDM at (%)  [active when port 9 connected]  e.g. 67.00:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [active when port 10 connected]:", ttl
        Ask shp, "ColorRise",          "Color Rise (% or CU):", ttl
        Ask shp, "HeatingType",        "Heating Type  (Injection or Coil):", ttl

    Case "receiver"
        Inf ttl, "Receiver: no input data needed unless the output is required." & vbCrLf & _
                 "Output pressure = MINIMUM of all input pressures (§10.2)." & vbCrLf & _
                 "No crystal growth or dissolution (§11)."

    Case "pump"
        Ask shp, "PressureOut",        "Discharge Pressure (kPa)  [Magenta]  e.g. 320:", ttl
        Ask shp, "PressureRise",       "Pressure Rise (kPa)  [Magenta — or blank]:", ttl

    Case "turbine"
        Ask shp, "DischargePressure",  "Discharge Pressure (kPa)  [Magenta]:", ttl
        Ask shp, "PressureDrop",       "Pressure Drop (kPa)  [Magenta — or blank]:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Maroon — or blank]:", ttl
        Ask shp, "IsentropicEff",      "Isentropic Efficiency (%)  [Maroon — or blank]:", ttl
        Ask shp, "PowerOutput",        "Power Output (kW)  [makes steam required; 0=not specified]:", ttl
        Ask shp, "MechanicalEff",      "Mechanical Efficiency (%):", ttl

    Case "thermocompressor"
        Ask shp, "Efficiency",         "Efficiency (%)  [Magenta — Truffault + 5% nozzle wear]:", ttl
        Ask shp, "PressureOut",        "Pressure Out (kPa)  [Maroon — or blank]:", ttl

    Case "compressor"
        Ask shp, "DischargePressure",  "Discharge Pressure (kPa)  [Magenta]  0=feedback from receiver:", ttl
        Ask shp, "DischargeTemp",      "Discharge Temperature (°C):", ttl

    Case "contact_condenser"
        Inf ttl, "Cold water (port 1) ALWAYS required. Output at atmospheric (§9.1, §10.1)."
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Magenta — combined output]:", ttl
        Ask shp, "Approach",           "Approach Temperature (°C)  [Magenta — or blank]:", ttl
        Ask shp, "InternalPressure",   "Internal Pressure (kPa)  [for pressure feedback — optional]:", ttl

    Case "surface_condenser"
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Magenta — or blank]:", ttl
        Ask shp, "TemperatureDrop",    "Temperature Drop (°C)  [Magenta — or blank]:", ttl
        Ask shp, "InternalPressure",   "Internal Pressure (kPa)  [for pressure feedback — optional]:", ttl

    Case "pressure_reducer"
        Ask shp, "PressureOut",        "Pressure Out (kPa)  [Magenta]:", ttl
        Ask shp, "PressureDrop",       "Pressure Drop (kPa)  [Magenta — or blank]:", ttl

    Case "turbo_alternator"
        Ask shp, "PressureOut",        "Pressure Out (kPa)  [Magenta]:", ttl
        Ask shp, "TemperatureOut",     "Temperature Out (°C)  [Maroon — or blank]:", ttl
        Ask shp, "IsentropicEff",      "Isentropic Efficiency (%)  [Maroon — or blank]:", ttl
        Ask shp, "ElecPowerOutput",    "Electrical Power Output (kW)  [makes steam required]:", ttl
        Ask shp, "MechanicalEff",      "Mechanical Efficiency (%):", ttl
        Ask shp, "ElectricalEff",      "Electrical Efficiency (%):", ttl

    End Select
End Sub

' Ask helper — single InputBox, saves non-empty values to Shape Data
Private Sub Ask(shp As Visio.Shape, propKey As String, _
                prompt As String, ttl As String)
    Dim cur As String : cur = GetProp(shp, propKey)
    Dim val As String : val = InputBox(prompt, ttl, cur)
    If StrPtr(val) = 0 Then Exit Sub   ' Cancel — leave unchanged
    val = Trim(val)
    If val <> "" Then SetProp shp, propKey, val
End Sub

' Inf helper — informational MsgBox (not a stop)
Private Sub Inf(ttl As String, msg As String)
    MsgBox msg, vbInformation, ttl
End Sub


'═══════════════════════════════════════════════════════════════════
' FLOW PROPERTIES WINDOW
' Called by Document_ShapeDoubleClicked for 1D connector shapes.
' §5, §7, §8
'═══════════════════════════════════════════════════════════════════
Public Sub ShowFlowProperties(shp As Visio.Shape)
    Dim fromNum  As String : fromNum  = GetProp(shp, "StationFromNumber")
    Dim toNum    As String : toNum    = GetProp(shp, "StationToNumber")
    Dim flowRate As String : flowRate = GetProp(shp, "WeightFlowRate")
    Dim temp     As String : temp     = GetProp(shp, "Temperature")
    Dim pres     As String : pres     = GetProp(shp, "Pressure")
    Dim tdm      As String : tdm      = GetProp(shp, "TDM")
    Dim sugar    As String : sugar    = GetProp(shp, "Sugar")
    Dim ds       As String : ds       = GetProp(shp, "DS")
    Dim pur      As String : pur      = GetProp(shp, "Purity")
    Dim cryst    As String : cryst    = GetProp(shp, "Crystals")
    Dim isns     As String : isns     = GetProp(shp, "ISNS")
    Dim gas      As String : gas      = GetProp(shp, "Gas")
    Dim col      As String : col      = GetProp(shp, "Color")
    Dim ftype    As String : ftype    = GetProp(shp, "FluidType")

    Dim isExt As Boolean
    isExt = (fromNum = "" Or fromNum = "0")
    Dim kind As String
    kind = IIf(isExt, "EXTERNAL FLOW  (user-specified)", _
                      "INTERNAL FLOW  (calculated by solver)")

    Dim m As String
    m = String(46, "=") & vbCrLf & "  " & kind & vbCrLf & _
        String(46, "=") & vbCrLf & vbCrLf

    If Not isExt Then
        m = m & "  From station:  " & fromNum & vbCrLf
        m = m & "  To station:    " & toNum   & vbCrLf & vbCrLf
    End If

    m = m & "  Flow rate:   " & FmtN(flowRate, "0.0")   & " kg/h"  & vbCrLf
    m = m & "  Temperature: " & FmtN(temp,     "0.0")   & " "      & Chr(176) & "C" & vbCrLf
    m = m & "  Pressure:    " & FmtN(pres,     "0.0")   & " kPa"   & vbCrLf & vbCrLf
    m = m & "  TDM:     " & FmtN(tdm,   "0.00") & "%  " & _
            "  Sugar:  " & FmtN(sugar,  "0.00") & "%" & vbCrLf
    m = m & "  DS:      " & FmtN(ds,    "0.00") & "%  " & _
            "  Purity: " & FmtN(pur,    "0.0")  & "%" & vbCrLf
    m = m & "  Crystals:" & FmtN(cryst, "0.00") & "%  " & _
            "  ISNS:   " & FmtN(isns,   "0.00") & "%" & vbCrLf
    m = m & "  Gas:     " & FmtN(gas,   "0.00") & "%" & vbCrLf & vbCrLf
    m = m & "  Color:     " & FmtN(col, "0")    & " ICU" & vbCrLf
    m = m & "  Fluid type: " & IIf(ftype = "", "(not yet calculated)", ftype) & vbCrLf

    MsgBox m, vbInformation, "Flow Stream Properties — Purity for Sugar"
End Sub


'═══════════════════════════════════════════════════════════════════
' MODEL PROPERTIES DIALOG (§17)
'═══════════════════════════════════════════════════════════════════
Private Sub OpenModelPropertiesDialog(doc As Visio.Document)
    Dim mp  As Visio.Shape : Set mp = FindModelPropsShape(doc)
    Dim ttl As String      : ttl = "Model Properties — Purity for Sugar"

    Dim units As String
    units = MProp(mp, "Units", "SI")
    units = InputBox("Units  (SI  or  Imperial):", ttl, units)
    If StrPtr(units) = 0 Then Exit Sub
    If Trim(units) = "" Then units = "SI"

    Dim sugar As String
    sugar = MProp(mp, "SugarType", "cane")
    sugar = InputBox("Sugar Type  (cane  or  beet):", ttl, sugar)
    If StrPtr(sugar) = 0 Then Exit Sub
    If Trim(sugar) = "" Then sugar = "cane"

    Dim tol As String
    tol = MProp(mp, "Tolerance", "0.0001")
    tol = InputBox("Convergence Tolerance  e.g. 0.0001  (= 0.01%):", ttl, tol)
    If StrPtr(tol) = 0 Then Exit Sub
    If Not IsNumeric(tol) Or CDbl(tol) <= 0 Then tol = "0.0001"

    Dim mxi As String
    mxi = MProp(mp, "MaxIter", "150")
    mxi = InputBox("Maximum Iterations:", ttl, mxi)
    If StrPtr(mxi) = 0 Then Exit Sub
    If Not IsNumeric(mxi) Or CLng(mxi) < 1 Then mxi = "150"

    Dim atm As String
    atm = MProp(mp, "AtmPressure", "101.325")
    atm = InputBox("Atmospheric Pressure (kPa):", ttl, atm)
    If StrPtr(atm) = 0 Then Exit Sub
    If Not IsNumeric(atm) Or CDbl(atm) <= 0 Then atm = "101.325"

    Dim sol As String
    sol = MProp(mp, "SolMode", "vavrinecz")
    sol = InputBox("Solubility Mode  (vavrinecz  or  wagnerowski):", ttl, sol)
    If StrPtr(sol) = 0 Then Exit Sub
    If Trim(sol) = "" Then sol = "vavrinecz"

    If mp Is Nothing Then Set mp = CreateModelPropsShape(doc)
    SetProp mp, "Units",       Trim(units)
    SetProp mp, "SugarType",   Trim(sugar)
    SetProp mp, "Tolerance",   Trim(tol)
    SetProp mp, "MaxIter",     Trim(mxi)
    SetProp mp, "AtmPressure", Trim(atm)
    SetProp mp, "SolMode",     Trim(sol)

    MsgBox "Model Properties saved." & vbCrLf & vbCrLf & _
           "Type:       " & Trim(sugar) & vbCrLf & _
           "Units:      " & Trim(units) & vbCrLf & _
           "Tolerance:  " & Trim(tol)   & " (" & _
           Format(CDbl(Trim(tol)) * 100, "0.00##") & "%)" & vbCrLf & _
           "Max iter:   " & Trim(mxi)   & vbCrLf & _
           "Atm press:  " & Trim(atm)   & " kPa", _
           vbInformation, ttl
End Sub

Private Function MProp(mp As Visio.Shape, key As String, _
                        def As String) As String
    If mp Is Nothing Then MProp = def : Exit Function
    Dim v As String : v = GetProp(mp, key)
    MProp = IIf(v = "", def, v)
End Function


'═══════════════════════════════════════════════════════════════════
' GRAPH SERIALIZATION → JSON  (§29.2)
' Iterates all pages, collects stations and flow connectors,
' validates, and serialises to the schema_version "1.0" JSON format.
'═══════════════════════════════════════════════════════════════════
Public Function SerializeGraph(doc As Visio.Document, _
                                ByRef errMsg As String) As String
    Dim pg   As Visio.Page
    Dim shp  As Visio.Shape

    Dim stJSON   As String  ' accumulates station JSON objects
    Dim flJSON   As String  ' accumulates flow JSON objects
    Dim errors   As String  ' validation error lines
    Dim stCount  As Long
    Dim flCount  As Long

    ' Duplicate station number detector — use a Collection (not array)
    ' to avoid large stack allocation.
    Dim usedNums As New Collection
    Dim dupKey   As String

    ' Read model properties (§17)
    Dim mp     As Visio.Shape : Set mp = FindModelPropsShape(doc)
    Dim mpU    As String : mpU  = MProp(mp, "Units",       "SI")
    Dim mpSug  As String : mpSug = MProp(mp, "SugarType",  "cane")
    Dim mpTol  As String : mpTol = MProp(mp, "Tolerance",  "0.0001")
    Dim mpIter As String : mpIter = MProp(mp, "MaxIter",   "150")
    Dim mpAtm  As String : mpAtm  = MProp(mp, "AtmPressure","101.325")
    Dim mpSol  As String : mpSol  = MProp(mp, "SolMode",   "vavrinecz")

    For Each pg In doc.Pages
        For Each shp In pg.Shapes

            ' ── Station shape ──────────────────────────────────────
            If IsStation(shp) Then
                Dim sn As String : sn = GetProp(shp, "StationNumber")
                Dim nm As String : nm = GetProp(shp, "StationName")

                ' Validate
                If sn = "" Or Not IsNumeric(sn) Then
                    errors = errors & Chr(149) & " Shape on page '" & pg.Name & _
                             "' (" & shp.Master.Name & ") has no station number." & vbCrLf
                ElseIf CLng(sn) < 1 Or CLng(sn) > 9999 Then
                    errors = errors & Chr(149) & " Station number " & sn & _
                             " is out of range 1–9999." & vbCrLf
                Else
                    dupKey = "N" & CStr(CLng(sn))
                    On Error Resume Next
                    usedNums.Add sn, dupKey
                    If Err.Number <> 0 Then
                        errors = errors & Chr(149) & " Station number " & sn & _
                                 " is duplicated (§4)." & vbCrLf
                    End If
                    On Error GoTo 0
                End If

                If Trim(nm) = "" Then
                    errors = errors & Chr(149) & " Station " & sn & _
                             " has no Station Name (§14)." & vbCrLf
                End If

                ' Serialise
                Dim st As String : st = MasterNameToType(shp.Master.Name)
                Dim pr As String : pr = CollectStationProps(shp, st)

                Dim sObj As String
                sObj = "{" & _
                    JStr("id",             CStr(shp.ID))         & "," & _
                    JStr("page",           pg.Name)              & "," & _
                    JNum("station_number", sn)                   & "," & _
                    JStr("type",           st)                   & "," & _
                    JStr("name",           nm)                   & "," & _
                    JStr("equipment_id",   GetProp(shp,"EquipmentID")) & "," & _
                    JStr("master_name",    shp.Master.Name)      & "," & _
                    """properties"":{" & pr & "}" & _
                    "}"

                If stCount > 0 Then stJSON = stJSON & ","
                stJSON = stJSON & sObj
                stCount = stCount + 1

            ' ── Flow connector ─────────────────────────────────────
            ElseIf IsFlowConnector(shp) Then
                Dim fromID As String : fromID = ""
                Dim toID   As String : toID   = ""
                Dim ci     As Integer
                For ci = 1 To shp.Connects.Count
                    Dim cn As Visio.Connect : Set cn = shp.Connects(ci)
                    If cn.FromSheet.ID = shp.ID Then
                        If cn.ToSheet.Type = visTypeShape Then
                            On Error Resume Next
                            Dim cname As String
                            cname = LCase(cn.FromCell.LocalName)
                            On Error GoTo 0
                            If InStr(cname, "begin") > 0 Then
                                fromID = CStr(cn.ToSheet.ID)
                            ElseIf InStr(cname, "end") > 0 Then
                                toID = CStr(cn.ToSheet.ID)
                            End If
                        End If
                    End If
                Next ci

                Dim isExt As Boolean : isExt = (fromID = "")

                ' Build initial_state block in two parts (VBA max 24 continuations per statement)
                Dim fsA As String
                fsA = JNumN("mass_flow_kgh",    GetProp(shp,"WeightFlowRate"))  & "," & _
                      JNumN("temperature_c",    GetProp(shp,"Temperature"))     & "," & _
                      JNumN("pressure_kpa",     GetProp(shp,"Pressure"))        & "," & _
                      JNumN("ds_pct",           GetProp(shp,"DS"))              & "," & _
                      JNumN("purity_pct",       GetProp(shp,"Purity"))          & "," & _
                      JNumN("crystal_pct",      GetProp(shp,"Crystals"))        & "," & _
                      JNumN("isns_pct",         GetProp(shp,"ISNS"))            & "," & _
                      JNumN("gas_pct",          GetProp(shp,"Gas"))             & "," & _
                      JNumN("water",            GetProp(shp,"Water"))           & "," & _
                      JNumN("dissolved_sucrose",GetProp(shp,"DissolvedSucrose")) & "," & _
                      JNumN("non_sucrose_1",    GetProp(shp,"NonSucrose1"))     & "," & _
                      JNumN("non_sucrose_2",    GetProp(shp,"NonSucrose2"))

                Dim fsB As String
                fsB = JNumN("sucrose_crystals", GetProp(shp,"SucrosecrystALS")) & "," & _
                      JNumN("fiber_isns",       GetProp(shp,"Fiber"))           & "," & _
                      JNumN("cao",              GetProp(shp,"CaO"))             & "," & _
                      JNumN("caco3",            GetProp(shp,"CaCO3"))           & "," & _
                      JNumN("water_vapor",      GetProp(shp,"WaterVapor"))      & "," & _
                      JNumN("co2",              GetProp(shp,"CO2"))             & "," & _
                      JNumN("nh3",              GetProp(shp,"NH3"))             & "," & _
                      JNumN("color_icu",        GetProp(shp,"Color"))           & "," & _
                      JNumN("sol_coef_a",       GetProp(shp,"SolCoefA"))        & "," & _
                      JNumN("sol_coef_b",       GetProp(shp,"SolCoefB"))        & "," & _
                      JNumN("sol_coef_c",       GetProp(shp,"SolCoefC"))

                Dim fObj As String
                fObj = "{" & _
                    JStr("id",              CStr(shp.ID))      & "," & _
                    JNullOrNum("origin_station", fromID)       & "," & _
                    JNullOrNum("dest_station",   toID)         & "," & _
                    JBool("is_external",    isExt)             & "," & _
                    JBool("is_required",    False)             & "," & _
                    """initial_state"":{" & fsA & "," & fsB & "}" & _
                    "}"

                If flCount > 0 Then flJSON = flJSON & ","
                flJSON = flJSON & fObj
                flCount = flCount + 1
            End If

        Next shp
    Next pg

    ' Return errors and abort if any
    errMsg = errors
    If errors <> "" Then SerializeGraph = "" : Exit Function

    If stCount = 0 Then
        errMsg = "No Purity for Sugar station shapes found on any page." & vbCrLf & _
                 "Open a Sugars stencil (Sug_*.vss) and drag shapes onto the diagram."
        SerializeGraph = "" : Exit Function
    End If

    ' Build final JSON (§29.2)
    SerializeGraph = "{" & _
        JStr("schema_version",           SCHEMA_VERSION) & "," & _
        JStr("model_id",                 CStr(CDbl(Now))) & "," & _
        JStr("model_name",               doc.Name)        & "," & _
        JStr("units",                    mpU)             & "," & _
        JStr("sugar_type",               mpSug)           & "," & _
        """convergence_tolerance"":" & mpTol              & "," & _
        """max_iterations"":"        & mpIter             & "," & _
        """atmospheric_pressure_kpa"":" & mpAtm           & "," & _
        JStr("solubility_mode",          mpSol)           & "," & _
        """stations"":[" & stJSON & "]"                   & "," & _
        """flows"":[" & flJSON & "]"                      & _
        "}"
End Function


'═══════════════════════════════════════════════════════════════════
' COLLECT STATION PROPS FOR JSON
' Maps Shape Data keys to JSON field names for the engine.
'═══════════════════════════════════════════════════════════════════
Private Function CollectStationProps(shp As Visio.Shape, _
                                      stType As String) As String
    Dim r As String

    r = AddPS(r, "station_number", GetProp(shp, "StationNumber"))
    r = AddPS(r, "name",           GetProp(shp, "StationName"))
    r = AddPS(r, "equipment_id",   GetProp(shp, "EquipmentID"))

    Select Case stType

    Case "evaporator"
        r = AddPN(r,"vapor_pressure_kpa",   GetProp(shp,"VaporPressure"))
        r = AddPN(r,"sat_temperature_c",    GetProp(shp,"SatTemperature"))
        r = AddPN(r,"flow_out_temp_c",      GetProp(shp,"FlowOutTemperature"))
        r = AddPN(r,"heat_transfer_coef",   GetProp(shp,"HeatTransferCoef"))
        r = AddPN(r,"heating_surface_m2",   GetProp(shp,"HeatingSurface"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))
        r = AddPN(r,"condensate_drop_k",    GetProp(shp,"CondensateDrop"))
        r = AddPN(r,"effect_number",        GetProp(shp,"EffectNumber"))
        r = AddPN(r,"total_solids_pct",     GetProp(shp,"TotalSolids"))
        r = AddPN(r,"entrainment_ppm",      GetProp(shp,"EntrainmentLoss"))
        r = AddPN(r,"bpe_factor",           GetProp(shp,"BPEFactor"))
        r = AddPN(r,"color_rise",           GetProp(shp,"ColorRise"))
        r = AddPB(r,"pressure_feedback",    GetProp(shp,"PressureFeedback"))

    Case "pan"
        r = AddPN(r,"vapor_pressure_kpa",   GetProp(shp,"VaporPressure"))
        r = AddPN(r,"sat_temperature_c",    GetProp(shp,"SatTemperature"))
        r = AddPN(r,"massecuite_out_temp_c",GetProp(shp,"MassecuiteOutTemp"))
        r = AddPN(r,"supersaturation",      GetProp(shp,"Supersaturation"))
        r = AddPN(r,"total_solids_pct",     GetProp(shp,"TotalSolids"))
        r = AddPN(r,"target_ml_purity_pct", GetProp(shp,"TargetMLPurity"))
        r = AddPN(r,"ds_high_limit_pct",    GetProp(shp,"DSHighLimit"))
        r = AddPN(r,"ds_low_limit_pct",     GetProp(shp,"DSLowLimit"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))
        r = AddPN(r,"condensate_drop_k",    GetProp(shp,"CondensateDrop"))
        r = AddPN(r,"color_rise",           GetProp(shp,"ColorRise"))
        r = AddPN(r,"entrainment_ppm",      GetProp(shp,"EntrainmentLoss"))
        r = AddPN(r,"sol_coef_a",           GetProp(shp,"SolCoefA"))
        r = AddPN(r,"sol_coef_b",           GetProp(shp,"SolCoefB"))
        r = AddPN(r,"sol_coef_c",           GetProp(shp,"SolCoefC"))
        r = AddPB(r,"pressure_feedback",    GetProp(shp,"PressureFeedback"))

    Case "crystallizer"
        r = AddPN(r,"supersaturation",      GetProp(shp,"Supersaturation"))
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"color_rise",           GetProp(shp,"ColorRise"))
        r = AddPN(r,"sol_coef_a",           GetProp(shp,"SolCoefA"))
        r = AddPN(r,"sol_coef_b",           GetProp(shp,"SolCoefB"))
        r = AddPN(r,"sol_coef_c",           GetProp(shp,"SolCoefC"))

    Case "centrifugal"
        r = AddPS(r,"centrifugal_type",     GetProp(shp,"CentrifugalType"))
        r = AddPN(r,"massecuite_ds_pct",    GetProp(shp,"MassecuiteDS"))
        r = AddPN(r,"massecuite_purity_pct",GetProp(shp,"MassecuitePurity"))
        r = AddPN(r,"massecuite_temp_c",    GetProp(shp,"MassecuiteTemp"))
        r = AddPN(r,"massecuite_ss",        GetProp(shp,"MassecuiteSs"))
        r = AddPN(r,"massecuite_flow",      GetProp(shp,"MassecuiteFlow"))
        r = AddPN(r,"wash_flow",            GetProp(shp,"WashFlow"))
        r = AddPN(r,"wash_temp_c",          GetProp(shp,"WashTemperature"))
        r = AddPN(r,"wash_quality_pct",     GetProp(shp,"WashQuality"))
        r = AddPN(r,"green_ds_pct",         GetProp(shp,"GreenDS"))
        r = AddPN(r,"green_purity_pct",     GetProp(shp,"GreenPurity"))
        r = AddPN(r,"green_temp_c",         GetProp(shp,"GreenTemperature"))
        r = AddPN(r,"sugar_ds_pct",         GetProp(shp,"SugarDS"))
        r = AddPN(r,"sugar_purity_pct",     GetProp(shp,"SugarPurity"))
        r = AddPN(r,"sugar_temp_c",         GetProp(shp,"SugarTemperature"))
        r = AddPB(r,"use_residual_data",    GetProp(shp,"UseResidualData"))

    Case "blender"
        r = AddPN(r,"ratio",                GetProp(shp,"Ratio"))
        r = AddPS(r,"ratio_component",      GetProp(shp,"RatioComponent"))
        r = AddPN(r,"blend_quantity_kgh",   GetProp(shp,"BlendQuantity"))
        r = AddPN(r,"nsw_out",              GetProp(shp,"NSWOut"))
        r = AddPN(r,"quantity_out_kgh",     GetProp(shp,"QuantityOut"))
        r = AddPN(r,"ds_out_pct",           GetProp(shp,"DSOut"))
        r = AddPN(r,"purity_out_pct",       GetProp(shp,"PurityOut"))
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))

    Case "distributor"
        r = AddPN(r,"quantity_0",GetProp(shp,"Quantity0"))
        r = AddPN(r,"quantity_1",GetProp(shp,"Quantity1"))
        r = AddPN(r,"quantity_2",GetProp(shp,"Quantity2"))
        r = AddPN(r,"quantity_3",GetProp(shp,"Quantity3"))
        r = AddPN(r,"quantity_4",GetProp(shp,"Quantity4"))
        r = AddPN(r,"quantity_5",GetProp(shp,"Quantity5"))
        r = AddPN(r,"quantity_6",GetProp(shp,"Quantity6"))
        r = AddPN(r,"quantity_7",GetProp(shp,"Quantity7"))
        r = AddPB(r,"use_percent",GetProp(shp,"UseQuantityPCT"))

    Case "heat_exchanger"
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"temperature_rise_k",   GetProp(shp,"TemperatureRise"))
        r = AddPN(r,"approach_c",           GetProp(shp,"Approach"))
        r = AddPN(r,"temp_out_port1_c",     GetProp(shp,"TempOutPort1"))
        r = AddPN(r,"heat_transfer_coef",   GetProp(shp,"HeatTransferCoef"))
        r = AddPN(r,"effectiveness_pct",    GetProp(shp,"Effectiveness"))
        r = AddPN(r,"heating_surface_m2",   GetProp(shp,"HeatingSurface"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))
        r = AddPN(r,"condensate_drop_k",    GetProp(shp,"CondensateDrop"))
        r = AddPS(r,"flow_direction",       GetProp(shp,"FlowDirection"))
        r = AddPS(r,"hx_type",              GetProp(shp,"HXType"))
        r = AddPB(r,"port1_required",       GetProp(shp,"Port1Required"))

    Case "injection_heater"
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"temperature_rise_k",   GetProp(shp,"TemperatureRise"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))

    Case "flash_tank"
        r = AddPN(r,"vapor_pressure_kpa",   GetProp(shp,"VaporPressure"))
        r = AddPN(r,"sat_temperature_c",    GetProp(shp,"SatTemperature"))
        r = AddPN(r,"output_flow_temp_c",   GetProp(shp,"OutputFlowTemp"))
        r = AddPN(r,"entrainment_ppm",      GetProp(shp,"EntrainmentLoss"))
        r = AddPB(r,"pressure_feedback",    GetProp(shp,"PressureFeedback"))

    Case "tank"
        r = AddPN(r,"flow_to_storage_m3h",  GetProp(shp,"FlowToStorage"))
        r = AddPN(r,"flow_from_storage_m3h",GetProp(shp,"FlowFromStorage"))
        r = AddPN(r,"hold_tdm_pct",         GetProp(shp,"HoldTDM"))
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"color_rise",           GetProp(shp,"ColorRise"))
        r = AddPS(r,"heating_type",         GetProp(shp,"HeatingType"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))

    Case "reactor"
        r = AddPS(r,"input_component_1",    GetProp(shp,"InputComponent1"))
        r = AddPN(r,"input_mole_pct_1",     GetProp(shp,"InputMole1"))
        r = AddPS(r,"output_component_1",   GetProp(shp,"OutputComponent1"))
        r = AddPN(r,"output_mole_pct_1",    GetProp(shp,"OutputMole1"))
        r = AddPN(r,"reaction_eff_pct",     GetProp(shp,"ReactionEff"))
        r = AddPN(r,"heat_reaction_kjkg",   GetProp(shp,"HeatReaction"))
        r = AddPN(r,"color_change_cu",      GetProp(shp,"ColorChange"))
        r = AddPN(r,"sol_coef_a",           GetProp(shp,"SolCoefA"))
        r = AddPN(r,"sol_coef_b",           GetProp(shp,"SolCoefB"))
        r = AddPN(r,"sol_coef_c",           GetProp(shp,"SolCoefC"))

    Case "separator_filter"
        r = AddPN(r,"diluent_ratio",        GetProp(shp,"DiluentRatio"))
        r = AddPS(r,"diluent_component",    GetProp(shp,"DiluentComponent"))
        r = AddPN(r,"out_flow_1_pct",       GetProp(shp,"OutFlow1Pct"))
        r = AddPN(r,"component_1_pct",      GetProp(shp,"Component1Pct"))
        r = AddPN(r,"component_2_pct",      GetProp(shp,"Component2Pct"))
        r = AddPN(r,"component_3_pct",      GetProp(shp,"Component3Pct"))
        r = AddPN(r,"component_4_pct",      GetProp(shp,"Component4Pct"))
        r = AddPN(r,"other_comp_pct",       GetProp(shp,"OtherCompPct"))
        r = AddPN(r,"color_pct",            GetProp(shp,"ColorPct"))
        r = AddPB(r,"no_ratio",             GetProp(shp,"NoRatio"))

    Case "dryer"
        r = AddPN(r,"dry_matter_out_pct",   GetProp(shp,"DryMatterOut"))
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"dry_matter_loss_ppm",  GetProp(shp,"DryMatterLoss"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))
        r = AddPN(r,"cond_heat_eff_pct",    GetProp(shp,"CondHeatEff"))

    Case "cooler"
        r = AddPN(r,"temperature_drop_k",  GetProp(shp,"TemperatureDrop"))
        r = AddPN(r,"temperature_out_c",   GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"heat_loss_pct",       GetProp(shp,"HeatLossPct"))
        r = AddPN(r,"heat_loss_kjkg",      GetProp(shp,"HeatLossKJKG"))

    Case "melter"
        r = AddPN(r,"hold_tdm_pct",        GetProp(shp,"HoldTDM"))
        r = AddPN(r,"temperature_out_c",   GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"color_rise",          GetProp(shp,"ColorRise"))
        r = AddPS(r,"heating_type",        GetProp(shp,"HeatingType"))
        r = AddPN(r,"heat_loss_pct",       GetProp(shp,"HeatLoss"))

    Case "pump"
        r = AddPN(r,"discharge_pressure_kpa",GetProp(shp,"PressureOut"))
        r = AddPN(r,"pressure_rise_kpa",     GetProp(shp,"PressureRise"))

    Case "turbine"
        r = AddPN(r,"discharge_pressure_kpa",GetProp(shp,"DischargePressure"))
        r = AddPN(r,"pressure_drop_kpa",     GetProp(shp,"PressureDrop"))
        r = AddPN(r,"temperature_out_c",     GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"isentropic_eff_pct",    GetProp(shp,"IsentropicEff"))
        r = AddPN(r,"power_output_kw",       GetProp(shp,"PowerOutput"))
        r = AddPN(r,"mechanical_eff_pct",    GetProp(shp,"MechanicalEff"))
        r = AddPB(r,"pressure_feedback",     GetProp(shp,"PressureFeedback"))

    Case "thermocompressor"
        r = AddPN(r,"pressure_out_kpa",     GetProp(shp,"PressureOut"))
        r = AddPN(r,"efficiency_pct",       GetProp(shp,"Efficiency"))
        r = AddPN(r,"entrainment_ratio",    GetProp(shp,"EntrainmentRatio"))
        r = AddPN(r,"discharge_temp_c",     GetProp(shp,"DischargeTemp"))
        r = AddPB(r,"pressure_feedback",    GetProp(shp,"PressureFeedback"))

    Case "compressor"
        r = AddPN(r,"discharge_pressure_kpa",GetProp(shp,"DischargePressure"))
        r = AddPN(r,"discharge_temp_c",      GetProp(shp,"DischargeTemp"))
        r = AddPB(r,"pressure_feedback",     GetProp(shp,"PressureFeedback"))

    Case "contact_condenser"
        r = AddPN(r,"internal_pressure_kpa",GetProp(shp,"InternalPressure"))
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"approach_c",           GetProp(shp,"Approach"))
        r = AddPN(r,"cw_quantity_kgh",      GetProp(shp,"CWQuantity"))
        r = AddPN(r,"cw_ratio",             GetProp(shp,"CWRatio"))
        r = AddPB(r,"min_cw_mode",          GetProp(shp,"MinCWMode"))

    Case "surface_condenser"
        r = AddPN(r,"temperature_out_c",    GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"temperature_drop_c",   GetProp(shp,"TemperatureDrop"))
        r = AddPN(r,"internal_pressure_kpa",GetProp(shp,"InternalPressure"))
        r = AddPN(r,"heat_transfer_coef",   GetProp(shp,"HeatTransferCoef"))
        r = AddPN(r,"effectiveness_pct",    GetProp(shp,"Effectiveness"))
        r = AddPN(r,"heating_surface_m2",   GetProp(shp,"HeatingSurface"))
        r = AddPN(r,"heat_loss_pct",        GetProp(shp,"HeatLoss"))
        r = AddPS(r,"flow_direction",       GetProp(shp,"FlowDirection"))
        r = AddPB(r,"cw_required",          GetProp(shp,"CWRequired"))

    Case "pressure_reducer"
        r = AddPN(r,"pressure_out_kpa",    GetProp(shp,"PressureOut"))
        r = AddPN(r,"pressure_drop_kpa",   GetProp(shp,"PressureDrop"))

    Case "turbo_alternator"
        r = AddPN(r,"pressure_out_kpa",        GetProp(shp,"PressureOut"))
        r = AddPN(r,"pressure_drop_kpa",       GetProp(shp,"PressureDrop"))
        r = AddPN(r,"temperature_out_c",       GetProp(shp,"TemperatureOut"))
        r = AddPN(r,"isentropic_eff_pct",      GetProp(shp,"IsentropicEff"))
        r = AddPN(r,"elec_power_output_kw",    GetProp(shp,"ElecPowerOutput"))
        r = AddPN(r,"mechanical_eff_pct",      GetProp(shp,"MechanicalEff"))
        r = AddPN(r,"electrical_eff_pct",      GetProp(shp,"ElectricalEff"))
        r = AddPB(r,"pressure_feedback",       GetProp(shp,"PressureFeedback"))

    End Select

    CollectStationProps = r
End Function


'═══════════════════════════════════════════════════════════════════
' APPLY RESULTS TO DOCUMENT
' Writes solver output to flow connector Shape Data rows.
' Colours flow connectors by DS% band (§5.2).
' NOTE: Station colours are NOT changed here — they stay YELLOW.
'  Only the Full Balance ribbon icon changes colour (§3).
'═══════════════════════════════════════════════════════════════════
Public Sub ApplyResultsToDocument(doc As Visio.Document, resp As String)
    StoreResults doc, resp

    Dim pg  As Visio.Page
    Dim shp As Visio.Shape
    For Each pg In doc.Pages
        For Each shp In pg.Shapes
            If IsFlowConnector(shp) Then
                On Error GoTo SkipFlow
                Dim sj As String
                sj = FindStreamByID(resp, CStr(shp.ID))
                If sj = "" Then GoTo SkipFlow

                ' Write all fields to Shape Data
                SetProp shp, "WeightFlowRate",    JsonGetStr(sj, "mass_flow_kgh")
                SetProp shp, "Temperature",       JsonGetStr(sj, "temperature_c")
                SetProp shp, "Pressure",          JsonGetStr(sj, "pressure_kpa")
                SetProp shp, "TDM",               JsonGetStr(sj, "tdm_pct")
                SetProp shp, "Sugar",             JsonGetStr(sj, "sugar_pct")
                SetProp shp, "DS",                JsonGetStr(sj, "ds_pct")
                SetProp shp, "Purity",            JsonGetStr(sj, "purity_pct")
                SetProp shp, "Crystals",          JsonGetStr(sj, "crystal_pct")
                SetProp shp, "ISNS",              JsonGetStr(sj, "isns_pct")
                SetProp shp, "Gas",               JsonGetStr(sj, "gas_pct")
                SetProp shp, "Color",             JsonGetStr(sj, "color_icu")
                SetProp shp, "Enthalpy",          JsonGetStr(sj, "enthalpy_kjkg")
                SetProp shp, "FluidType",         JsonGetStr(sj, "fluid_type")
                SetProp shp, "Water",             JsonGetStr(sj, "water")
                SetProp shp, "DissolvedSucrose",  JsonGetStr(sj, "dissolved_sucrose")
                SetProp shp, "NonSucrose1",       JsonGetStr(sj, "non_sucrose_1")
                SetProp shp, "NonSucrose2",       JsonGetStr(sj, "non_sucrose_2")
                SetProp shp, "SucrosecrystALS",   JsonGetStr(sj, "sucrose_crystals")
                SetProp shp, "Fiber",             JsonGetStr(sj, "fiber_isns")
                SetProp shp, "CaO",               JsonGetStr(sj, "cao")
                SetProp shp, "CaCO3",             JsonGetStr(sj, "caco3")
                SetProp shp, "WaterVapor",        JsonGetStr(sj, "water_vapor")
                SetProp shp, "CO2",               JsonGetStr(sj, "co2")
                SetProp shp, "NH3",               JsonGetStr(sj, "nh3")
                SetProp shp, "SolCoefA",          JsonGetStr(sj, "sol_coef_a")
                SetProp shp, "SolCoefB",          JsonGetStr(sj, "sol_coef_b")
                SetProp shp, "SolCoefC",          JsonGetStr(sj, "sol_coef_c")

                ' Colour connector by DS% (§5.2 — inline RGB strings, no Const)
                Dim dsPct As Double
                Dim dsStr As String : dsStr = JsonGetStr(sj, "ds_pct")
                If IsNumeric(dsStr) Then dsPct = CDbl(dsStr) Else dsPct = -1

                Dim lineCol As String
                If dsPct < 0 Then
                    lineCol = "RGB(180,178,169)"   ' Steam / vapor
                ElseIf dsPct < 10 Then
                    lineCol = "RGB(59,139,212)"    ' Thin juice / condensate
                ElseIf dsPct < 30 Then
                    lineCol = "RGB(99,153,34)"     ' Thin-medium
                ElseIf dsPct < 60 Then
                    lineCol = "RGB(186,117,23)"    ' Medium-thick
                ElseIf dsPct < 75 Then
                    lineCol = "RGB(133,79,11)"     ' Thick
                Else
                    lineCol = "RGB(153,60,29)"     ' Massecuite
                End If

                On Error Resume Next
                shp.CellsU("LineColor").FormulaU = lineCol
                On Error GoTo 0

                ' Add flow label (Flow rate, DS, Purity, T)
                Dim kgh  As String : kgh  = JsonGetStr(sj, "mass_flow_kgh")
                Dim pct  As String : pct  = JsonGetStr(sj, "purity_pct")
                Dim tstr As String : tstr = JsonGetStr(sj, "temperature_c")
                shp.Text = BuildFlowLabel(kgh, dsPct, pct, tstr)

SkipFlow:
                On Error GoTo 0
            End If
        Next shp
    Next pg
End Sub

Private Function BuildFlowLabel(kgh As String, dsPct As Double, _
                                  pur As String, temp As String) As String
    Dim s As String
    If IsNumeric(kgh) Then s = Format(CDbl(kgh), "0.0") & " kg/h"
    If dsPct >= 0 Then s = s & "  DS " & Format(dsPct, "0.0") & "%"
    If IsNumeric(pur) Then s = s & "  Pur " & Format(CDbl(pur), "0.0") & "%"
    If IsNumeric(temp) Then _
        s = s & "  T " & Format(CDbl(temp), "0.0") & Chr(176) & "C"
    BuildFlowLabel = Trim(s)
End Function


'═══════════════════════════════════════════════════════════════════
' MASTER NAME → STATION TYPE
' Maps Sugars stencil master names to the 24 station type keys.
'═══════════════════════════════════════════════════════════════════
Public Function MasterNameToType(masterName As String) As String
    Dim n As String : n = LCase(Trim(masterName))

    ' EVAPORATOR family (all bodies + steam pulp dryer + distillation columns)
    If InStr(n,"robert evap")   > 0 Or InStr(n,"falling film")    > 0 Or _
       InStr(n,"forced circ")   > 0 Or InStr(n,"calandria")       > 0 Or _
       InStr(n,"long tube")     > 0 Or InStr(n,"steam pulp")      > 0 Or _
       InStr(n,"rectif")        > 0 Or InStr(n,"beer still")      > 0 Or _
       InStr(n,"stripping col") > 0 Or n = "evaporator"           Then
        MasterNameToType = "evaporator" : Exit Function

    ' PAN (batch and continuous)
    ElseIf InStr(n,"vacuum pan") > 0 Or InStr(n,"vkt") > 0 Or _
           n = "pan" Or n = "batch pan" Or n = "continuous pan"   Then
        MasterNameToType = "pan" : Exit Function

    ' CRYSTALLIZER
    ElseIf InStr(n,"crystallizer") > 0 Or InStr(n,"cryst") > 0 Or _
           InStr(n,"holding tank massecuite") > 0                  Then
        MasterNameToType = "crystallizer" : Exit Function

    ' CENTRIFUGAL
    ElseIf InStr(n,"centrifugal") > 0 Or InStr(n,"centrif") > 0  Then
        MasterNameToType = "centrifugal" : Exit Function

    ' FLASH TANK
    ElseIf InStr(n,"flash tank") > 0 Or InStr(n,"flash") > 0     Then
        MasterNameToType = "flash_tank" : Exit Function

    ' DRYER (before TANK to avoid false match)
    ElseIf InStr(n,"sugar dry") > 0 Or InStr(n,"pulp dry") > 0 Or _
           InStr(n,"dryer")     > 0 Or InStr(n,"granulat")  > 0  Then
        MasterNameToType = "dryer" : Exit Function

    ' MELTER (before TANK)
    ElseIf InStr(n,"melter") > 0 Or n = "melter"                  Then
        MasterNameToType = "melter" : Exit Function

    ' TANK
    ElseIf InStr(n,"storage tank")   > 0 Or _
           InStr(n,"coil heated")    > 0 Or _
           InStr(n,"injection heat") > 0 And InStr(n,"heater") = 0 Or _
           n = "tank"                                               Then
        MasterNameToType = "tank" : Exit Function

    ' INJECTION HEATER (must come after TANK to avoid false match)
    ElseIf InStr(n,"injection heater") > 0 Or InStr(n,"inj. heat") > 0 Then
        MasterNameToType = "injection_heater" : Exit Function

    ' HEAT EXCHANGER
    ElseIf InStr(n,"heat exch")  > 0 Or InStr(n,"plate heat")  > 0 Or _
           InStr(n,"juice heat") > 0 Or InStr(n,"tube shell")   > 0 Or _
           InStr(n,"heater")     > 0                               Then
        MasterNameToType = "heat_exchanger" : Exit Function

    ' SURFACE CONDENSER (before CONTACT CONDENSER)
    ElseIf InStr(n,"surface cond") > 0 Or InStr(n,"surf. cond") > 0 Then
        MasterNameToType = "surface_condenser" : Exit Function

    ' CONTACT CONDENSER
    ElseIf InStr(n,"contact cond") > 0 Or InStr(n,"barometric") > 0  Or _
           InStr(n,"direct cond")  > 0                             Then
        MasterNameToType = "contact_condenser" : Exit Function

    ' COOLER
    ElseIf InStr(n,"cooler") > 0 Or InStr(n,"refriger") > 0 Or _
           InStr(n,"cooling tower") > 0                            Then
        MasterNameToType = "cooler" : Exit Function

    ' THERMOCOMPRESSOR (before COMPRESSOR)
    ElseIf InStr(n,"thermocomp") > 0 Or InStr(n,"thermo comp") > 0 Then
        MasterNameToType = "thermocompressor" : Exit Function

    ' TURBO ALTERNATOR (before TURBINE)
    ElseIf InStr(n,"turbo alt") > 0 Or InStr(n,"turbo gen") > 0  Then
        MasterNameToType = "turbo_alternator" : Exit Function

    ' TURBINE
    ElseIf InStr(n,"turbine") > 0 Or InStr(n,"steam driv") > 0   Then
        MasterNameToType = "turbine" : Exit Function

    ' COMPRESSOR / MVR
    ElseIf InStr(n,"compressor") > 0 Or InStr(n,"mvr") > 0       Then
        MasterNameToType = "compressor" : Exit Function

    ' PRESSURE REDUCER
    ElseIf InStr(n,"pressure reduc") > 0 Or InStr(n,"pr valve") > 0 Or _
           InStr(n,"pressure drop")  > 0                          Then
        MasterNameToType = "pressure_reducer" : Exit Function

    ' DISTRIBUTOR
    ElseIf InStr(n,"distributor") > 0 Or InStr(n,"vapor distrib") > 0 Then
        MasterNameToType = "distributor" : Exit Function

    ' RECEIVER
    ElseIf InStr(n,"receiver") > 0 Or InStr(n,"vapor receiv") > 0 Then
        MasterNameToType = "receiver" : Exit Function

    ' BLENDER / MINGLER
    ElseIf InStr(n,"blender") > 0 Or InStr(n,"mingler") > 0 Or _
           InStr(n,"magma mixer") > 0 Or InStr(n,"cossette mix") > 0 Then
        MasterNameToType = "blender" : Exit Function

    ' PUMP
    ElseIf InStr(n,"pump") > 0                                    Then
        MasterNameToType = "pump" : Exit Function

    ' REACTOR
    ElseIf InStr(n,"reactor") > 0  Or InStr(n,"liming")   > 0 Or _
           InStr(n,"carb")    > 0  Or InStr(n,"lime slak") > 0 Or _
           InStr(n,"ferment") > 0  Or InStr(n,"knife")     > 0 Or _
           InStr(n,"fiberiz") > 0                                 Then
        MasterNameToType = "reactor" : Exit Function

    ' SEPARATOR / FILTER (last broad match)
    ElseIf InStr(n,"separator") > 0 Or InStr(n,"filter")     > 0 Or _
           InStr(n,"clarif")    > 0 Or InStr(n,"diffuser")   > 0 Or _
           InStr(n,"mill")      > 0 Or InStr(n,"press")      > 0 Or _
           InStr(n,"ion exch")  > 0 Or InStr(n,"chromat")    > 0 Then
        MasterNameToType = "separator_filter" : Exit Function

    Else
        MasterNameToType = "unknown"
    End If
End Function


'═══════════════════════════════════════════════════════════════════
' SHAPE IDENTIFICATION
'═══════════════════════════════════════════════════════════════════
Public Function IsStation(shp As Visio.Shape) As Boolean
    If shp.Master Is Nothing Then IsStation = False : Exit Function
    If shp.OneD Then IsStation = False : Exit Function
    Dim t As String : t = MasterNameToType(shp.Master.Name)
    IsStation = (t <> "unknown" And t <> "")
End Function

Public Function IsFlowConnector(shp As Visio.Shape) As Boolean
    If Not shp.OneD Then IsFlowConnector = False : Exit Function
    IsFlowConnector = (shp.Connects.Count > 0)
End Function


'═══════════════════════════════════════════════════════════════════
' STATION NUMBER UNIQUENESS CHECK (§4)
'═══════════════════════════════════════════════════════════════════
Public Function IsStationNumberInUse(num As Long, _
                                      excludeShape As Visio.Shape) As Boolean
    Dim pg  As Visio.Page
    Dim shp As Visio.Shape
    For Each pg In ActiveDocument.Pages
        For Each shp In pg.Shapes
            If shp.ID <> excludeShape.ID Then
                Dim ex As String : ex = GetProp(shp, "StationNumber")
                If ex <> "" And IsNumeric(ex) Then
                    If CLng(ex) = num Then
                        IsStationNumberInUse = True : Exit Function
                    End If
                End If
            End If
        Next shp
    Next pg
    IsStationNumberInUse = False
End Function


'═══════════════════════════════════════════════════════════════════
' SHAPE COLOUR HELPER (§3 — inline RGB strings, no numeric Const)
' §28.4: RGB() must NOT appear in Const declarations.
' Here we use inline strings in the formula which is correct.
'═══════════════════════════════════════════════════════════════════
Public Sub SetShapeColour(shp As Visio.Shape, state As String)
    On Error Resume Next
    Select Case LCase(state)
    Case "red"
        ' §3: RED = dropped, awaiting station number
        shp.CellsU("FillForegnd").FormulaU = "RGB(220,0,0)"
        shp.CellsU("FillBkgnd").FormulaU   = "RGB(220,0,0)"
        shp.CellsU("FillPattern").FormulaU = "1"
        shp.CellsU("Char.Color").FormulaU  = "RGB(255,255,255)"
    Case "blue"
        ' §3: BLUE = numbered, properties not yet entered
        shp.CellsU("FillForegnd").FormulaU = "RGB(0,100,180)"
        shp.CellsU("FillBkgnd").FormulaU   = "RGB(0,100,180)"
        shp.CellsU("FillPattern").FormulaU = "1"
        shp.CellsU("Char.Color").FormulaU  = "RGB(255,255,255)"
    Case "yellow"
        ' §3: YELLOW = properties entered (OK clicked on Properties window)
        ' "The station turns yellow to indicate that data for the station
        '  was entered." — Program_Overview.htm
        shp.CellsU("FillForegnd").FormulaU = "RGB(255,200,0)"
        shp.CellsU("FillBkgnd").FormulaU   = "RGB(255,200,0)"
        shp.CellsU("FillPattern").FormulaU = "1"
        shp.CellsU("Char.Color").FormulaU  = "RGB(0,0,0)"
    End Select
    On Error GoTo 0
End Sub


'═══════════════════════════════════════════════════════════════════
' SHAPE DATA HELPERS
' All Shape Data stored under "Prop.<rowName>" namespace (§21)
'═══════════════════════════════════════════════════════════════════
Public Function GetProp(shp As Visio.Shape, rowName As String) As String
    On Error Resume Next
    GetProp = shp.CellsU("Prop." & rowName & ".Value"). _
              ResultStr(visNone)
    If Err.Number <> 0 Then GetProp = ""
    On Error GoTo 0
End Function

Public Sub SetProp(shp As Visio.Shape, rowName As String, value As String)
    On Error Resume Next
    If Not shp.CellExistsU("Prop." & rowName, visExistsAnywhere) Then
        shp.AddNamedRow visSectionProp, rowName, visTagDefault
    End If
    shp.CellsU("Prop." & rowName & ".Value").FormulaU = _
        """" & EscapeJSON(value) & """"
    On Error GoTo 0
End Sub


'═══════════════════════════════════════════════════════════════════
' MODEL PROPERTIES SHAPE
' Stored as a small rectangle on page 1 (not a stencil shape).
'═══════════════════════════════════════════════════════════════════
Private Function FindModelPropsShape(doc As Visio.Document) As Visio.Shape
    On Error Resume Next
    Dim s As Visio.Shape
    For Each s In doc.Pages(1).Shapes
        If LCase(s.Name) = "model_properties" Then
            Set FindModelPropsShape = s : Exit Function
        End If
    Next s
    Set FindModelPropsShape = Nothing
    On Error GoTo 0
End Function

Private Function CreateModelPropsShape(doc As Visio.Document) As Visio.Shape
    On Error Resume Next
    Dim s As Visio.Shape
    Set s = doc.Pages(1).DrawRectangle(0.05, 10.8, 2.7, 11.4)
    s.Name = "model_properties"
    s.Text = "Purity for Sugar" & vbCrLf & "Model Properties"
    s.CellsU("FillForegnd").FormulaU = "RGB(235,242,252)"
    s.CellsU("LineColor").FormulaU   = "RGB(100,140,200)"
    s.CellsU("Char.Size").FormulaU   = "7pt"
    Set CreateModelPropsShape = s
    On Error GoTo 0
End Function


'═══════════════════════════════════════════════════════════════════
' RESULTS STORAGE
' Stored in doc.Description (simple Phase 01 approach).
'═══════════════════════════════════════════════════════════════════
Private Sub StoreResults(doc As Visio.Document, results As String)
    On Error Resume Next
    doc.Description = results
    On Error GoTo 0
End Sub

Public Function GetStoredResults(doc As Visio.Document) As String
    On Error GoTo NR
    If Not doc Is Nothing Then GetStoredResults = doc.Description
    Exit Function
NR: GetStoredResults = ""
End Function


'═══════════════════════════════════════════════════════════════════
' HTTP HELPERS  (§29)
'═══════════════════════════════════════════════════════════════════
Public Function EngineIsRunning() As Boolean
    Dim r As String : r = HttpGet(ENGINE_URL & "/status")
    EngineIsRunning = (r <> "" And InStr(LCase(r), "running") > 0)
End Function

Private Function HttpPost(url As String, body As String, _
                           timeoutMs As Long) As String
    On Error GoTo Fail
    Dim h As Object : Set h = CreateObject("MSXML2.ServerXMLHTTP")
    h.setTimeouts timeoutMs, timeoutMs, timeoutMs, timeoutMs
    h.Open "POST", url, False
    h.setRequestHeader "Content-Type", "application/json"
    h.setRequestHeader "Accept",       "application/json"
    h.Send body
    ' §29.3: engine always returns HTTP 200 for solver outcomes
    If h.Status = 200 Then HttpPost = h.responseText Else HttpPost = ""
    Exit Function
Fail: HttpPost = ""
End Function

Private Function HttpGet(url As String) As String
    On Error GoTo Fail
    Dim h As Object : Set h = CreateObject("MSXML2.ServerXMLHTTP")
    h.setTimeouts PING_TIMEOUT, PING_TIMEOUT, PING_TIMEOUT, PING_TIMEOUT
    h.Open "GET", url, False : h.Send
    If h.Status = 200 Then HttpGet = h.responseText Else HttpGet = ""
    Exit Function
Fail: HttpGet = ""
End Function

Private Function Base64Decode(s As String) As Byte()
    Dim xml As Object : Set xml = CreateObject("MSXML2.DOMDocument")
    Dim nd  As Object : Set nd  = xml.createElement("b64")
    nd.dataType = "bin.base64" : nd.Text = s
    Base64Decode = nd.nodeTypedValue
End Function


'═══════════════════════════════════════════════════════════════════
' JSON HELPERS
'═══════════════════════════════════════════════════════════════════
Public Function JsonGetStr(json As String, key As String) As String
    Dim pat As String : pat = """" & key & """:"
    Dim pos As Long   : pos = InStr(json, pat)
    If pos = 0 Then JsonGetStr = "" : Exit Function

    pos = pos + Len(pat)
    Do While pos <= Len(json) And Mid(json, pos, 1) = " " : pos = pos + 1 : Loop

    Dim ch As String : ch = Mid(json, pos, 1)
    If ch = """" Then
        pos = pos + 1
        Dim ep As Long : ep = InStr(pos, json, """")
        If ep > 0 Then JsonGetStr = Mid(json, pos, ep - pos) Else JsonGetStr = ""
    ElseIf ch = "n" Then     ' null
        JsonGetStr = ""
    Else                     ' number or boolean
        Dim ei As Long : ei = pos
        Do While ei <= Len(json)
            Dim c As String : c = Mid(json, ei, 1)
            If c = "," Or c = "}" Or c = "]" Or c = " " Then Exit Do
            ei = ei + 1
        Loop
        JsonGetStr = Trim(Mid(json, pos, ei - pos))
    End If
End Function

Private Function FindStreamByID(json As String, _
                                  flowId As String) As String
    Dim tag As String : tag = """id"":""" & flowId & """"
    Dim pos As Long   : pos = InStr(json, tag)
    If pos = 0 Then FindStreamByID = "" : Exit Function

    Dim sp As Long : sp = pos
    Do While sp > 1 And Mid(json, sp, 1) <> "{" : sp = sp - 1 : Loop

    Dim depth As Integer : depth = 0
    Dim ep As Long : ep = sp
    Do While ep <= Len(json)
        Dim cc As String : cc = Mid(json, ep, 1)
        If cc = "{" Then depth = depth + 1
        If cc = "}" Then
            depth = depth - 1
            If depth = 0 Then Exit Do
        End If
        ep = ep + 1
    Loop
    FindStreamByID = Mid(json, sp, ep - sp + 1)
End Function

' ── JSON builders ─────────────────────────────────────────────────
Private Function JStr(k As String, v As String) As String
    JStr = """" & k & """:""" & EscapeJSON(v) & """"
End Function

Private Function JNum(k As String, v As String) As String
    If IsNumeric(v) Then JNum = """" & k & """:" & v _
    Else JNum = """" & k & """:0"
End Function

Private Function JNumN(k As String, v As String) As String
    If v <> "" And IsNumeric(v) Then JNumN = """" & k & """:" & v _
    Else JNumN = """" & k & """:null"
End Function

Private Function JNullOrNum(k As String, v As String) As String
    If v = "" Then JNullOrNum = """" & k & """:null" _
    Else JNullOrNum = """" & k & """:" & v
End Function

Private Function JBool(k As String, v As Boolean) As String
    JBool = """" & k & """:" & IIf(v, "true", "false")
End Function

' ── Accumulator helpers ───────────────────────────────────────────
Public Function AddPS(ex As String, k As String, v As String) As String
    If Trim(v) = "" Then AddPS = ex : Exit Function
    AddPS = ex & IIf(ex = "", "", ",") & JStr(k, v)
End Function

Public Function AddPN(ex As String, k As String, v As String) As String
    If Trim(v) = "" Or Not IsNumeric(v) Then AddPN = ex : Exit Function
    AddPN = ex & IIf(ex = "", "", ",") & JNum(k, v)
End Function

Public Function AddPB(ex As String, k As String, v As String) As String
    If Trim(v) = "" Then AddPB = ex : Exit Function
    Dim bv As Boolean : bv = (LCase(v) = "true" Or v = "1")
    AddPB = ex & IIf(ex = "", "", ",") & JBool(k, bv)
End Function

Private Function EscapeJSON(s As String) As String
    s = Replace(s, "\",   "\\")
    s = Replace(s, """",  "\""")
    s = Replace(s, Chr(13), "\r")
    s = Replace(s, Chr(10), "\n")
    s = Replace(s, Chr(9),  "\t")
    EscapeJSON = s
End Function


'═══════════════════════════════════════════════════════════════════
' FORMATTING HELPERS
'═══════════════════════════════════════════════════════════════════
Private Function FmtN(v As String, fmt As String) As String
    If IsNumeric(v) Then FmtN = Format(CDbl(v), fmt) Else FmtN = "—"
End Function


'═══════════════════════════════════════════════════════════════════
' TYPE DISPLAY NAME
'═══════════════════════════════════════════════════════════════════
Public Function TypeDisplayName(stType As String) As String
    Select Case stType
    Case "evaporator"        : TypeDisplayName = "Evaporator"
    Case "pan"               : TypeDisplayName = "Vacuum Pan"
    Case "crystallizer"      : TypeDisplayName = "Crystallizer"
    Case "centrifugal"       : TypeDisplayName = "Centrifugal"
    Case "blender"           : TypeDisplayName = "Blender"
    Case "distributor"       : TypeDisplayName = "Distributor"
    Case "heat_exchanger"    : TypeDisplayName = "Heat Exchanger"
    Case "injection_heater"  : TypeDisplayName = "Injection Heater"
    Case "flash_tank"        : TypeDisplayName = "Flash Tank"
    Case "tank"              : TypeDisplayName = "Tank"
    Case "melter"            : TypeDisplayName = "Melter"
    Case "cooler"            : TypeDisplayName = "Cooler"
    Case "separator_filter"  : TypeDisplayName = "Separator / Filter"
    Case "dryer"             : TypeDisplayName = "Dryer"
    Case "reactor"           : TypeDisplayName = "Reactor"
    Case "receiver"          : TypeDisplayName = "Receiver"
    Case "pump"              : TypeDisplayName = "Pump"
    Case "turbine"           : TypeDisplayName = "Turbine"
    Case "thermocompressor"  : TypeDisplayName = "Thermocompressor"
    Case "compressor"        : TypeDisplayName = "Compressor (MVR)"
    Case "contact_condenser" : TypeDisplayName = "Contact Condenser"
    Case "surface_condenser" : TypeDisplayName = "Surface Condenser"
    Case "pressure_reducer"  : TypeDisplayName = "Pressure Reducer"
    Case "turbo_alternator"  : TypeDisplayName = "Turbo Alternator"
    Case Else                : TypeDisplayName = stType
    End Select
End Function
