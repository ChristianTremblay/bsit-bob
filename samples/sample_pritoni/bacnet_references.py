from rdflib import URIRef
from bob.externalreference.bacnet import BACnetDevice, BACnetReference
import lighting_devices as ld
import hvac_devices as hd


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

hd.vav1["VAV1_ZN-T"].measure @ zn1_t
hd.vav2["VAV2_ZN-T"].measure @ zn2_t
# A bulb with only one object
ld.openofficeEast_luminaire_1.brightnessRatio @ BACnetReference(
    uri=URIRef("bacnet://2/analog-input,1")
)
ld.openofficeEast_luminaire_1.hasOnOffStatus @ BACnetReference(
    uri=URIRef("bacnet://2/binary-input,1")
)
