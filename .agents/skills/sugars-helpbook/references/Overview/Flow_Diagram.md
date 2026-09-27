# Flow Diagram

 

Sugars is used to analyze a sugar factory process by constructing a flow
diagram of the process.<span class="hcp1"> </span> The flow diagram
consists of individual stations with interconnecting flows and external
flows that go into the process.<span class="hcp1"> </span> *External*
flows are all flows that go into the flow diagram from outside sources;
e.g., beets, or cane, into the factory, juice from storage, water for
dilution, remelt sugar from storage, sweepings, steam for heating,
etc.<span class="hcp1"> </span> Individual *stations* are computer
models that use mathematical relationships and actual process data to
model the stations used in the process.

 

All of the external flows are processed by the stations in the flow
diagram to provide output flows from each station that are processed by
other stations in the flow diagram until all of the material and heat
entering the flow diagram is accounted for by the flows and losses
leaving the flow diagram.<span class="hcp1"> </span> Interconnecting
flows within flow diagrams that go to and from each station are called
*internal* flows in contrast to external flows that originate from
sources outside the process.

 

Each station in the flow diagram is given a station
number.<span class="hcp1"> </span> All output flows from each station
are identified and either routed to another station, or shown to leave
the flow diagram.<span class="hcp1"> </span> Any arrangement of the
stations is possible.<span class="hcp1"> </span> Therefore, virtually
any process can be evaluated provided the stations in Sugars can be used
to simulate the actual stations used in the process.

 

Often combining several stations to model an actual station is necessary
if the actual station does not conform to a station available in
Sugars.<span class="hcp1"> </span> For example, a juice clarifier (see
figure below) can be modeled using a cooler station (1050) for heat
loss, a separator station (1051) to separate insoluble components (for
example, CaCO3) and impurities from the juice, a blender station (1053)
to maintain a moisture content for the mud underflow and a distributor
station (1052) to feed the blender with sufficient juice to maintain the
moisture content in the mud and send the remaining juice out as the
overflow (see figure below).<span class="hcp1"> </span> Other similar
combinations can be used to provide a model of most stations in an
actual process that do not have corresponding duplicate stations in
Sugars with the same operating characteristics.

 

<img src="../../assets/images/Overview/Flow_Diagram_Clarifier.png" class="hcp3"
data-border="0" />

 

Sugars will accept any station number between 1 and
9999.<span class="hcp1"> </span> When numbering stations, it is best to
start the numbering at a number higher than 1 and allow for gaps between
numbers so that future additions can be accomplished easily without
having to renumber all of the stations in the
model.<span class="hcp1">  </span> Using numbers in a given range for
each page makes it easier to locate a
station.<span class="hcp1"> </span> For example, if milling is on one
page and all of the station numbers on the milling page are between 500
and 999, then searching for station no. 650 is much easier because it
will be located on the milling page.

 

**Keeping the initial model simple is best when building a model of a
process, or factory.<span class="hcp1"> </span> Do not try to model the
intricate details of a process, or factory at the
beginning.<span class="hcp1"> </span> Add complexity to the model after
gaining experience with the simpler model.**

 

The origin and destination station numbers identify flow streams within
a flow diagram.<span class="hcp1"> </span> If a flow stream leaves the
flow diagram, it is given a "0" for the destination station number when
the flow stream is stored in the
database.<span class="hcp1"> </span> And, if a flow stream is an
external flow, then the originating station number will be “0”.

 

<span class="hcp4">A typical 4-effect evaporator station is shown in the
figure below to illustrate how a flow diagram can be constructed using
the different stations available in
Sugars.</span><span class="hcp1"> </span><span class="hcp4"> As shown,
each station has been assigned a station number and all of the flows
from each station go to another station, or leave the flow diagram; for
example, syrup, condensates and
vapors.</span><span class="hcp1"> </span><span class="hcp4"> The only
external flows into the flow diagram are steam, juice and cold
water.</span><span class="hcp1"> </span><span class="hcp4"> Distributor
stations (for example, station numbers 516, 526 and 536) are used to
split a flow stream into several flows and receiver stations (for
example, station numbers 515, 525, 531 and 535) are used to combine
several flow
streams.</span><span class="hcp1"> </span><span class="hcp4"> Intermingling
of material, steam, vapor, and condensate lines within the flow diagram
allows Sugars to do the complete heat, material and color
balances.</span><span class="hcp1"> </span><span class="hcp4"> After the
model has been constructed, Sugars can quickly evaluate the effects of
changes made to the process.</span>

 

<img src="../../assets/images/Overview/4-Effect%20Multiple.png" class="hcp3"
data-border="0" />

 

Some stations can have more than one input
flow.<span class="hcp1"> </span> The input ports of the station
determine the type of flow.<span class="hcp1"> </span> For example, a
pan station will have a syrup flow into port number 0 and a vapor flow
into port number 1.<span class="hcp1"> </span> The input ports are
labeled on each station when it has more than one
input.<span class="hcp1"> </span> Receivers can have up to ten input
flows, and tanks and melters can have up to ten input flows and one
heating flow.<span class="hcp1"> </span> Blenders and thermocompressors
have two input flows.<span class="hcp1">  </span> Centrifugals have
massecuite and wash input flows.

 

In all cases, stations that use heat (for example, pans, evaporators,
melters, tanks and heat exchangers) are limited to a quantity of one
input flow into the heating port.

 

Heater, melter and tank stations can have either coil, or injection,
heating.<span class="hcp1"> </span> Coil heating is used to transfer
heat from the heating flow to the material flow without the two flow
streams being mixed (that is, both a material flow and heating flow go
into and leave the station); whereas, with injection heating, the
heating flow is injected into the material flow stream (that is, only a
material flow stream leaves the
station).<span class="hcp1"> </span> Sugars gives full consideration to
changes that occur in the material flow stream due to injected heating
flows.

 

A distributor can have up to ten output flows, a centrifugal has either
two (or three) outputs, and a separator has two output flows - all other
stations are limited to only one output material flow
stream.<span class="hcp1"> </span> Vapor and condensate output flows
from a station depend on the station and its input values; for example,
injection, or coil heating for heat exchangers, tanks and melters;
whereas, pans, dryers and evaporators always have material, vapor and
condensate output flows.

 

Stations that have both material and heating input flow streams process
the flows based on the input port used for the input
flow.<span class="hcp1"> </span> The station will identify, by input
port number, which flow stream is the material and which is the heating
flow.

 

<span class="hcp1"> </span>Phase changes that occur in the process are
considered in the appropriate stations.<span class="hcp1"> </span> For
example, crystallizers and pans can have a phase change for sucrose
going from dissolved to crystalline, and a cooler station can cause
vapor condensation due to heat loss in the
station.<span class="hcp1"> </span> The stations in Sugars have been
designed to give considerable control over changes in flow stream
characteris­tics.

 

<span class="hcp6">Normally, a receiver station is used to accept
multiple inputs for any station that needs to have more than one input
flow; for example, in the previous flow diagram example, two condensate
flows go to the receiver (station no. 531) that feeds the flash tank
(station no.
532).</span><span style="mso-spacerun: yes; font-family: Arial, sans-serif;"> </span><span class="hcp6"> Since
a flash tank can accept only one input flow, a receiver station is
placed in front of the flash tank to accept the two input flows</span>
(see [Station Modules](../Station_Modules/About_Station_Modules.htm)
section for further information about each station).
