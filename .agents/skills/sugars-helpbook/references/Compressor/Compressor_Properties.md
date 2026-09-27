# Compressor Properties

 

<img src="../../assets/images/Compressor/CompressorProperties_Scn-1.png" style="border: none;"
data-border="0" />

 

 

Equipment ID An equipment ID of up to 11 characters can be used to
identify the station with an actual station in the process. Any
combination of numbers and letters that are used in the factory/refinery
to identify equipment can be entered. For example, Equipment ID =
123.456A. It is not necessary to make an entry in the Equipment ID field
if the station in the model does not have a corresponding station in the
factory/refinery.

 

Station Name A name of up to 20 characters must be entered for the
station. For example, Station Name = 1st Vapor Compressor.

 

Pressure Discharge pressure from the compressor can be specified by
either specifying a discharge pressure or by using pressure feedback to
set the pressure from another station.

 

Discharge Enter Discharge Pressure for flow out of a compressor. If the
flow goes to a receiver station, the discharge pressure will be
determined by pressure feedback from the receiver if a value of 0.0 is
entered; otherwise, enter a value for Discharge Pressure that will be
held during the simulation. For example, Discharge Pressure = 320 kPa.

 

Feedback Check the Feedback box to use pressure feedback for the
discharge pressure from the compressor. If the output flow leaves the
model, the discharge pressure will be set to atmospheric pressure (see
[Program Overview \> User Interface](../Overview/Program_Overview.htm)).

 

Discharge Temperature Enter Discharge Temperature (°C) for vapor leaving
the compressor, or turbine. For example, Discharge Temperature =
125.8°C.

 

 

[Compressor Features](Compressor_Features.htm)

[Compressor Examples](Compressor_Examples.htm)
