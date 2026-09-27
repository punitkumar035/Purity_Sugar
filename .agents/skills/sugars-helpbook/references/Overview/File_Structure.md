# File Structure

 

Data for each model is stored in a Microsoft Access
database.<span class="hcp1"> </span> The database file for a model has a
".sgd" extension; whereas, the Visio drawing file has a ".vsd"
extension.<span class="hcp1"> </span> Each station type has a table in
the database where all of the station data for each of the stations of
that type are stored.<span class="hcp1"> </span> For example, data for
each centrifugal in a model is stored in the "tblCentrifugal" table of
the Access database for the model.<span class="hcp1"> </span> Each row
in the table for a station type contains the data for one station in the
model of the same station type.<span class="hcp1"> </span> Each column
in the table contains data for one of the properties of the
station.<span class="hcp1"> </span> All columns for each table are
labeled as to their corresponding property on the station property
window.

 

All flow streams are stored in a separate table called
"tblFlows".<span class="hcp1"> </span> Each row contains the data for
each flow stream in a model and the columns contain the data fields for
each flow stream.<span class="hcp1"> </span> External flow streams
(flows into the model from outside sources) have a "0" in the field for
the "StationFromNumber" column.<span class="hcp1"> </span> Internal flow
streams (flows going between stations) that leave the model have a "0"
in the field for the "StationToNumber"
column.<span class="hcp1"> </span> All columns are labeled to give the
properties of the flow stream to correspond with the characteristics of
the flow.<span class="hcp1"> </span> For example, pressure, temperature,
quantity, components, solubility coefficients, and color.
