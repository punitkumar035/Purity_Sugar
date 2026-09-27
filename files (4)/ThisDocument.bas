Attribute VB_Name = "ThisDocument"
'
' ╔══════════════════════════════════════════════════════════════════╗
' ║  Purity for Sugar  —  ThisDocument.bas                          ║
' ║  Phase 01  |  v1.0  |  Document-level event handlers            ║
' ╚══════════════════════════════════════════════════════════════════╝
'
' SOURCE RULES: RULES_v4.md
'   §2  How a Model is Built — Step by Step
'   §3  Shape Colour Scheme (RED → BLUE → YELLOW)
'   §4  Station Numbering Rules
'   §5  Flow Streams (connectors open flow window)
'   §28 VBA Implementation Rules (§28.1 events MUST be here)
'
' ══════════════════════════════════════════════════════════════════
' INSTALLATION — READ THIS BEFORE ANYTHING ELSE
' ══════════════════════════════════════════════════════════════════
'  1. Save your drawing as  Sugar_Model.vsdm  (Macro-Enabled Drawing)
'     File → Save As → Visio Macro-Enabled Drawing (*.vsdm)
'     Events do NOT fire from .vsdx files. §28, §27.
'
'  2. Open the VBA editor:  Alt + F11
'
'  3. Import the two standard modules first:
'       File → Import File → StationDialogManager.bas
'       File → Import File → PurityForSugar.bas
'
'  4. Now paste THIS file into ThisDocument:
'     a) In Project panel (left), expand "Microsoft Visio Objects"
'     b) Double-click "ThisDocument (Sugar_Model)"
'     c) Select ALL existing code: Ctrl+A
'     d) Delete it
'     e) Paste the entire contents of this file
'     f) Ctrl+S
'
'  5. Close VBA editor (Alt+F4 or the X button)
'
'  6. Open the Sugars stencils:
'     View tab → Shapes → More Shapes → Open Stencil
'     Select all 10  Sug_*.vss  files from your Sugars installation.
'
'  7. Test:
'     Drag any station shape from a stencil onto the canvas.
'     Expected: shape turns RED → InputBox appears → enter number →
'               shape turns BLUE with number as label.
'
' ──────────────────────────────────────────────────────────────────
Option Explicit


