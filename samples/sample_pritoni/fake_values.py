from pathlib import Path

import electrical_devices as ed
import functions as fn
import hvac_devices as hd
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.enum import OccupancyEnum, OnOffEnum
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

hd.vav1["VAV1_ZN-T"].observesProperty.set_value(69.7)  # PD-SR-MP HVACZone1Temperature
hd.vav2["VAV2_ZN-T"].observesProperty.set_value(73.2)  # PD-SR-MP HVACZone2Temperature
hd.vav1["VAV1_DA-T"].observesProperty.set_value(
    72.3
)  # PD-SR-MP VAV1 Outlet Temperature
hd.vav2["VAV2_DA-T"].observesProperty.set_value(
    71.2
)  # PD-SR-MP VAV2 Outlet Temperature
hd.ahu["DA-T"].observesProperty.set_value(70.2)  # PD-SR-MP VAV1&VAV2 Inlet Temperature

# hd.bathroom_exhaust_fan.onOffStatus = OnOffEnum.On
hd.ahu["RF-VFD"].drive_running = OnOffEnum.On
# hd.ahu['SF-STARTER']['SF-STARTER.sensor'].onOffStatus = OnOffEnum.On
hd.ahu["TPD3"].observesProperty.set_value(
    129.3
)  # !!! My TPD3 is static pressure...not flow

fn.open_office_occ_control.occupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.kitchenette_occ_control.occupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.private_office_occ_control.occupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.bathroom_occ_control.occupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.corridor_occ_control.occupancyStatus.hasValue = OccupancyEnum.Unoccupied

ld.openofficeEast_luminaire_1.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeEast_luminaire_1.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeEast_luminaire_2.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeEast_luminaire_2.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeWest_luminaire_3.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeWest_luminaire_3.onOffCommand.hasValue = OnOffEnum.Off

ld.openofficeWest_luminaire_4.onOffStatus.hasValue = OnOffEnum.Off
ld.openofficeWest_luminaire_4.onOffCommand.hasValue = OnOffEnum.Off

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

ed.openofficeEast_luminaire_1_dimmer["dimmer_command"].set_value(50.5)

if __name__ == "__main__":
    dump()
