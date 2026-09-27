# Melter Features

 

Melter A melter station is used to combine flow streams and melt sucrose
crystals using heat (if necessary). Three different melter shapes are
provided with Sugars as shown below.

 

<img src="../../assets/images/Melter/MelterFeatures_Fig-1.png" style="border: none;"
data-border="0" />

 

General Features <span class="hcp4">As its name suggests, a melter
station is used to melt sucrose crystals in process flow streams (input
ports 0 thru 9).</span><span class="hcp5"> </span><span class="hcp4"> It
can be heated by a heating flow (input port
10).</span><span class="hcp5"> </span><span class="hcp4"> The heating
can be either by injection heating (heating flow is absorbed into the
process flow stream), or by coil heating (heating flow is not absorbed
into the process flow stream, but leaves the melter after giving up heat
to the process
flow).</span><span class="hcp5"> </span><span class="hcp4"> Sucrose
crystals, if any, are melted until the output flow stream is saturated
(that is, supersaturation coefficient is 1.0); however, crystal growth
is not allowed, even if the input flow is
supersaturated.</span><span class="hcp5"> </span><span class="hcp4"> Up
to ten process flows can flow into a melter, but only one heating flow
is allowed.</span><span class="hcp5"> </span><span class="hcp4"> The
pressure of the process flow out of the melter will always be at
atmospheric pressure, despite the pressures of any of the process or
heating input
flows.</span><span class="hcp5"> </span><span class="hcp4"> If any input
flows are pressure feedback flows, the pressure fed back will be
atmospheric pressure.</span>

 

<span style="font-size: 10.0pt; mso-fareast-font-family: 'Times New Roman'; mso-ansi-language: EN-US; mso-fareast-language: EN-US; mso-bidi-language: HE; font-family: Arial, sans-serif;">The
input flow into port 9 will be a required flow if an entry is made for
the dry substance out of the melter (see</span>  [Melter
Properties](Melter_Properties.htm) <span class="hcp4">for "Hold TDM at"
entry
field).</span><span style="mso-spacerun: yes; font-size: 10pt;"> </span><span class="hcp4"> If
a dry substance is not specified, the flow into port 9 will not be
required unless the output flow from the melter is required and the
input flow into port 9 is selected to satisfy the required output
flow.</span>

 

<span class="hcp4">If a heating flow into port 10 is used, it will
always be a required
flow.</span><span class="hcp5"> </span><span class="hcp4"> If a
temperature value is not entered for the flow out of the melter, the
quantity of the heating flow will be set to 0.0 by Sugars.</span>

 

<span class="hcp4">The output flow from a melter can be required by
another station, and if it is, one of the input flows into the melter
must be made a required flow that can be adjusted by Sugars to satisfy
the required output
flow.</span><span class="hcp5"> </span><span class="hcp4"> The quantity
of the required input flow will be calculated by Sugars to equal the
required output flow quantity less the quantities of all other flows
into the melter.</span><span class="hcp5"> </span><span class="hcp4"> A
small box will appear on the Melter Properties window to select which
input flow is to be required when the output flow is
required.</span><span class="hcp5"> </span><span class="hcp4"> Input
flows into the melter from other stations that cannot be made required
will not be displayed in the box.</span>

 

 

[Melter Properties](Melter_Properties.htm)

[Melter Examples](Melter_Examples.htm)
