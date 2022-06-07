from pathlib import Path

import functions as fn
import hvac_devices as hd
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.enum import OccupancyEnum, OnOffEnum
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

hd.vav1["VAV1_ZN-T"].observesProperty.set_value(20.3)
hd.vav2["VAV2_ZN-T"].observesProperty.set_value(22.2)


fn.open_office_occ_control.hasOccupancyStatus.hasValue = OccupancyEnum.Occupied
fn.kitchenette_occ_control.hasOccupancyStatus.hasValue = OccupancyEnum.Occupied
fn.private_office_occ_control.hasOccupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.bathroom_occ_control.hasOccupancyStatus.hasValue = OccupancyEnum.Unoccupied
fn.corridor_occ_control.hasOccupancyStatus.hasValue = OccupancyEnum.Unoccupied

ld.openofficeEast_luminaire_1.onOffStatus.hasValue = OnOffEnum.On
ld.openofficeEast_luminaire_1.onOffCommand.hasValue = OnOffEnum.On

ld.openofficeEast_luminaire_2.onOffStatus.hasValue = OnOffEnum.On
ld.openofficeEast_luminaire_2.onOffCommand.hasValue = OnOffEnum.On

ld.openofficeWest_luminaire_3.onOffStatus.hasValue = OnOffEnum.On
ld.openofficeWest_luminaire_3.onOffCommand.hasValue = OnOffEnum.On

ld.openofficeWest_luminaire_4.onOffStatus.hasValue = OnOffEnum.On
ld.openofficeWest_luminaire_4.onOffCommand.hasValue = OnOffEnum.On

ld.bathroom_luminaire_5.onOffStatus.hasValue = OnOffEnum.Off
ld.bathroom_luminaire_5.onOffCommand.hasValue = OnOffEnum.On

ld.bathroom_luminaire_6.onOffStatus.hasValue = OnOffEnum.Off
ld.bathroom_luminaire_6.onOffCommand.hasValue = OnOffEnum.Off

ld.privateoffice_luminaire_8.onOffStatus.hasValue = OnOffEnum.Off
ld.privateoffice_luminaire_8.onOffCommand.hasValue = OnOffEnum.Off

ld.privateoffice_luminaire_8.onOffStatus.hasValue = OnOffEnum.Off
ld.privateoffice_luminaire_8.onOffCommand.hasValue = OnOffEnum.Off

ld.corridor_luminaire_9.onOffStatus.hasValue = OnOffEnum.Off
ld.corridor_luminaire_9.onOffCommand.hasValue = OnOffEnum.Off

ld.corridor_luminaire_10.onOffStatus.hasValue = OnOffEnum.On
ld.corridor_luminaire_10.onOffCommand.hasValue = OnOffEnum.On

ld.kitchenette_luminaire_11.onOffStatus.hasValue = OnOffEnum.On
ld.kitchenette_luminaire_11.onOffCommand.hasValue = OnOffEnum.On

ld.kitchenette_luminaire_12.onOffStatus.hasValue = OnOffEnum.On
ld.kitchenette_luminaire_12.onOffCommand.hasValue = OnOffEnum.On

if __name__ == "__main__":
    dump()
