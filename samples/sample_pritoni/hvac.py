from pathlib import Path

import hvac_devices as hd
import hvac_spaces as hs
import physical_spaces as ps

from bob.connections.air import *
from bob.core import UNIT, bind_model_namespace, dump
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.sensor.temperature import Temperature

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


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
returnExhaust = AirConnection(
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
outdoor >> hd.ahu["OADPR"].airInlet  # >> mixedAir
hd.ahu["OADPR"]["damper"] >> mixedAir
hd.ahu["MADPR"]["damper"] >> mixedAir
(
    mixedAir
    >> hd.ahu["FILTER"]
    >> hd.ahu["HTGCOIL"]
    >> hd.ahu["CLGCOIL"]
    >> hd.ahu["SF"]
    >> supplyAir
)
hs.openoffice_hvac.ductAirOutlet >> returnAir >> hd.ahu["RF"].airInlet
hd.ahu["RF"].airOutlet >> returnExhaust >> hd.ahu["EADPR"]["damper"].airInlet
hd.ahu["EADPR"]["damper"] >> outdoor
returnExhaust >> hd.ahu["MADPR"].airInlet

# AHU Sensors
hd.ahu["OA-T"] % outdoor
hd.ahu["TPD1"]["highPort"] % hd.ahu["FILTER"].airInlet
hd.ahu["MA-T"] % hd.ahu["FILTER"].airInlet
hd.ahu["TPD1"]["lowPort"] % hd.ahu["FILTER"].airOutlet
hd.ahu["HC-T"] % hd.ahu["HTGCOIL"].airOutlet
hd.ahu["DA-T"] % hd.ahu["CLGCOIL"].airOutlet
hd.ahu["TPD2"]["highPort"] % hd.ahu["SF"].airOutlet
hd.ahu["TPD2"]["lowPort"] % plenum
hd.ahu["TPD3"]["highPort"] % hd.ahu["RF"].airOutlet
hd.ahu["TPD3"]["lowPort"] % plenum

hd.ahu["RF_VFD"].drive_running = OnOffStatus(label="VFD DriveRunning")
hd.ahu["RF_VFD"].run_command = OnOffCommand(label="Run Command")

hd.boiler.hotWaterLeaving >> hd.hot_water_pump.waterInlet
hd.hot_water_pump.waterOutlet >> hd.ahu["HTGCOIL"].hotWaterInlet

hd.ahu["HTGCOIL"].hotWaterOutlet >> hd.htg_vlv["valve"].waterInlet
hd.htg_vlv.waterOutlet >> hd.boiler.hotWaterEntering

hd.chiller.chilledWaterLeaving >> hd.chilled_water_pump.waterInlet
hd.chilled_water_pump.waterOutlet >> hd.ahu["CLGCOIL"].chilledWaterInlet
hd.ahu["CLGCOIL"].chilledWaterOutlet >> hd.clg_vlv["valve"].waterInlet
hd.clg_vlv["valve"].waterOutlet >> hd.chiller.chilledWaterEntering


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
# Relationships between Equipment and positioning sensors
supplyAir >> hd.vav1["VAV1_damper"].airInlet
hd.vav1.hasPhysicalLocation = ps.private_office
hd.vav1["VAV1_damper"]["damper"].airOutlet >> hd.vav1["VAV1_HeatingCoil"].airInlet

# vav1 >> hs.hvac_zone_1
hd.vav1["VAV1_HeatingCoil"].airOutlet >> hs.privateoffice_hvac.ductAirInlet
hd.vav1["VAV1_SA-F"] % hd.vav1["VAV1_damper"]["damper"].airInlet
hd.vav1["VAV1_DA-T"] % hd.vav1["VAV1_HeatingCoil"].airOutlet
hd.vav1["VAV1_ZN-T"] % hs.openoffice_hvac
hd.vav1["VAV1_ZN-T"].hasPhysicalLocation = ps.openoffice


supplyAir >> hd.vav2["VAV2_damper"].airInlet
hd.vav2.hasPhysicalLocation = ps.kitchenette
hd.vav2["VAV2_damper"].airOutlet >> hd.vav2["VAV2_HeatingCoil"].airInlet

# vav2 >> hs.hvac_zone_2
hd.vav2["VAV2_HeatingCoil"].airOutlet >> hs.kitchenette_hvac.ductAirInlet
hd.vav2["VAV2_SA-F"] % hd.vav2["VAV2_damper"]["damper"].airInlet
hd.vav2["VAV2_DA-T"] % hd.vav2["VAV2_HeatingCoil"].airOutlet
hd.vav2["VAV2_ZN-T"] % hs.corridorSouth_hvac
hd.vav2["VAV2_ZN-T"].hasPhysicalLocation = ps.corridor

hs.hvac_zone_1.airInlet.mapsTo = hs.privateoffice_hvac.ductAirInlet
hs.hvac_zone_1.airOutlet.mapsTo = hs.openoffice_hvac.ductAirOutlet

hs.hvac_zone_2.airInlet.mapsTo = hs.kitchenette_hvac.ductAirInlet
hs.hvac_zone_2.airOutlet.mapsTo = hs.corridorSouth_hvac.airTransfer

# hd.vav1.airInlet.mapsTo = hd.vav1["VAV1_damper"].airInlet
# hd.vav1.airOutlet.mapsTo = hd.vav1["VAV1_HeatingCoil"].airOutlet
# hd.vav2.airInlet.mapsTo = hd.vav2["VAV2_damper"].airInlet
# hd.vav2.airOutlet.mapsTo = hd.vav2["VAV2_HeatingCoil"].airOutlet

hd.ahu.outsideAirInlet.mapsTo = hd.ahu["OADPR"].airInlet
hd.ahu.returnAirInlet.mapsTo = hd.ahu["MADPR"].airInlet
hd.ahu.supplyAirOutlet.mapsTo = hd.ahu["SF"].airOutlet
hd.ahu.exhaustAirOutlet.mapsTo = hd.ahu["EADPR"].airOutlet
hd.ahu.electricalInlet.mapsTo = hd.ahu["SF_Starter"].electricalInlet

if __name__ == "__main__":
    dump()
