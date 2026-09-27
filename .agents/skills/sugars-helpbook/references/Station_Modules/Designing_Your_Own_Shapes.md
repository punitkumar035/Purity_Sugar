# Designing Your Own Shapes

 

Visio Developer Mode is necessary to design shapes for use with
Sugars.  Activate Developer Mode by clicking
<span class="hcp2">FILE</span> \> <span class="hcp2">Options</span> \>
<span class="hcp2">Advanced</span> and then click the box for "Run in
developer mode" (see screen below).  Click the
<span class="hcp2">OK</span> button to return to the drawing window.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-1.png" class="hcp5"
data-border="0" />

 

 

Custom shapes of Sugars stations can be designed using the Visio Drawing
Tools. Open the Blank drawing in the "C:\Program Files\Sugars\Examples"
sub-directory.<span class="hcp6"> </span> Create the shape and use the
Group selection on the **DEVELOPER** tab to group all of the shape's
elements into one grouped assembly.<span class="hcp6"> </span> After the
shape is drawn and grouped, use the Connection Point Tool on the Visio
Drawing Toolbar as shown on the screen below to make the input and
output connections. Make sure the shape is highlighted with a border
around it and click the left mouse button on the connection
tool.<span class="hcp6"> </span> Hold the Control key down and position
the cursor at the points on the shape where the connections are to be
added. Click the left mouse button at each point and a magenta colored
<span style="color: #FF66FF;">■</span> should appear as each new
connection point is added.<span class="hcp6"> </span> The connections
should be made in the order of the ports; i.e., for the pan station
shown in the figure below, input port 0 first, input port 1 next, then
output port 0, output port 1, and output port 2 last.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-2.png" class="hcp5"
data-border="0" />

 

 

A text field must be added that Sugars can use to assign a station
number to the shape as it is added to a flow diagram. The Visio
SmartShape Wizard can be used to create the text
box.<span class="hcp6"> </span> The SmartShape Wizard is located in the
C:\Program Files\Sugars\Utilities
directory.<span class="hcp6"> </span> Highlight the new shape and then
double click the wizard from Windows Explorer (or make a shortcut to the
wizard on the Desktop).<span class="hcp6"> </span> The wizard options
are self-explanatory, and it will create a text field to be the top most
field in the order of the shapes.

 

A station name must be assigned so Sugars will recognize the new
shape.<span class="hcp6"> </span> Highlight the shape so that there is a
selection border around the shape.<span class="hcp6"> </span> Click
**DEVELOPER <span class="hcp9">\></span>** **Show ShapeSheet**
<span class="hcp9">\> **<u>S</u>hape** as shown on the screen
below</span>.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-3.png" class="hcp5"
data-border="0" />

 

 

This will open the ShapeSheet for the new
shape.<span class="hcp6"> </span> The ShapeSheet has several sections
that are used to control the behavior of the
shape.<span class="hcp6"> </span> The screen below shows the ShapeSheet
in the Visio window.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-4.png" class="hcp5"
data-border="0" />

 

 

The ShapeSheet in the screen above shows a **Connection Points**
section, but a **User-defined cells** section is needed to name the
shape.<span class="hcp6"> </span> The **User-defined cells** section can
be added by clicking **Insert** in the Sections group on the Visio
ribbon (see screen below) and then clicking the **User-defined cells**
box.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-5.png" class="hcp5"
data-border="0" />

 

Click on the first cell in the first row under User-defined Cells and
type **Class** in the cell editing
area.<span class="hcp6"> </span> Click on the green check next to the
entry field, or press the **Enter** key when
done.<span class="hcp6"> </span> Click on the cell in the first row
under **Value** in the **User-defined Cells**
area.<span class="hcp6"> </span> Enter the name of the shape with
quotation marks around the name in the cell editing space and click the
green check next to the entry field, or press the **Enter** key when
finished.<span class="hcp6"> </span> For example, type **"SI_Pan"** to
name a pan shape (see screen below).<span class="hcp6"> </span> This is
the name Sugars will recognize when the shape is dragged from a stencil
and dropped onto a drawing.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-6.png" class="hcp5"
data-border="0" />

 

Next the connection points need to be identified so they can be
recognized by Sugars as the shape is added to a
drawing.<span class="hcp6"> </span> Use the following procedure to
identify the input and output connections.

 

Make sure the shape is highlighted with the green border and the shape
sheet is shown.<span class="hcp6">  </span> On the shape sheet, click on
the first cell in the first row under **Connection Points** and type in
the port number in the entry field next to the green check at the top of
the window.<span class="hcp6"> </span> Input port numbers start with
Input0 and are numbered in sequence.<span class="hcp6"> </span> The
input port numbers must coincide with the flows into the station in the
same relationship as they are for all stations of the same
type.<span class="hcp6"> </span> For example, a Pan station has two
input ports.<span class="hcp6"> </span> Input port 0 (Input0) is for
syrup and Input port 1 (Input1) is for
steam/vapor.<span class="hcp6"> </span> A black box is shown around the
connection point on the shape as each cell (row) of the **Connections
Points** is checked.

 

As shown in the screen below at the top of the window, the name of the
first input connection (syrup) is entered as **Input0** (do not enclose
the entry in quotation marks " ").<span class="hcp6"> </span> Enter
**Input1** <span class="hcp9">on **Row_2**</span> for the second input
connection (steam/vapor) for the pan.<span class="hcp6"> </span> Click
on the green check next to the input box, or press **Enter** when
finished with the entry.<span class="hcp6"> </span> Type **Output0** for
the first output connection (massecuite), **Output1** for the second
output connection (vapor) and **Output2** for the third output
connection (condensate).<span class="hcp6"> </span> Be sure to label
each connection correctly for the type of input and output flow.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-7.png" class="hcp5"
data-border="0" />

 

The ShapeSheet should look as shown in the screen below where the shape
name is in the User-defined Cells in the User.Class row and “SI_Pan” is
in the Value column.<span class="hcp6"> </span> Also, each connection
point for the ports into and out of the station are listed and named.

 

<img src="../../assets/images/Station_Modules/Designing_Shapes_Scn-8.png" class="hcp5"
data-border="0" />

 

Close the ShapeSheet.

 

The new shape is now ready to be placed on a stencil for use in building
flow diagrams.<span class="hcp6"> </span> To place the new shape on a
stencil, open the stencil and then right click on the stencil title bar
and select **Edit Stencil** from the drop-down
menu.<span class="hcp6"> </span> Then drag the new shape from the
drawing on to the stencil.<span class="hcp6"> </span> Once the shape is
on the stencil, the shape can be named by selecting the stencil and then
using the **<u>E</u>dit Master** \> **Master
P<u>r</u>operties…**<span class="hcp6"> </span> to name the shape and
enter text for the prompt.

 

Save the stencil with the new shape by right clicking the stencil title
bar and selecting **Save <u>A</u>s…** from the drop-down menu and saving
the new stencil under the same name, or giving it a new
name.<span class="hcp6"> </span> The stencil can be used with any other
drawing by opening it as a stencil from the
drawing.<span class="hcp6"> </span> <span style="color: #ff0000;">It is
best to not add custom shapes to the Sugars stencils because these
custom shapes may become lost when Sugars is updated with a new version
at a later time and the Sugars stencils could be overwritten with the
update.</span>
