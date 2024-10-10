from pathlib import Path

import electrical_devices as ed
import functions as fn
import hvac_devices as hd
import lighting_devices as ld
import lighting_spaces as ls
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.enum import OccupancyStatus, OnOffEnum

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")

hd.vav1["DA-T"].observedProperty.set_value(72.3)  # PD-SR-MP VAV1 Outlet Temperature
hd.vav2["DA-T"].observedProperty.set_value(71.2)  # PD-SR-MP VAV2 Outlet Temperature
hd.ahu["DA-T"].observedProperty.set_value(70.2)  # PD-SR-MP VAV1&VAV2 Inlet Temperature

# hd.bathroom_exhaust_fan.onOffStatus = OnOffEnum.On
hd.ahu["RF_VFD"].drive_running = OnOffEnum.On
# hd.ahu['SF-STARTER']['SF-STARTER.sensor'].onOffStatus = OnOffEnum.On
hd.ahu["TPD3"].observedProperty.set_value(
    129.3
)  # !!! My TPD3 is static pressure...not flow

# lighting spaces are all unoccupied
ls.openofficeNorth_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied
ls.openofficeSouth_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied
ls.bathroom_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied
ls.corridor_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied
ls.privateoffice_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied
ls.kitchenette_lightspace.occupancy.hasValue = OccupancyStatus.Unoccupied

ld.openofficeNorth_luminaire_1.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeNorth_luminaire_2.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeNorth_luminaire_2.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeSouth_luminaire_3.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeSouth_luminaire_3.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeSouth_luminaire_4.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeSouth_luminaire_4.onOffCommand.hasValue = OnOffEnum.Off

ld.bathroom_luminaire_5.onOffStatus.hasValue = OnOffEnum.Off
ld.bathroom_luminaire_5.onOffCommand.hasValue = OnOffEnum.Off

ld.bathroom_luminaire_6.onOffStatus.hasValue = OnOffEnum.Off
ld.bathroom_luminaire_6.onOffCommand.hasValue = OnOffEnum.Off

ld.privateoffice_luminaire_8.onOffStatus.hasValue = OnOffEnum.Off
ld.privateoffice_luminaire_8.onOffCommand.hasValue = OnOffEnum.Off

ld.privateoffice_luminaire_8.onOffStatus.hasValue = OnOffEnum.Off
ld.privateoffice_luminaire_8.onOffCommand.hasValue = OnOffEnum.Off

ld.corridor_luminaire_9.onOffStatus.hasValue = OnOffEnum.Off
ld.corridor_luminaire_9.onOffCommand.hasValue = OnOffEnum.Off

ld.corridor_luminaire_10.onOffStatus.hasValue = OnOffEnum.Off
ld.corridor_luminaire_10.onOffCommand.hasValue = OnOffEnum.Off

ld.kitchenette_luminaire_11.onOffStatus.hasValue = OnOffEnum.Off
ld.kitchenette_luminaire_11.onOffCommand.hasValue = OnOffEnum.Off

ld.kitchenette_luminaire_12.onOffStatus.hasValue = OnOffEnum.Off
ld.kitchenette_luminaire_12.onOffCommand.hasValue = OnOffEnum.Off

ed.openofficeNorth_luminaire_1_dimmer["dimmer_command"].set_value(50.5)

if __name__ == "__main__":
    dump()
