from pathlib import Path

from header import g36_header

from bob.connections.air import AirConnection
from bob.connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    EthernetBidirectionalConnectionPoint,
    EthernetBidirectionalSystemConnectionPoint,
    ModulationSignalInletConnectionPoint,
    ModulationSignalSystemConnectionPoint,
    OnOffSignalSystemInletConnectionPoint,
    OnOffSignalSystemOutletConnectionPoint,
    RS485BidirectionalSystemConnectionPoint,
)
from bob.connections.light import LightVisibleOutletSystemConnectionPoint
from bob.connections.water import (
    HotWaterConnection,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterConnection,
)
from bob.core import (
    BidirectionalSystemConnectionPoint,
    Node,
    System,
    bind_model_namespace,
    clear,
    connect_mm,
    contains_mm,
    dump,
)
from bob.devices.hvac.coil import HotWaterCoil
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.stats import HighStaticPressureStat
from bob.devices.hvac.valve import TwoWayValve
from bob.devices.electricity.vfd import VFD
from bob.externalreference.BACNET import BACnetDevice, BACnetReference
from bob.functions import InputConnector

# from bob.systems.hvac.g36 import AnalogIn, AnalogOut, BinaryIn, BinaryOut, G36Block
from bob.functions.g36 import AnalogIn, AnalogOut, BinaryIn, BinaryOut, G36Sequence
from bob.properties.ratio import Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.sensor.fire import SmokeDetectionSensor
from bob.sensor.pressure import AirDifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3611", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

fan_template = {
    "params": {
        "label": "Fan",
        "comment": "Fan driven by VFD",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
    },
    "sensors": {},
    "devices": {},
}

vfd_template = {
    "params": {
        "label": "VFD",
        "comment": "VFD for Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "drive_running": 0,
        "run_command": 0,
        "speed_reference": 0,
    },
    "sensors": {},
    "devices": {},
}


class HighStaticController(System):
    highPressureNO: OnOffSignalSystemInletConnectionPoint
    pushButton: OnOffSignalSystemInletConnectionPoint
    pilotLight: LightVisibleOutletSystemConnectionPoint
    enableVFD: OnOffSignalSystemOutletConnectionPoint
    resetInput: OnOffSignalSystemInletConnectionPoint


class VFDController(System):
    enable: OnOffSignalSystemInletConnectionPoint
    run: OnOffSignalSystemInletConnectionPoint
    speed: ModulationSignalSystemConnectionPoint
    status: OnOffSignalSystemOutletConnectionPoint
    mstp: BidirectionalSystemConnectionPoint
    bacnetIP: EthernetBidirectionalSystemConnectionPoint


class FIG_A_11(G36Sequence):
    # network: Node
    returnAirTemp: AnalogIn
    dischargeAirTemp: AnalogIn
    filterDiffPressure: AnalogIn
    ductStaticPressure: AnalogIn
    highStaticReset: BinaryIn
    fanStatus: BinaryIn
    fanStart: BinaryOut
    fanSpeed: AnalogOut


# HVAC Side
ra = AirConnection(label="ra", comment="Return air")
sa = AirConnection(label="sa", comment="Supply Air")
inside = AirConnection(label="INSIDE", comment="Needed to reference DPT")

filter = Filter(label="Filter")
hwc = HotWaterCoil(label="HC", comment="Hot Water Coil")

hw_valve = TwoWayValve(
    label="HWValve",
    comment="Hot Water Valve",
    waterInlet=HotWaterInletConnectionPoint,
    waterOutlet=HotWaterOutletConnectionPoint,
    hasPositionCommand=0,
)

f = Fan(config=fan_template)
vfd = VFD(config=vfd_template)

hws = HotWaterConnection(label="HWS", comment="Hot Water Supply")
hwr = HotWaterConnection(label="HWR", comment="Hot Water Return")

