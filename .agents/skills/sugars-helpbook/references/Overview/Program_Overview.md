# Program Overview

 

<span class="hcp3">Sugars™ for Windows® uses Visio® diagramming software
to provide a full graphical interface for building models of sugar
factories and
refineries.</span><span class="hcp4"> </span><span class="hcp3"> Models
are built using drag-and-drop techniques to draw the flow
diagram.</span><span class="hcp4"> </span><span class="hcp3"> Stencils
containing shapes of stations are used to draw the flow diagram of the
process.</span><span class="hcp4"> </span><span class="hcp3"> Connections
are made between shapes using a connector tool with automatic line
routing and
crossovers.</span><span class="hcp4"> </span><span class="hcp3"> Data
for each station and flow stream in the model is entered on windows that
are displayed by double clicking on the station shape, or flow
stream.</span><span class="hcp4"> </span><span class="hcp3"> Changing a
model, after it is built, is done by simply revising the flow diagram
and/or modifying the performance data for any
station.</span><span class="hcp4"> </span><span class="hcp3"> All of the
data for a model is stored in a Microsoft® Access® database that can be
addressed by other
programs.</span><span class="hcp4"> </span><span class="hcp3"> Heat,
material and color balances are quickly obtained from simulations to
predict process
performance.</span><span class="hcp4"> </span><span class="hcp3"> A
revenues window shows the net process revenues to assist with financial
decisions.</span>

 

