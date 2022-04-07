from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs
import physical_spaces as ps

from bob.connections.air import *
from bob.core import bind_model_namespace, dump

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


# Comment
"""
Now looking at the plan, we miss a detail regarding air movement. How is the return air
dealt with ?

A single return in the open office ? In this case, air will be forced through doors up 
to the open office... 

Return grills in each room open on a big plenum covering the entire floor ?

Most probably, the bathroom doesn't have a return grill... just an exhaust... but again,
we miss this information.

Both scenarios are possible and they will endup being modeled differently

Based on what we have here, it's impossible to know exactly.

Knowing that, I'll still try to connect the HVAC Spaces to get the more probably air flow

"""
corridorNorth_doors = AirConnection(
    label="CorridorNorthDoors",
    comment="There are 3 doors in this space, so I'm using a connection to model those relationships",
)
# My model of spaces include 1 input for doors, 1 input for Windows, etc... if there are multiple of those, use a connection.
hs.kitchenette_hvac.doors >> hs.corridorSouth_hvac.doors
hs.corridorSouth_hvac.airTransfer >> hs.corridorNorth_hvac.airTransfer
hs.corridorNorth_hvac.doors >> corridorNorth_doors
hs.privateoffice_hvac.doors >> corridorNorth_doors
hs.bathroom_hvac.doors >> corridorNorth_doors
hs.openoffice_hvac.doors >> corridorNorth_doors

outdoor = AirConnection(
    label="Outdoor",
    comment="This is where we exhaust air of bathroom, and windows of OpenOffice are connected here to",
)

openoffice_windows = AirConnection(
    label="OpenOfficeWindows",
    comment="There are 2 windows connected to the space, so I use a connection",
)

mixedAir = AirConnection(
    label="MixedAirDuct",
    comment="Mix between return air and outdoor air",
)
returnExhaut = AirConnection(
    label="Return / Exhaust",
    comment="Paths for return or exhaust",
)

supplyAir = AirConnection(
    label="SUPPLY-DUCT", comment="Supply Air Duct that feed VAV Boxes 1 & 2"
)

returnAir = AirConnection(
    label="RETURN-DUCT", comment="Return Air Duct extracting air from open office"
)

plenum = AirConnection(
    label="Plenum",
    comment="Plenum. It's where Duct Static Pressure Low port is connected",
)

# AHU
outdoor >> hd.ahu["OADPR"] >> mixedAir
hd.ahu["MADPR"] >> mixedAir
mixedAir >> hd.ahu["FILTER"] >> hd.ahu["HTGCOIL"] >> hd.ahu["CLGCOIL"] >> hd.ahu[
    "SF"
] >> supplyAir
hs.openoffice_hvac.ductAirOutlet >> returnAir >> hd.ahu["RF"] >> returnExhaut >> hd.ahu[
    "EADPR"
] >> outdoor
returnExhaut >> hd.ahu["MADPR"]

# AHU Sensors
hd.ahu["OA-T"].hasMeasurementLocation = outdoor
hd.ahu["TPD1"].hasMeasurementLocationHigh = hd.ahu["FILTER"].airInlet
hd.ahu["TPD1"].hasMeasurementLocationLow = hd.ahu["FILTER"].airOutlet
hd.ahu["HC-T"].hasMeasurementLocation = hd.ahu["HTGCOIL"].airOutlet
hd.ahu["DA-T"].hasMeasurementLocation = hd.ahu["CLGCOIL"].airOutlet
hd.ahu["TPD2"].hasMeasurementLocationHigh = hd.ahu["SF"].airOutlet
hd.ahu["TPD2"].hasMeasurementLocationLow = plenum
hd.ahu["TPD3"].hasMeasurementLocationHigh = hd.ahu["RF"].airOutlet
hd.ahu["TPD3"].hasMeasurementLocationLow = plenum

# Windows
hd.window1.outdoor >> outdoor
hd.window1.indoor >> openoffice_windows
hd.window1.hasPhysicalLocation = ps.openoffice

hd.window2.outdoor >> outdoor
hd.window2.indoor >> openoffice_windows
hd.window2.hasPhysicalLocation = ps.openoffice
openoffice_windows >> hs.openoffice_hvac.windows

# Exhaust Fan
hd.bathroom_exhaust_fan.airInlet << hs.bathroom_hvac.ductAirOutlet
hd.bathroom_exhaust_fan.airOutlet >> outdoor


# VAV Boxes
# Relationships between devices and positioning sensors
supplyAir >> hd.vav1["VAV1_damper"].airInlet
hd.vav1["VAV1_damper"].airOutlet >> hd.vav1["VAV1_HeatingCoil"].airInlet
hd.vav1["VAV1_HeatingCoil"].airOutlet >> hs.privateoffice_hvac.ductAirInlet
hd.vav1["VAV1_SA-F"].hasMeasurementLocation = hd.vav1["VAV1_damper"].airInlet
hd.vav1["VAV1_DA-T"].hasMeasurementLocation = hd.vav1["VAV1_HeatingCoil"].airOutlet
hd.vav1["VAV1_ZN-T"].hasMeasurementLocation = hs.openoffice_hvac
hd.vav1["VAV1_ZN-T"].hasPhysicalLocation = ps.openoffice

supplyAir >> hd.vav2["VAV2_damper"].airInlet
hd.vav2["VAV2_damper"].airOutlet >> hd.vav2["VAV2_HeatingCoil"].airInlet
hd.vav2["VAV2_HeatingCoil"].airOutlet >> hs.kitchenette_hvac.ductAirInlet
hd.vav2["VAV2_SA-F"].hasMeasurementLocation = hd.vav2["VAV2_damper"].airInlet
hd.vav2["VAV2_DA-T"].hasMeasurementLocation = hd.vav2["VAV2_HeatingCoil"].airOutlet
hd.vav2["VAV2_ZN-T"].hasMeasurementLocation = hs.corridorSouth_hvac
hd.vav2["VAV2_ZN-T"].hasPhysicalLocation = ps.corridor

hs.hvac_zone_1.airInlet.mapsTo = hs.privateoffice_hvac.ductAirInlet
hs.hvac_zone_1.airOutlet.mapsTo = hs.openoffice_hvac.ductAirOutlet

hs.hvac_zone_2.airInlet.mapsTo = hs.kitchenette_hvac.ductAirInlet
hs.hvac_zone_2.airOutlet.mapsTo = hs.corridorSouth_hvac.airTransfer

# Would be nice to make this when we create the system...
hd.vav1.airInlet.mapsTo = hd.vav1["VAV1_damper"].airInlet
hd.vav1.airOutlet.mapsTo = hd.vav1["VAV1_HeatingCoil"].airOutlet
hd.vav2.airInlet.mapsTo = hd.vav2["VAV2_damper"].airInlet
hd.vav2.airOutlet.mapsTo = hd.vav2["VAV2_HeatingCoil"].airOutlet

if __name__ == "__main__":
    dump()
