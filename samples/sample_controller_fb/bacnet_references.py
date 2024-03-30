from pathlib import Path

# import functions as fn
import hvac_devices as hd
#import hvac_spaces as hs

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
from bob.core import bind_model_namespace, dump
from bob.externalreference.bacnet import BACnetExternalReference

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}/{model_name}/")


# VAV1 is defined as a BACnet device already, so we can fill the missing info here (keep BACnet related stuff here)
vav_controller = hd.vav1

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

hd.vav1["ZN-T"].observedProperty @ zone1_temp.presentValue
hd.vav1["DA-T"].observedProperty @ vav1_dat.presentValue
hd.vav1["DPR"].command @ damper_command.presentValue
hd.vav1["REHEAT"]["modulation"] @ heater_command.presentValue
hd.vav1["DPR"].position_feedback @ damper_feedback.presentValue
hd.vav1["supplyAirTemperature"] @ vav1_sat.presentValue
hd.vav1.airFlow @ vav1_flow.presentValue
#hs.zone1_hvac.temperature_setpoint @ zone1_temp_sp.presentValue


if __name__ == "__main__":
    dump()
