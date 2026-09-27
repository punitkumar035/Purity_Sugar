# Cane Factory (Diffusion)

 

<img src="../../assets/images/Examples/Cane_Factory_(Diffusion)_Dgm-1.png" class="hcp2"
data-border="0" />

Diffusion

 

<span class="hcp4">The model of a cane factory with a diffuser is the
same as the milling factory except for the first
page.</span><span class="hcp5"> </span><span class="hcp4"> The above
figure shows the first page (Diffusion page) with a
diffuser.</span><span class="hcp5"> </span><span class="hcp4"> Cane
preparation is done by one set of knives and a fiberizer - both of which
are driven by steam
turbines.</span><span class="hcp5"> </span><span class="hcp4"> Bagasse
after the diffuser is dewatered in a steam driven
mill.</span><span class="hcp5"> </span><span class="hcp4"> A separator
station controls the quantity of steam to the knife and fiberizer as a
ratio to the quantity of the total cane
flow.</span><span class="hcp5"> </span><span class="hcp4"> The ratio
could be set to the fiber in the cane as an alternative method for
controlling the steam quantity.</span>

 

<span class="hcp4">The diffuser is modeled using cells/stages that
consist of a receiver, separator, distributor and blender stations in an
arrangement that allows for fiber to move through the diffuser with
decreasing amounts of sucrose and non-sucrose
components.</span><span class="hcp5"> </span><span class="hcp4"> Seven
identical combinations are used so that injection steam and
recirculation juice flow streams are modeled like the actual
diffuser.</span><span class="hcp5"> </span><span class="hcp4"> The
results of the model can be adjusted in the separator and blender
stations to give the same operating results as measured in the
factory.</span><span class="hcp5"> </span><span class="hcp4"> Because
the separation of sucrose and non-sugars from fiber can be controlled in
each of the cells, it is not necessary to have as many cells to achieve
the same performance in the model as in the actual diffuser in the
factory; however, a diffuser model could be constructed to have the same
number of cells as the actual diffuser.</span>

 

Draft for the diffuser is controlled by blender station no. 161 which
ratios the quantity of makeup water to the fiber content of the flow
into the blender. Changing the ratio will quickly change the draft on
the diffuser, sucrose extraction and mixed juice characteristics.

<img src="../../assets/images/Examples/Cane_Factory_(Diffusion)_Dgm-6.png" class="hcp2"
data-border="0" />

Steam/Water

 

The figure above shows the Steam/Water page for the boiler, turbo
alternator and cooling water loop with cooling
tower.<span class="hcp5"> </span> The boiler grouping is a simple model
for the boiler that uses a separator station (no. 4701) to ratio the
fuel to the boiler feed water. <span class="hcp5"> </span>The reactor
station no. 4703 is used to convert feed water to
steam.<span class="hcp5"> </span> The efficiency of the conversion is
100% (all of the feed water is converted to steam) and the heat of
reaction is set to give a temperature for the steam leaving the reactor
that is higher than the live steam out of the
boiler.<span class="hcp5"> </span> A blender station (no. 4704) is used
to control the temperature of the live steam by using feed water to
reduce the steam temperature to the actual live steam
temperature.<span class="hcp5"> </span> The pressure of the live steam
is set in the boiler feed water pump.<span class="hcp5"> </span> Other
boiler groupings are available on the Equipment stencil that can provide
automatic adjustment of the fuel depending on the moisture content of
the fuel.

 

The cooling tower is modeled using a flash tank (station no. 4020) and a
cooler (station no. 4021) to give cooling water at the correct
temperature for the pan and evaporator
condensers.<span class="hcp5"> </span> Excess water from the cooling
loop is discharged from distributor station no. 4040.
