from pathlib import Path

import hvac_devices as hd
import functions as fn
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

hd.vav1["VAV1_ZN-T"].observesProperty.hasValue = 20.3
hd.vav2["VAV2_ZN-T"].observesProperty.add_value(22.2)


fn.open_office_occ_control.hasOccupancyStatus.hasValue = 1
fn.kitchenette_occ_control.hasOccupancyStatus.hasValue = 1
fn.private_office_occ_control.hasOccupancyStatus.hasValue = 0
fn.bathroom_occ_control.hasOccupancyStatus.hasValue = 0
fn.corridor_occ_control.hasOccupancyStatus.hasValue = 0

ld.openofficeEast_luminaire_1.hasOnOffStatus.hasValue = 1
ld.openofficeEast_luminaire_1.hasOnOffCommand.hasValue = 1

ld.openofficeEast_luminaire_2.hasOnOffStatus.hasValue = 1
ld.openofficeEast_luminaire_2.hasOnOffCommand.hasValue = 1

ld.openofficeWest_luminaire_3.hasOnOffStatus.hasValue = 1
ld.openofficeWest_luminaire_3.hasOnOffCommand.hasValue = 1

ld.openofficeWest_luminaire_4.hasOnOffStatus.hasValue = 1
ld.openofficeWest_luminaire_4.hasOnOffCommand.hasValue = 1

ld.bathroom_luminaire_5.hasOnOffStatus.hasValue = 0
ld.bathroom_luminaire_5.hasOnOffCommand.hasValue = 1

ld.bathroom_luminaire_6.hasOnOffStatus.hasValue = 0
ld.bathroom_luminaire_6.hasOnOffCommand.hasValue = 0

ld.privateoffice_luminaire_8.hasOnOffStatus.hasValue = 0
ld.privateoffice_luminaire_8.hasOnOffCommand.hasValue = 0

ld.privateoffice_luminaire_8.hasOnOffStatus.hasValue = 0
ld.privateoffice_luminaire_8.hasOnOffCommand.hasValue = 0

ld.corridor_luminaire_9.hasOnOffStatus.hasValue = 0
ld.corridor_luminaire_9.hasOnOffCommand.hasValue = 0

ld.corridor_luminaire_10.hasOnOffStatus.hasValue = 1
ld.corridor_luminaire_10.hasOnOffCommand.hasValue = 1

ld.kitchenette_luminaire_11.hasOnOffStatus.hasValue = 1
ld.kitchenette_luminaire_11.hasOnOffCommand.hasValue = 1

ld.kitchenette_luminaire_12.hasOnOffStatus.hasValue = 1
ld.kitchenette_luminaire_12.hasOnOffCommand.hasValue = 1

if __name__ == "__main__":
    dump()
