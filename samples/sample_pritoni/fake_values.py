from pathlib import Path

import functions as fn
import hvac_devices as hd
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

hd.vav1["VAV1_ZN-T"].observesProperty.hasValue = 20.3
hd.vav2["VAV2_ZN-T"].observesProperty.hasValue = 22.2


fn.open_office_occ_control.hasOccupancyStatus.hasValue = 1
fn.kitchenette_occ_control.hasOccupancyStatus.hasValue = 1
fn.private_office_occ_control.hasOccupancyStatus.hasValue = 0
fn.bathroom_occ_control.hasOccupancyStatus.hasValue = 0
fn.corridor_occ_control.hasOccupancyStatus.hasValue = 0

ld.openofficeEast_luminaire_1.onOffStatus.hasValue = 1
ld.openofficeEast_luminaire_1.onOffCommand.hasValue = 1

ld.openofficeEast_luminaire_2.onOffStatus.hasValue = 1
ld.openofficeEast_luminaire_2.onOffCommand.hasValue = 1

ld.openofficeWest_luminaire_3.onOffStatus.hasValue = 1
ld.openofficeWest_luminaire_3.onOffCommand.hasValue = 1

ld.openofficeWest_luminaire_4.onOffStatus.hasValue = 1
ld.openofficeWest_luminaire_4.onOffCommand.hasValue = 1

ld.bathroom_luminaire_5.onOffStatus.hasValue = 0
ld.bathroom_luminaire_5.onOffCommand.hasValue = 1

ld.bathroom_luminaire_6.onOffStatus.hasValue = 0
ld.bathroom_luminaire_6.onOffCommand.hasValue = 0

ld.privateoffice_luminaire_8.onOffStatus.hasValue = 0
ld.privateoffice_luminaire_8.onOffCommand.hasValue = 0

ld.privateoffice_luminaire_8.onOffStatus.hasValue = 0
ld.privateoffice_luminaire_8.onOffCommand.hasValue = 0

ld.corridor_luminaire_9.onOffStatus.hasValue = 0
ld.corridor_luminaire_9.onOffCommand.hasValue = 0

ld.corridor_luminaire_10.onOffStatus.hasValue = 1
ld.corridor_luminaire_10.onOffCommand.hasValue = 1

ld.kitchenette_luminaire_11.onOffStatus.hasValue = 1
ld.kitchenette_luminaire_11.onOffCommand.hasValue = 1

ld.kitchenette_luminaire_12.onOffStatus.hasValue = 1
ld.kitchenette_luminaire_12.onOffCommand.hasValue = 1

if __name__ == "__main__":
    dump()