# Sensors
rat = AirTemperatureSensor(
    label="TS1",
    comment="Return Air Temperature sensor",
)
dpt1 = AirDifferentialStaticPressureSensor(
    label="DPT1", comment="Filter differential Pressure sensor"
)
dps = HighStaticPressureStat(label="DPS", comment="High Static Pressure Stat")


sd = SmokeDetectionSensor(label="SD", comment="Smoke Detector in discharge air")
dat = AirTemperatureSensor(label="TS2", comment="Supply Air Temperature sensor")
dpt2 = AirDifferentialStaticPressureSensor(
    label="DPT2", comment="Duct Static Pressure sensor"
)

# BACnet Stuff
dps["DPS.sensor"] @ BACnetReference("bacnet://2/binary-output,1")
rat @ BACnetReference("bacnet://2/analog-input,1")
dat @ BACnetReference("bacnet://2/analog-input,2")
dpt1 @ BACnetReference("bacnet://2/analog-input,3")
dpt2 @ BACnetReference("bacnet://2/analog-input,4")


high_static = HighStaticController(
    label="SFHIGHSTATIC",
    comment="This system is the abstraction of control relay, push buttons and pilot light that are triggered by a high static pressure reading after the fan. The push button is the manual reset.",
)
high_static > dps


vfd_controller = VFDController(
    label="VFDController",
    comment="This is the abstraction of the VFD Controller that interact with other systems like DDC controlers and other controllers. Each property is related to something in the device itself.",
)
vfd_bacnet = BACnetDevice(
    label="VFDBACNET",
    comment="BACnet controller of VFD",
    deviceId=5206,
    deviceName="VFD",
    networkNumber=2,
    address=6,
    vendorId=5,
)

# Connections

vfd.electricalOutlet >> f.electricalInlet
# Air
ra >> filter >> hwc >> f >> sa

# Water
hws >> hwc.hotWaterInlet
hwc.hotWaterOutlet >> hw_valve >> hwr

# Sensors
rat.hasMeasurementLocation = ra
dpt1.hasMeasurementLocationHigh = filter.airInlet
dpt1.hasMeasurementLocationLow = filter.airOutlet

dps["DPS.sensor"].hasMeasurementLocationHigh = f.airOutlet
dps["DPS.sensor"].hasMeasurementLocationLow = inside
sd.hasMeasurementLocation = f.airOutlet
dat.hasMeasurementLocation = f.airOutlet

dpt2.hasMeasurementLocationHigh = sa
dpt2.hasMeasurementLocationLow = inside

# Map Systems
a11 = FIG_A_11(
    label="Figure-a-11",
    comment="This is a simple Fan Coil / Variable Volume. This system shows a fan controlled by a VFD to control static pressure in the supply air duct. The VFD will be disable on smoke detection, preventing the fan from running in case of fire. A high presure sensor will also disable the VFD and prevent the drive from running. In the latter case, a manual reset will be needed to authorize the VFD to restart. Supply air temeprature is maintained at setpoint by modulating a hot water valve (air pass through a hot water coil, before the fan). The discharge air temperature setpoint is calculated between limits to satisfied the demand created to maintain return air temeprature to setpoint.",
)

high_static.highPressureNO.mapsTo = dps.highStaticPressureOutput
high_static.enableVFD.mapsTo = vfd_controller.enable

# vfd > vfd_controller  ###TODO: devices cannot contain systems

a11.uses_input(rat.observesProperty)
a11.uses_input(dat.observesProperty)
# a11.uses_input(high_static.resetInput)
a11.uses_input(dpt1.observesProperty)
a11.produces_output(hw_valve.hasPositionCommand)
a11.uses_input(vfd.drive_running)
a11.produces_output(vfd.run_command)
a11.produces_output(vfd.speed_reference)
a11.uses_input(dpt2.observesProperty)
# a11.network.uses_input(vfd_controller.mstp) Is Network part of the G36 requirement ? Should this be there ?

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
