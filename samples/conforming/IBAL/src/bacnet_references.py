from pathlib import Path

# import functions as fn
import hvac_devices as hd
import hvac_spaces as hs

# import lighting_devices as ld
from rdflib import URIRef

from bob.bacnet import (
    AnalogInputObject,
    AnalogOutputObject,
    AnalogValueObject,
    BinaryInputObject,
    BinaryOutputObject,
    Device,
    DeviceObject,
    ScheduleObject,
)
from bob.connections.electricity import (
    Electricity_24VLN_1Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from bob.connections.network import RS485BidirectionalConnectionPoint
from bob.core import bind_model_namespace, dump
from bob.equipment.control.controller import (
    AnalogInput,
    AnalogOutput,
    BinaryInput,
    BinaryOutput,
)
from bob.externalreference.bacnet import BACnetExternalReference

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}:{model_name}/")

vav_controller_template_example = {
    "cp": {
        "electricalInlet": Electricity_24VLN_1Ph_60HzInletConnectionPoint,
        "bacnet_mstp": RS485BidirectionalConnectionPoint,
        # "zone_temperature_sensor": AnalogInput,
        # "airflow_sensor": AnalogInput,
        # "damper_output": AnalogOutput,
        "heating_command": AnalogOutput,
    },
    "properties": {},
}
ahu_controller_template_example = {
    "cp": {
        "electricalInlet": Electricity_24VLN_1Ph_60HzInletConnectionPoint,
        "bacnet_mstp": RS485BidirectionalConnectionPoint,
        "heating_command_request": AnalogInput,
    },
    "properties": {},
}

# An HVAC BACnet Device
vav_controller = Device(
    label="VAV_DEVICE_1111",
    comment="VAV Controller",
    config=vav_controller_template_example,
    # deviceId=5204,
    # deviceName="CGM-2-004",
    # networkNumber=2,
    # address=4,
    # vendorId=5,
)

vav_controller_device_object = DeviceObject(
    objectIdentifier="device,1111",
    objectName="VAV_1",
    vendorName="Servisys inc.",
    vendorIdentifier=842,
)
vav_controller > vav_controller_device_object

heater_command = AnalogOutputObject(
    objectIdentifier="analog-output,1",
    objectName="vav1_heat_c",
    description="VAV1 Heater Control Signal",
)
damper_command = AnalogOutputObject(
    objectIdentifier="analog-output,2",
    objectName="d15_pos_c",
    description="VAV1 Damper Control Signal",
)
damper_feedback = AnalogInputObject(
    objectIdentifier="analog-input,1",
    objectName="d15_pos_fb",
    description="VAV1 Damper Feedback Signal",
)
vav1_dat = AnalogInputObject(
    objectIdentifier="analog-input,2",
    objectName="vav1_out_rtd",
    description="VAV1 Discharge Temperature",
)
vav1_sat = AnalogInputObject(
    objectIdentifier="analog-input,3",
    objectName="vav1_t_in",
    description="VAV1 Supply Air Temperature",
)
vav1_flow = AnalogInputObject(
    objectIdentifier="analog-input,4",
    objectName="vav1_f",
    description="VAV1 Airflow Rate",
)
zone1_temp = AnalogInputObject(
    objectIdentifier="analog-input,5",
    objectName="zs1_out_rtd",
    description="Zone1 Temperature",
)
zone1_temp_sp = AnalogInputObject(
    objectIdentifier="analog-input,6",
    objectName="zs1_t_sp_f",
    description="Zone1 Temperature Setpoint",
)
vav_controller > heater_command
vav_controller > damper_command
vav_controller > damper_feedback
vav_controller > vav1_dat
vav_controller > vav1_sat
vav_controller > vav1_flow
vav_controller > zone1_temp
vav_controller > zone1_temp_sp


# An HVAC BACnet Device
ahu_controller = Device(
    label="IBAL AHU Controller",
    comment="VAV Controller",
    config=ahu_controller_template_example,
    # deviceId=5204,
    # deviceName="CGM-2-004",
    # networkNumber=2,
    # address=4,
    # vendorId=5,
)
vav1_heat_c_AI = AnalogInputObject(
    objectIdentifier="analog-input,1",
    objectName="vav1_heat_c_AI",
    description="Heating 0-10VDC command coming from VAV1 AO",
)
ahu_controller > vav1_heat_c_AI

# objects mapsTo connection points
heater_command >> vav_controller.heating_command
vav1_heat_c_AI >> ahu_controller.heating_command_request

hd.vav1["VAV1_ZN-T"].observedProperty @ zone1_temp.presentValue
hd.vav1["DA-T"].observedProperty @ vav1_dat.presentValue
hd.vav1["VAVController"]["command"] @ damper_command.presentValue
hd.vav1["REHEAT"]["modulation"] @ heater_command.presentValue
hd.vav1["VAVController"]["position_feedback"] @ damper_feedback.presentValue
# hd.vav1["supplyAirTemperature"] @ vav1_sat.presentValue
# hd.vav1.airFlow @ vav1_flow.presentValue
hs.zone1_hvac.temperature_setpoint @ zone1_temp_sp.presentValue

# 0-10V from AO is wired to AI of AHU Controller
vav_controller.heating_command >> ahu_controller.heating_command_request

if __name__ == "__main__":
    dump()
