from pathlib import Path

import functions as fn
import hvac_devices as hd
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetDevice, BACnetReference

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


# An HVAC BACnet device
CGM_2_004 = BACnetDevice(
    label="CGM-2-004",
    comment="AHU Controller",
    deviceId=5204,
    deviceName="CGM-2-004",
    networkNumber=2,
    address=4,
    vendorId=5,
)

VAV_2_005 = BACnetDevice(
    label="CVM-2-005",
    comment="VAV for Zone 1",
    deviceId=5205,
    deviceName="CVM-2-005",
    networkNumber=2,
    address=5,
    vendorId=5,
)

VAV_2_006 = BACnetDevice(
    label="CVM-2-006",
    comment="VAV for Zone 2",
    deviceId=5206,
    deviceName="CVM-2-006",
    networkNumber=2,
    address=6,
    vendorId=5,
)

rat = BACnetReference(
    objectInstance=1209,
    objectOf=CGM_2_004,
    objectName="RA-T",
    description="Return Air Temeprature",
    objectType="analog-input",
)

dat_avg = BACnetReference(
    objectInstance=321,
    objectOf=CGM_2_004,
    objectName="DAT-AVG",
    description="Discharge Air Temp Average",
    objectType="analog-value",
)


dat = BACnetReference(
    objectInstance=1210,
    objectOf=CGM_2_004,
    objectName="DA-T",
    description="Discharge Air Temperature",
    objectType="analog-input",
)

zn1_t = BACnetReference(
    objectInstance=1002,
    objectOf=VAV_2_005,
    objectName="ZN1-T",
    description="Zone 1 Temperature",
    objectType="analog-input",
)

zn2_t = BACnetReference(
    objectInstance=1002,
    objectOf=VAV_2_006,
    objectName="ZN2-T",
    description="Zone 2 Temperature",
    objectType="analog-input",
)

rf_vfd_status = BACnetReference(
    objectInstance=5021,
    objectOf=CGM_2_004,
    objectName="RF-S",
    description="Return Fan Status from VFD drive running",
    objectType="binary-input",
)

rf_vfd_cmd = BACnetReference(
    objectInstance=12345,
    objectOf=CGM_2_004,
    objectName="RF-C",
    description="Return Fan Command from VFD run command",
    objectType="binary-output",
)

pritoni_schedule = BACnetReference(
    objectInstance=1,
    objectOf=CGM_2_004,
    objectName="OCC-SCHEDULE",
    description="Building Occupancy Schedule",
    objectType="schedule",
)

hd.vav1["VAV1_ZN-T"].observesProperty @ zn1_t
hd.vav2["VAV2_ZN-T"].observesProperty @ zn2_t

hd.ahu["RF-VFD"]["drive_running"] @ rf_vfd_status
hd.ahu["RF-VFD"]["run_command"] @ rf_vfd_cmd

# A bulb with only one object
ld.openofficeEast_luminaire_1.brightnessRatio @ BACnetReference(
    uri=URIRef("bacnet://2/analog-input,1")
)
ld.openofficeEast_luminaire_1.onOffStatus @ BACnetReference(
    uri=URIRef("bacnet://2/binary-input,1")
)

fn.f.avg_tmp @ dat_avg

fn.bathroom_occ_control.schedule @ pritoni_schedule
fn.corridor_occ_control.schedule @ pritoni_schedule
fn.kitchenette_occ_control.schedule @ pritoni_schedule
fn.open_office_occ_control.schedule @ pritoni_schedule
fn.private_office_occ_control.schedule @ pritoni_schedule

if __name__ == "__main__":
    dump()