'═══════════════════════════════════════════════════════════════════
' EVENT 1 — Shape dropped onto canvas
'
' RULES_v4 §2 Step 3: "Immediately on drop: station number window
' appears → shape is RED"
' RULES_v4 §3: RED = awaiting number, BLUE = number assigned
' RULES_v4 §4: Range 1-9999, unique across all pages
' RULES_v4 §28.1: This event MUST live in ThisDocument
'═══════════════════════════════════════════════════════════════════
Private Sub Document_ShapeAdded(ByVal Shape As IVShape)

    ' ── Guard: only handle Sugars station shapes ──────────────────
    If Shape.Master Is Nothing Then Exit Sub   ' no stencil master
    If Shape.OneD Then Exit Sub                ' connectors are 1D

    Dim stType As String
    stType = PurityForSugar.MasterNameToType(Shape.Master.Name)
    If stType = "unknown" Or stType = "" Then Exit Sub

    ' ── STEP 1: Turn RED immediately (§3) ─────────────────────────
    ' "The station being numbered will turn RED until the number
    '  is assigned." — Grouped_Stations.htm
    PurityForSugar.SetShapeColour Shape, "red"

    ' ── STEP 2: Show station number InputBox ──────────────────────
    Dim sNum   As String
    Dim prompt As String

    Do
        prompt = "ASSIGN STATION NUMBER  (1 – 9999)"              & vbCrLf & _
                 "Station type:  " & _
                   PurityForSugar.TypeDisplayName(stType)          & vbCrLf & vbCrLf & _
                 "Rules (§4):"                                     & vbCrLf & _
                 "  • Lower numbers are solved FIRST"              & vbCrLf & _
                 "  • Number in the direction material flows"      & vbCrLf & _
                 "  • Leave gaps of 10 between unrelated stations" & vbCrLf & _
                 "  • Each number must be unique (all pages)"      & vbCrLf & vbCrLf & _
                 "Click Cancel to remove this shape."

        sNum = InputBox(prompt, "New Station — Purity for Sugar", "")

        ' Cancel → delete the shape immediately (§4: cancel = delete)
        If StrPtr(sNum) = 0 Then
            Shape.Delete
            Exit Sub
        End If

        Dim n As String : n = Trim(sNum)

        ' ── Validate ──────────────────────────────────────────────
        If n = "" Then
            MsgBox "A station number is required." & vbCrLf & _
                   "Click Cancel to remove this shape instead.", _
                   vbExclamation, "Purity for Sugar"

        ElseIf Not IsNumeric(n) Or InStr(n, ".") > 0 Then
            MsgBox "Enter a whole number between 1 and 9999.", _
                   vbExclamation, "Purity for Sugar"

        ElseIf CLng(n) < 1 Or CLng(n) > 9999 Then
            MsgBox "Station number must be between 1 and 9999.", _
                   vbExclamation, "Purity for Sugar"

        ElseIf PurityForSugar.IsStationNumberInUse(CLng(n), Shape) Then
            MsgBox "Station number " & n & " is already in use." & vbCrLf & _
                   "Each station must have a unique number." & vbCrLf & _
                   "Tip: leave gaps of 10 so you can insert later.", _
                   vbExclamation, "Purity for Sugar"

        Else
            Exit Do   ' ← valid
        End If
    Loop

    ' ── STEP 3: Store data and turn BLUE (§3) ─────────────────────
    ' "After the station number is assigned, the station will turn
    '  blue." — Grouped_Stations.htm
    PurityForSugar.SetProp Shape, "StationNumber", Trim(sNum)
    PurityForSugar.SetProp Shape, "Type",          stType
    PurityForSugar.SetShapeColour Shape, "blue"
    Shape.Text = Trim(sNum)   ' station number displayed as shape label

End Sub


'═══════════════════════════════════════════════════════════════════
' EVENT 2 — Shape double-clicked
'
' RULES_v4 §2 Step 6: "Double-click a station → Properties window
' opens → enter performance data → click OK → shape turns YELLOW"
' RULES_v4 §5: Flow connectors open the flow properties window
'═══════════════════════════════════════════════════════════════════
Private Sub Document_ShapeDoubleClicked(ByVal Shape As IVShape)

    ' ── 1D shape (flow connector) → show flow properties (§5) ────
    If Shape.OneD Then
        PurityForSugar.ShowFlowProperties Shape
        Exit Sub
    End If

    ' ── Station shape → open Properties window ────────────────────
    If Shape.Master Is Nothing Then Exit Sub

    Dim stType As String
    stType = PurityForSugar.MasterNameToType(Shape.Master.Name)
    If stType = "unknown" Or stType = "" Then Exit Sub

    ' Defensive: shape must have been numbered first
    Dim sNum As String
    sNum = PurityForSugar.GetProp(Shape, "StationNumber")
    If sNum = "" Then
        MsgBox "This shape has no station number." & vbCrLf & _
               "Delete it and drag it from the stencil again.", _
               vbExclamation, "Purity for Sugar"
        Exit Sub
    End If

    ' Open Properties window.
    ' The YELLOW colour is applied INSIDE OpenStationProperties,
    ' only after the user clicks OK — not before (§3).
    PurityForSugar.OpenStationProperties Shape, stType

End Sub


'═══════════════════════════════════════════════════════════════════
' EVENT 3 — Document opened
' Pings the calculation engine and reports status in the status bar.
'═══════════════════════════════════════════════════════════════════
Private Sub Document_DocumentOpened(ByVal doc As IVDocument)
    On Error Resume Next
    If PurityForSugar.EngineIsRunning() Then
        Application.StatusBar = _
            "Purity for Sugar  ✓  Engine ready on localhost:8765"
    Else
        Application.StatusBar = _
            "Purity for Sugar  ✗  Engine not running" & _
            "  —  start purity_engine.exe then use Macros > RunSimulation"
    End If
    On Error GoTo 0
End Sub
