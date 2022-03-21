from pathlib import Path
from bob.connections.air import AirConnection
from bob.connections.electricity import (
    OnOffSignalSystemInletConnectionPoint,
    OnOffSignalSystemOutletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    EthernetBidirectionalConnectionPoint,
    EthernetBidirectionalSystemConnectionPoint,
    ModulationSignalInletConnectionPoint,
    ModulationSignalSystemConnectionPoint,
    RS485BidirectionalSystemConnectionPoint,
)
from bob.connections.light import LightVisibleOutletSystemConnectionPoint
from bob.connections.water import HotWaterConnection, WaterConnection
from bob.core import BidirectionalSystemConnectionPoint, System, bind_model_namespace
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.vfd import VFD
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.coil import HotWaterCoil
from bob.devices.hvac.valve import HotWaterValve
from bob.devices.hvac.stats import HighStaticPressureStat
from bob.sensor.fire import SmokeDetectionSensor

from bob.sensor.pressure import DifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor

from bob.systems.hvac.g36 import G36Block, AnalogIn, AnalogOut, BinaryIn, BinaryOut

from bob.core import clear, dump

from header import g36_header

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(
    "exg3611", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

fan_template = {
    "params": {
        "label": "Fan",
        "comment": "Fan driven by VFD",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
    },
    "sensors": {},
    "contains": {},
}

vfd_template = {
    "params": {
        "label": "VFD",
        "comment": "VFD for Fan",
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
    },
    "sensors": {},
    "contains": {},
}


# HVAC Side
ra = AirConnection(label="ra", comment="Return air")
sa = AirConnection(label="sa", comment="Supply Air")
inside = AirConnection(label="INSIDE", comment="Needed to reference DPT")

filter = Filter(label="Filter")
hwc = HotWaterCoil(label="HC", comment="Hot Water Coil")

hw_valve = HotWaterValve(label="HWValve", comment="Hot Water Valve")

f = Fan(config=fan_template)
vfd = VFD(config=vfd_template)

hws = HotWaterConnection(label="HWS", comment="Hot Water Supply")
hwr = HotWaterConnection(label="HWR", comment="Hot Water Return")

# Sensors
rat = AirTemperatureSensor(
    label="TS1",
    comment="Return Air Temperature sensor",
)
dpt1 = DifferentialStaticPressureSensor(
    label="DPT1", comment="Filter differential Pressure sensor"
)
dps = HighStaticPressureStat(
    label="DPS", comment="High Static Pressure Stat"
)


sd = SmokeDetectionSensor(label="SD", comment="Smoke Detector in discharge air")
dat = AirTemperatureSensor(label="TS2", comment="Supply Air Temperature sensor")
dpt2 = DifferentialStaticPressureSensor(
    label="DPT2", comment="Duct Static Pressure sensor"
)

# BACnet Stuff
dps.sensor.measure.hasExternalReference = "bacnet://2/binary-output/1"
rat.measure.hasExternalReference = "bacnet://2/analog-input/1"
dat.measure.hasExternalReference = "bacnet://2/analog-input/2"
dpt1.measure.hasExternalReference = "bacnet://2/analog-input/3"
dpt2.measure.hasExternalReference = "bacnet://2/analog-input/4"

class HighStaticController(System):
    highPressureNO: OnOffSignalSystemInletConnectionPoint
    pushButton: OnOffSignalSystemInletConnectionPoint
    pilotLight: LightVisibleOutletSystemConnectionPoint
    enableVFD: OnOffSignalSystemOutletConnectionPoint
    resetInput: OnOffSignalSystemInletConnectionPoint


high_static = HighStaticController(
    label="SFHIGHSTATIC",
    comment="This system is the abstraction of control relay, push buttons and pilot light that are triggered by a high static pressure reading after the fan. The push button is the manual reset.",
)
high_static > dps

class VFDController(System):
    enable: OnOffSignalSystemInletConnectionPoint
    run: OnOffSignalSystemInletConnectionPoint
    speed: ModulationSignalSystemConnectionPoint
    status: OnOffSignalSystemOutletConnectionPoint
    mstp: BidirectionalSystemConnectionPoint
    bacnetIP: EthernetBidirectionalSystemConnectionPoint


vfd_controller = VFDController(
    label="VFDController",
    comment="This is the abstraction of the VFD Controller that interact with other systems like DDC controlers and other controllers. Each property is related to something in the device itself.",
)


# Connections
# Air
vfd >> f
ra >> filter >> hwc >> f >> sa
# Water
hws >> hwc.hotWaterInlet
hwc.hotWaterOutlet >> hw_valve >> hwr

# Sensors
rat.hasMeasurementLocation = ra
dpt1.hasMeasurementLocationHigh = filter.airInlet
dpt1.hasMeasurementLocationLow = filter.airOutlet

dps.sensor.hasMeasurementLocationHigh = f.airOutlet
dps.sensor.hasMeasurementLocationLow = inside
sd.hasMeasurementLocation = f.airOutlet
dat.hasMeasurementLocation = f.airOutlet

dpt2.hasMeasurementLocationHigh = sa
dpt2.hasMeasurementLocationLow = inside

# Map Systems


class FIG_A_11(G36Block):
    sf_high_static_reset: BinaryOut
    return_air_temp: AnalogIn
    filter_dp: AnalogIn
    hw_valve: AnalogOut
    sf_status: BinaryIn
    sf_speed: AnalogOut
    sf_start: BinaryOut
    supply_air_temp: AnalogIn
    duct_static_press: AnalogIn
    network: RS485BidirectionalSystemConnectionPoint


a11 = FIG_A_11(
    label="Figure-a-11",
    comment="This is a simple Fan Coil / Variable Volume. This system shows a fan controlled by a VFD to control static pressure in the supply air duct. The VFD will be disable on smoke detection, preventing the fan from running in case of fire. A high presure sensor will also disable the VFD and prevent the drive from running. In the latter case, a manual reset will be needed to authorize the VFD to restart. Supply air temeprature is maintained at setpoint by modulating a hot water valve (air pass through a hot water coil, before the fan). The discharge air temperature setpoint is calculated between limits to satisfied the demand created to maintain return air temeprature to setpoint.",
)

high_static.highPressureNO.mapsTo = dps.highStaticPressureOutput
high_static.enableVFD.mapsTo = vfd_controller.enable
vfd > vfd_controller

a11.return_air_temp.mapsTo = rat
a11.supply_air_temp.mapsTo = dat
a11.sf_high_static_reset.mapsTo = high_static.resetInput
a11.filter_dp.mapsTo = dpt1
a11.hw_valve.mapsTo = hw_valve
a11.sf_status.mapsTo = vfd_controller.status
a11.sf_start.mapsTo = vfd_controller.run
a11.sf_speed.mapsTo = vfd_controller.speed
a11.duct_static_press.mapsTo = dpt2
a11.network.mapsTo = vfd_controller.mstp

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