[Model Building](#Model_Building)

[Simulation](#Simulation)

[Results](#Results)

[Data Import/Export](#Data_Import_Export)

 

<span id="User_Interface642b3b9347ca42c9b00b820c00c373fa=1"></span><span id="User_Interface"></span>

User Interface

 

<span class="hcp3">The graphical interface for Sugars makes model
building a simple matter of dragging pre-drawn shapes from the Shapes
Stencils to the drawing
surface.</span><span class="hcp4"> </span><span class="hcp3"> </span><span class="hcp4"> </span><span class="hcp3">The
shapes are designed to represent actual stations in the
process.</span><span class="hcp4"> </span><span class="hcp3"> Connections
between shapes are drawn using a connection tool that automatically
routes connections between associated
stations.</span><span class="hcp4"> </span><span class="hcp3"> Data
entry windows for controlling the performance of each station are
displayed by double clicking on the station
shape.</span><span class="hcp4"> </span><span class="hcp3"> Flow stream
properties are entered and displayed in a window by double clicking on
the flow stream.</span>

<img src="../../assets/images/Overview/Overview_Dgm-1.png" class="hcp8" data-border="0" />

 

<span class="hcp3">The interface is shown in the figure above when using
Visio 2013. </span><span class="hcp4"> </span><span class="hcp3">Other
versions of Visio may appear
different.</span><span class="hcp4"> </span><span class="hcp3"> Stencils
on the left contain shapes of stations that are used to build a
model.</span><span class="hcp4"> </span><span class="hcp3"> Additional
stencils may be selected using the “More Shapes”
bar.</span><span class="hcp4"> </span><span class="hcp3"> Shapes on a
stencil are dragged from the stencil to the drawing surface and dropped
in place.</span><span class="hcp4"> </span><span class="hcp3"> Drawing
tools are available to design shapes of factory equipment and add them
to the stencils as
needed.</span><span class="hcp4"> </span><span class="hcp3"> Connections
between stations are drawn using a connection tool that features auto
routing around shapes and crossovers (line jumps) for crossing
connection
lines.</span><span class="hcp4"> </span><span class="hcp3"> Drawings can
be composed of different layers and
pages.</span><span class="hcp4"> </span><span class="hcp3"> Full
zoom-in, zoom-out and panning features are provided in the
interface.</span>

 

The selections in the Sugars ribbon menu provided by the SUGARS tab
contain icons for:

 

<table style="width:100%;" data-cellspacing="0" width="675"
data-align="center">
<colgroup>
<col style="width: 34%" />
<col style="width: 64%" />
</colgroup>
<tbody>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Create New Model From
Template</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Close the current model
then open a blank drawing to start a new model.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>Model Properties</p></td>
<td class="hcp11" style="width: 64.67%"><p><span>- Overall properties of
the model such as molecular weights for flow stream components,
iteration accuracy, maximum number of iterations, color values,
atmospheric pressure and default solubility coefficients are set using
this window.</span></p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Default Units</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Units used for all entries
and when a model is saved.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>User Preferences</p></td>
<td class="hcp11" style="width: 64.67%"><p>- <span class="hcp14">Set the
increment between station numbers when adding new stations, renumbering
stations and adding a group of stations.</span><span
class="hcp15"> </span><span class="hcp14"> Select external flow default
pressure, and select whether to update all values or only the changed
values on the drawing.</span></p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Synchronize Database</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Check the drawing and
database for consistency and make any necessary corrections.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>Renumber Stations</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Change the station number
of one, or more, stations.</p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Summary</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Provide a report listing
every flow stream in the model.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>Revenues</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Provide a report giving the
net process revenues.</p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Single</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Balance calculations for a
single pass through the model.  Used to see how the model changes
between balance iterations.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>Full</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Balance calculations for a
full balance of the model.  Icon is:</p>
<p>  <span class="hcp16">Green</span> = model is balanced, <span
style="font-size: 10pt; text-indent: -0.083in; color: #ff0000;">Red</span><span
style="font-size: 10pt; text-indent: -0.083in;"> = model is
unbalanced</span></p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>Last Error/Warning
Message(s)</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Display error or warning
messages from the last balance calculation.</p></td>
</tr>
<tr class="even hcp10">
<td class="hcp11" style="width: 34.83%"><p>Help</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Open the Sugars help
system.</p></td>
</tr>
<tr class="odd hcp10">
<td class="hcp11" style="width: 34.83%"><p>About</p></td>
<td class="hcp11" style="width: 64.67%"><p>- Display the about Sugars
screen.</p></td>
</tr>
</tbody>
</table>

…  

Clicking the **Full** icon will give a full iteration balance of the
model.<span class="hcp4"> </span> If any errors occur during the balance
calculations, they will be displayed on an error, or warning, message
window.<span class="hcp4"> </span> Sometimes revisions to the design of
the model, or data controlling the performance of stations in the model,
may be needed to bring the model into
balance.<span class="hcp4"> </span> The **Last Error/Warning
Message(s)** icon will give the message window that can be referenced as
corrections are made to the model.<span class="hcp4"> </span> Clicking
the **Single** icon will give a single iteration for the model so that
changes between iterations can be
observed.<span class="hcp4"> </span> This can be very helpful to see
where a model may be having problems to do a full balance.

 

The figure below shows the <span class="hcp18">Model Properties</span>
window when it is selected from the Sugars ribbon menu.

<img src="../../assets/images/Overview/Overview_Dgm-2.png" class="hcp8" data-border="0" />

 

 

<span class="hcp3">The **Model Properties** window has entries for
molecular weights for most flow stream components, iteration accuracy
and maximum number of iterations, atmospheric pressure, color values for
pure sucrose in water, invert in water, ash in water and non-sucrose \#2
in water. </span><span class="hcp4"> </span><span class="hcp3">A button
on the bottom of the row of buttons is for setting the default
solubility coefficients.</span>

<img src="../../assets/images/Overview/Overview_Dgm-3.png" class="hcp8" data-border="0" />

 

<span class="hcp3">The above figure shows the **Solubility Coefficients
Defaults** window that is used to enter the solubility coefficients that
will be displayed on all windows that require solubility coefficients to
be entered.</span><span class="hcp4"> </span><span class="hcp3"> Using
this window, the default values for solubility coefficients can be set
individually for each model; that is, different models can have
different default solubility coefficients that are used for entering
solubility coefficients on windows that require solubility coefficients
to be entered.</span>

<img src="../../assets/images/Overview/Overview_Dgm-4.png" class="hcp8" data-border="0" />

 

 

<span class="hcp3">The above figure shows the **Defaults Units**
selection window for selecting the system of units to be used with
Sugars for entering data and displaying results from the balance
calculations.</span><span class="hcp4"> </span><span class="hcp3"> The
default system of units is used when a model is saved, even if the
displayed units are
different.</span><span class="hcp4"> </span><span class="hcp3"> Units
are available for systems in SI, US with temperature in °C and US with
temperature in °F.</span>

 

<span class="hcp14">Also shown on the figure above, the stencils on the
left contain shapes of stations that can be used to build a
model.</span><span class="hcp15"> </span><span class="hcp14"> Each of
the station types in Sugars is represented on the stencils and many of
the stations have more than one shape that can be used to represent the
same type of
station.</span><span class="hcp15"> </span><span class="hcp14"> Other
unique shapes can be drawn and added to the stencils, if
needed.</span><span class="hcp15"> </span><span class="hcp14"> There is
no limit to the number of different shapes that can be used to represent
the Sugars station types.</span><span class="hcp4"> </span> See
[Designing Your Own
Shapes](../Station_Modules/Designing_Your_Own_Shapes.htm) for further
information.

 

<img src="../../assets/images/Overview/Overview_Dmg-5.png" class="hcp8" data-border="0" />

 

 

<span class="hcp3">The above figure shows the **User Preferences**
window.</span><span class="hcp4"> </span><span class="hcp3"> Entries on
this window will change the station number increment as new stations are
added to a model, the station increment when stations are renumbered and
the station increment for stations in a
group.</span><span class="hcp4"> </span><span class="hcp3"> Also, it
controls whether the atmospheric pressure or 0.0 is used when new
external flows are added to a
model.</span><span class="hcp4"> </span><span class="hcp3"> User
Preferences are set for the computer being used; hence, the preferences
will apply to all models that are built and modified on the same
computer.</span>

 

Consistency between the drawing and the Sugars database that contains
all of the data for a model can be checked at any time by using the
**Synchronize Database** option.<span class="hcp4"> </span> When this
option is selected, Sugars will examine each object on the drawing
(stations and connecting flow streams) and verify that the database has
corresponding entries.<span class="hcp4"> </span> If it finds any errors
or differences it will try to fix them and display a message that says
errors were found.<span class="hcp4"> </span> The drawing always
controls the entries in the database.<span class="hcp4"> </span> That
is, if a station or flow is in the database but not on the drawing, then
the entry in the database will be
deleted.<span class="hcp4"> </span> And, if the drawing has a station or
flow that is not in the database, then a corresponding entry will be
made in the database.

 

Stations can be renumbered at any time by selecting either one
individual station or a group of stations and then selecting the
<span class="hcp18">Renumber Stations</span> option. The increment
between each station that is renumbered (if more than one is being
renumbered) is controlled by the User Preferences window shown above.

 

The **Summary** icon gives the Summary report that can be displayed and
printed out.<span class="hcp4"> </span> The figure below shows the
Summary report which lists every flow stream in the
model.<span class="hcp4"> </span> External flows are listed first with
internal flows between stations listed
next.<span class="hcp4"> </span> The **Revenues** icon gives the Net
Process Revenues report shown below where a value can be entered for
every flow stream that leaves the model and a cost can be entered for
every external flow into the model.<span class="hcp4"> </span> The
difference between the revenues and the costs give the net process
revenues for the model.

 

<img src="../../assets/images/Overview/Overview_Dmg-6.png" class="hcp8" data-border="0" />

 

 

<img src="../../assets/images/Overview/Overview_Dmg-7.png" class="hcp8" data-border="0" />

 

<span class="hcp14">Complete help systems are available from the main
menu for both Visio and Sugars (see figure
below).</span><span class="hcp15"> </span><span class="hcp14"> **Visio
Help** describes all of the drawing features available in Visio and
**Sugars Help** describes each of the stations, input properties,
examples and features of each
station.</span><span class="hcp15"> </span><span class="hcp14"> Also,
the Sugars help system describes how to design shapes so that they will
work with Sugars</span><span class="hcp3"> </span> (see [Designing Your
Own Shapes](../Station_Modules/Designing_Your_Own_Shapes.htm)) and other
features of the program.

<img src="../../assets/images/Overview/Overview_Dmg-8.png" class="hcp8" data-border="0" />

 

Input and output connections for shapes stay glued to the shapes even
when the shapes are moved, or the flow streams are rerouted. Stations
can be copied from one part of the flow diagram and pasted into another
part with the data for the station repeated in the copied station. Also,
groups of stations may be combined and placed on the drawing as a group
instead of having to add each station individually (station numbers for
each station are entered when the group is dropped on the drawing). See
[Grouping Shapes](../Station_Modules/Grouping_Shapes.htm) for further
information.

 

<span id="Model_Building642b3b9347ca42c9b00b820c00c373fa=2"></span><span id="Model_Building"></span>

Model Building

 

<span class="hcp3">Every model of a factory, refinery, or portion of a
process is built by selecting stations from the available station
modules in Sugars and connecting the stations together using flow
streams.</span><span class="hcp4"> </span><span class="hcp3"> Flow
streams between stations, and flow streams that leave a model, are
called *internal
flows*.</span><span class="hcp4"> </span><span class="hcp3"> Flow
streams that go into the model from outside sources (e.g., beets, steam,
water, CaO, etc.) are called *external flows*. All external flows must
be fully specified before a balance can be
done.</span><span class="hcp4"> </span><span class="hcp3"> Internal
flows are calculated by Sugars during the balance
calculations.</span><span class="hcp4"> </span><span class="hcp3"> When
a shape is dragged from a stencil to the drawing surface, a window
appears to assign a number to the station (see figure below).</span>

<img src="../../assets/images/Overview/Overview_Dmg-9.png" class="hcp8" data-border="0" />

 

The Station Number for each station in a model must be
unique.<span class="hcp4"> </span> Sugars will automatically index the
station numbers by 10 (or as set in User Preferences) as each new one is
added to the flow diagram; however, the number may be changed on the
window to any unused number in the model.

 

<span class="hcp3">Each Sugars station type has a data input window that
is associated with the shapes for that type of
station.</span><span class="hcp4"> </span><span class="hcp3"> The data
input window defines the properties of each station (or object) in a
model.</span><span class="hcp4"> </span><span class="hcp3"> Drawing the
process flow diagram defines the
model.</span><span class="hcp4"> </span><span class="hcp3"> The output
flows emitted from a station are a result of the properties of the
station.</span><span class="hcp4"> </span><span class="hcp3"> Changing
the properties of a station will control how the station processes flows
coming into the
station.</span><span class="hcp4"> </span><span class="hcp3"> For
example, an evaporator station, with juice and steam inputs, will
process the juice flow to evaporate water while using steam, or vapor,
to boil the juice. Thus, the properties of the stations in a model and
the characteristics of the external flows into the model control all of
the internal flows between stations, and the flows leaving the
model.</span><span class="hcp4"> </span><span class="hcp3"> Each station
type has a properties window for entering the appropriate data, and a
window is provided for entering the data to define external flows into
the model.</span>

 

Shapes on the stencils are associated with their respective Sugars
station modules by naming the shape in Visio with a Sugars station name
and identifying the input and output ports for the station. See
[Designing Your Own
Shapes](../Station_Modules/Designing_Your_Own_Shapes.htm) for further
information.

 

<span class="hcp3">The shape color turns to blue after the station
number is
entered.</span><span class="hcp4"> </span><span class="hcp3"> Double
click the shape with the left mouse button to get the data entry window
for the station (see the Evaporator Properties window in the figure
below).</span>

 

<img src="../../assets/images/Overview/Overview_Dmg-10.png" class="hcp8" data-border="0" />

 

All of the necessary data to describe the performance of the station is
entered on the Properties window. The station turns yellow to indicate
that data for the station was entered after clicking on the
O<span class="hcp18">K</span> button to close the Evaporator Properties
window. Shapes are added to the drawing until all of the stations for
the model are on the drawing and data is entered for each station until
all of the stations in the model have turned to yellow.

 

<span class="hcp3">Connections are made between input and output ports
on each station using the connection tool until all of the ports on the
stations have connecting
flows.</span><span class="hcp4"> </span><span class="hcp3"> Some
stations, such as melters, tanks and receivers, do not need to have all
of their ports connected (extra ports are provided), but these stations
must have at least one input and one output flow.</span>

<img src="../../assets/images/Overview/Overview_Dmg-11.png" class="hcp8" data-border="0" />

<span class="hcp3">Data for external flows into the model is entered on
the External Flow Properties window (see
above).</span><span class="hcp4"> </span><span class="hcp3"> Double
clicking on the external flow or right clicking and selecting
"S<u>u</u>gars properties" from the drop-down menu gives the External
Flows Properties window (see figure
above)</span><span class="hcp3">.</span><span class="hcp24"> </span><span class="hcp3"> </span>**<span class="hcp3">Every
external flow stream going into the model must be specified with
pressure, temperature and flow stream
components.</span>**<span class="hcp24"> </span><span class="hcp3"> If
the flow stream contains dissolved non-sucrose components, the
solubility coefficients must be
defined.</span><span class="hcp4"> </span><span class="hcp3"> And, if
the flow is not a required flow, the quantity of the flow stream must be
specified.</span><span class="hcp4"> </span><span class="hcp3"> *Required*
flows are flows that have their quantity determined by the properties of
a station.</span><span class="hcp4"> </span><span class="hcp3"> For
example, the vapor flow into a pan is a required flow because the
quantity of the vapor needed by the pan is determined by the properties
of the pan and the syrup flow into the
pan.</span><span class="hcp4"> </span><span class="hcp3"> A flow stream
color entry must be made for the external flow if the color balance is
being done.</span><span class="hcp4"> </span><span class="hcp3"> And, a
currency value for the flow stream can be entered if the net process
revenues are being calculated for the
model.</span><span class="hcp4"> </span><span class="hcp3"> Successful
model building with Sugars requires organization and careful layout of
the factory’s stations and flow
streams.</span><span class="hcp4"> </span><span class="hcp3"> Poorly
designed models do not balance well and they are unstable when changes
or revisions are made at a later
time.</span><span class="hcp4"> </span><span class="hcp3"> Also, good
drawing methods can make it much easier to follow the process
flows.</span>

 

<span id="Simulation642b3b9347ca42c9b00b820c00c373fa=3"></span><span id="Simulation"></span>

Simulation

 

The model is ready for balancing once the data for every station and
every external flow stream is entered. The balance calculations give a
simulation of the process and provide all of the details of the internal
flow streams in the model.

<img src="../../assets/images/Overview/Overview_Dmg-12.png" class="hcp8" data-border="0" />

 

<span class="hcp3">Clicking on the **Full** balance icon will initiate
the balance calculations and give a small window showing the progress of
the
iterations.</span><span class="hcp4"> </span><span class="hcp3"> Clicking
on the **Single** balance icon will give one-balance iteration to
observe the progress of the
balance.</span><span class="hcp4"> </span><span class="hcp3"> An error
message window will appear if any errors are detected during the
iterations.</span><span class="hcp4"> </span><span class="hcp3"> Fatal
errors have to be corrected before the calculations can be
completed.</span><span class="hcp4"> </span><span class="hcp3"> Sometimes
warning or informative messages appear giving information about the
calculations, or observations about the
model.</span><span class="hcp4"> </span><span class="hcp3"> Many of
these messages do not require any action by the user, but are merely
displayed as information that might be important, or helpful to the
user.</span><span class="hcp4"> </span><span class="hcp3"> The
error/warning message window may be recalled at any time after the
balance calculations are done so that it can be referred to as
corrections are made to remove any errors that occurred during the
balance
calculations.</span><span class="hcp4"> </span><span class="hcp3"> Clicking
on the **Last Error/Warning Message(s)** icon will recall the display of
the last error messages that occurred during a
balance.</span><span class="hcp4"> </span>

 

<span id="Results642b3b9347ca42c9b00b820c00c373fa=4"></span><span id="Results"></span>

Results

 

The results of the calculations can be displayed after the balance
calculations are completed. Sugars provides several different
presentations of the results.

<img src="../../assets/images/Overview/Overview_Dmg-13.png" class="hcp8" data-border="0" />

<span class="hcp3">The figure above shows the display of the Internal
Flow Properties window after a
balance.</span><span class="hcp4"> </span><span class="hcp3"> This
window shows all of the details of the internal flow, such as pressure,
temperature, flow quantity, components, color and solubility
coefficients.</span><span class="hcp4"> </span><span class="hcp3"> In
addition, the % total dry matter (TDM), % sugar, % dry substance (DS), %
purity, % crystals, % insoluble solid non-sugars (ISNS) and % gas are
given in the middle of the window with the quantity of flow in tons per
hour.</span><span class="hcp4"> </span><span class="hcp3"> Clicking the
**DS and Purity** button, under the Flow Stream Components in the Liquid
phase section, will give the % dry substance and purity for the liquid
portion of the
flow.</span><span class="hcp4"> </span><span class="hcp3"> For a
massecuite, this would be the mother liquor %DS and % Purity.</span>

 

<span class="hcp25">Clicking the **Parameters** button on the Internal
Flow Properties window gives additional characteristics of the flow,
such as: volume flow, specific weight, enthalpy, specific heat capacity,
supersaturation and boiling point elevation (see figure
below).</span><span class="hcp4"> </span><span class="hcp25"> Place the
cursor on the “Volume flow” “Liquid” displayed value to see the liquid
portion of the flow displayed as liters per minute (lpm) or gallons per
minute (gpm) depending on the units (SI or US) being
used.</span><span class="hcp4"> </span><span class="hcp25"> The Flow
Stream Parameters feature is also available for external flows.</span>

# <img src="../../assets/images/Overview/Overview_Dmg-14.png" class="hcp8" data-border="0" />

 

Every internal flow in the model can be displayed using the Properties
window. Also, flow streams that are required and/or pressure feedback
(flow streams that need a pressure value from another station) are
identified on the flow diagram by a small 'R' for required and a small
'P' for pressure feedback. Sugars will place these indicators on the
flow streams after the balance calculations are completed.

 

The Internal Flow Properties window has a small internal flow scroll
able selection window that shows every internal flow stream in the
model. Using this window, individual flow streams can be displayed
quickly without having to close the Internal Flow Properties window and
double click on another flow stream to display its properties. The
External Flow Properties window also has a similar external flow
selection window for viewing external flows. The internal and external
flow properties windows provide valuable information about the process
that can be used for engineering design and/or data reconciliation.

 

Some external and internal flow data and parameters can be displayed on
the drawing obviating the need to open the properties windows. Right
click the flow stream and from the drop-down menu that appears, select
"Add Flow Legend..." (see figure below).

<img src="../../assets/images/Overview/Overview_Dmg-15.png" class="hcp8" data-border="0" />

 

 

Select the data to be displayed when the flow legend menu appears (see
figure below).

 

<img src="../../assets/images/Overview/Overview_Dmg-16.png" class="hcp8" data-border="0" />

 

 

The displayed data can be positioned and formatted using the normal
Visio methods and it will be updated by Sugars after each balance (see
figure below).

 

<img src="../../assets/images/Overview/Overview_Dmg-17.png" class="hcp8" data-border="0" />

 

 

Data can also be displayed on the drawing using Visio Shape
Data.<span class="hcp4"> </span> Every station and flow stream has Shape

 

 

<img src="../../assets/images/Overview/Overview_Dmg-18.png" class="hcp8" data-border="0" />

 

 

Data associated with it.  The Shape Data is stored in the Visio
ShapeSheet and it can be displayed in the Visio Shape Data
window.<span style="font-family: Arial, sans-serif;">
 </span><span class="hcp14">Click the **DATA** tab and then check the
“Shape Data Windows” check box to have Visio display the Shape Data in a
collapsible window (see figure
above).</span><span class="hcp15"> </span><span class="hcp14"> The Shape
Data can be displayed on the drawing and/or used in calculations using
the Visio **INSERT** \> **Field** feature (see [Shape Data
Display](../Program_Operation/Shape_Data_Display.htm)).</span>

 

In addition, Shape Data can be exported to either an embedded or
external Microsoft Excel spreadsheet.<span class="hcp4"> </span> Visual
Basic for Applications (VBA) is used to make the connection between the
Shape Data and Excel (see <span class="hcp16">[Exporting Data to
Excel](../Program_Operation/Exporting_Data_to_Excel.htm)</span>).

 

Printouts are available for the Summary and Revenues
reports.<span class="hcp4"> </span> These reports provide an overview of
the balance calculations. The Summary report (see figure below) shows
every flow stream in the model with the characteristics of each flow
listed along with the station the flow originates from and the station
to which it goes. <span class="hcp4"> </span>The flow quantity, TDM%
(total dry matter percent), Sugar% (sugar percent), DSmas% (percent dry
substance including sucrose crystals – if any), PUmas% (percent purity
including sucrose crystal - if any), CRY% (percent sucrose crystals),
Temp (temperature in °C or °F), ISNS% (percent insoluble solids
non-sucrose), and color is printed for each flow stream. The Summary
report is a listing of the same summary information that is on the
Internal Flow Properties and External Flow Properties windows for each
flow.

 

# <img src="../../assets/images/Overview/Overview_Dmg-19.png" class="hcp8" data-border="0" />

 

The Revenues report (see figure below) is a report of the process net
revenues that are generated by the model. The process net revenues are
calculated from the revenue values for all flows leaving the model
(internal flow) minus the cost of all flows into the model (external
flows).<span class="hcp4"> </span> As changes are made to the process,
the net revenues will either increase, or decrease.
<span class="hcp4"> </span>New process equipment with new station
properties, or changes in the process routing, can be evaluated quickly
to see now the revenues will change. <span class="hcp4"> </span>This
information is very useful for making investment decisions. Also, it is
the most convenient way to show how changes to the model will affect the
financial operating performance of the process.

 

# <img src="../../assets/images/Overview/Overview_Dmg-20.png" class="hcp8" data-border="0" />

 

The revenues and costs value entries for all external flows into the
model and internal flows that leave the model are entered on the
External Flow Properties and Internal Flow Properties windows. These
values are used to calculate the process net revenues. The entered
values also can be changed on the Process Net Revenues window as shown
in the figure above.

 

<span id="Data_Import_Export642b3b9347ca42c9b00b820c00c373fa=5"></span><span id="Data_Import_Export"></span>

**<span style="font-size: 11.0pt;">Data Import/Export</span>**

 

Data Import/Export is an optional feature of Sugars that can be added to
the Sugars license.<span class="hcp4"> </span> It allows importing data
directly into an opened model from an external e**X**tensible **M**arkup
**L**anguage (XML) file.<span class="hcp4"> </span> Also, data can be
exported from the model to an XML file that can then be read by other
programs.<span class="hcp4"> </span> This allows changes to be made to
the model that can then be exported to other software that can process
the file for either reports or to use as set points for the factory.

 

<span class="hcp25">Every station in a model has an Equipment ID entry
field and a unique ID must be entered for every station that is
importing or exporting
data.</span><span class="hcp4"> </span><span class="hcp25"> A schema
file is used to define the format for the XML file and data is keyed to
the Equipment ID’s for each
station.</span><span class="hcp4">   </span><span class="hcp25"> The
data import/export feature uses these Equipment ID’s to place the data
from the XML file into the proper
station.</span><span class="hcp4"> </span><span class="hcp25"> Station
and external and internal flow data can be imported as defined in the
“AMS Import PropertiesRev\_.pdf” document in the **…Sugars\AMS**
subdirectory.</span><span class="hcp4"> </span><span class="hcp25"> External
flow data in an XML file is aligned with the station that it goes to by
the Equipment ID and the input port number for the
station.</span><span class="hcp4"> </span><span class="hcp25"> Internal
flow data is aligned with the flow that leaves a station and port
number. </span>

<img src="../../assets/images/Overview/Data_Import_Export_Scn-7.png" class="hcp8"
data-border="0" />

 

The figure above shows the data Import/Export icon as it appears if this
feature is licensed for the copy of Sugars being
used.<span class="hcp4"> </span> Clicking the left mouse button on the
**Import/Export** icon will give the Data Import/Export window shown
below.

 

<img src="../../assets/images/Overview/Data_Import_Export_Scn-8.png" class="hcp8"
data-border="0" />

 

 

 

[User Interface](Program_Overview.htm)

[Model Building](#Model_Building)

[Simulation](Program_Overview.htm)

[Results](Program_Overview.htm)

[Data Import/Export](#Data_Import_Export)
