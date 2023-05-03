from pathlib import Path

import functions as fn
import hvac_devices as hd
import lighting_devices as ld
from rdflib import URIRef

from bob.core import bind_model_namespace, dump
from bob.bacnet import Device, DeviceObject, AnalogInputObject, AnalogValueObject, BinaryInputObject, BinaryOutputObject, ScheduleObject
from bob.externalreference.bacnet import BACnetReference

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


# An HVAC BACnet Device
CGM_2_004 = Device(
    label="CGM-2-004",
    comment="AHU Controller",
    # deviceId=5204,
    # deviceName="CGM-2-004",
    # networkNumber=2,
    # address=4,
    # vendorId=5,
)

CGM_2_004_device_object = DeviceObject(
    objectIdentifier="device,5204",
    objectName="CGM-2-004",
    vendorName="Unknown",
    vendorIdentifier=5,
)
CGM_2_004 > CGM_2_004_device_object

VAV_2_005 = Device(
    label="CVM-2-005",
    comment="VAV for Zone 1",
    # deviceId=5205,
    # deviceName="CVM-2-005",
    # networkNumber=2,
    # address=5,
    # vendorId=5,
)

VAV_2_005_device_object = DeviceObject(
    objectIdentifier="device,5205",
    objectName="CVM-2-005",
    vendorName="Unknown",
    vendorIdentifier=5,
)
VAV_2_005 > VAV_2_005_device_object


VAV_2_006 = Device(
    label="CVM-2-006",
    comment="VAV for Zone 2",
    # deviceId=5206,
    # deviceName="CVM-2-006",
    # networkNumber=2,
    # address=6,
    # vendorId=5,
)

VAV_2_006_device_object = DeviceObject(
    objectIdentifier="device,5206",
    objectName="CVM-2-006",
    vendorName="Unknown",
    vendorIdentifier=5,
)
VAV_2_006 > VAV_2_006_device_object


rat = AnalogInputObject(
    objectIdentifier="analog-input,1209",
    objectName="RA-T",
    description="Return Air Temeprature",
)
CGM_2_004 > rat

dat_avg = AnalogValueObject(
    objectIdentifier="analog-value,321",
    objectName="DAT-AVG",
    description="Discharge Air Temp Average",
)
CGM_2_004 > dat_avg


dat = AnalogInputObject(
    objectIdentifier="analog-input,1210",
    objectName="DA-T",
    description="Discharge Air Temperature",
)
CGM_2_004 > dat

zn1_t = AnalogInputObject(
    objectIdentifier="analog-input,1001",
    objectName="ZN1-T",
    description="Zone 1 Temperature",
)
VAV_2_005 > zn1_t

zn2_t = AnalogInputObject(
    objectIdentifier="analog-input,1002",
    objectName="ZN2-T",
    description="Zone 2 Temperature",
)
VAV_2_006 > zn2_t

rf_vfd_status = BinaryInputObject(
    objectIdentifier="binary-input,5021",
    objectName="RF-S",
    description="Return Fan Status from VFD drive running",
)
CGM_2_004 > rf_vfd_status

rf_vfd_cmd = BinaryOutputObject(
    objectIdentifier="binary-output,12345",
    objectName="RF-C",
    description="Return Fan Command from VFD run command",
)
CGM_2_004 > rf_vfd_cmd

pritoni_schedule = ScheduleObject(
    objectIdentifier="schedule,1",
    objectName="OCC-SCHEDULE",
    description="Building Occupancy Schedule",
)
CGM_2_004 > pritoni_schedule

hd.vav1["VAV1_ZN-T"].observedProperty @ zn1_t
hd.vav2["VAV2_ZN-T"].observedProperty @ zn2_t

hd.ahu["RF_VFD"]["drive_running"] @ rf_vfd_status
hd.ahu["RF_VFD"]["run_command"] @ rf_vfd_cmd

# A bulb with only one object
ld.openofficeNorth_luminaire_1.brightnessRatio @ BACnetReference(
    "bacnet://2/analog-input,1"
)
ld.openofficeNorth_luminaire_1.onOffStatus @ BACnetReference(
    "bacnet://2/binary-input,1"
)

fn.f_avg_temp @ dat_avg

fn.bathroom_occ_control_schedule @ pritoni_schedule
fn.corridor_occ_control_schedule @ pritoni_schedule
fn.kitchenette_occ_control_schedule @ pritoni_schedule
fn.open_office_occ_control_schedule @ pritoni_schedule
fn.private_office_occ_control_schedule @ pritoni_schedule

if __name__ == "__main__":
    dump()
