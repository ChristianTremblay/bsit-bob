from pathlib import Path

import hvac_devices as hd
import occupancy as oc
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

hd.vav1["VAV1_ZN-T"].observesProperty.hasValue = 20.3
hd.vav2["VAV2_ZN-T"].observesProperty.add_value(22.2)


oc.open_office_occ_control.hasOccupancyStatus.hasValue = 1
oc.kitchenette_occ_control.hasOccupancyStatus.hasValue = 1
oc.private_office_occ_control.hasOccupancyStatus.hasValue = 0
oc.bathroom_occ_control.hasOccupancyStatus.hasValue = 0
oc.corridor_occ_control.hasOccupancyStatus.hasValue = 0


if __name__ == "__main__":
    dump()
