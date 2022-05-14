"""
Figure A-2 | VAV Simple + Reheat Coil
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_120V_60HzConnection,
    Electricity_120V_60HzInletConnectionPoint,
    Electricity_120V_60HzOutletConnectionPoint,
    ModulationSignalInletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    RS485BidirectionalConnectionPoint,
)
from bob.connections.water import (
    HotWaterConnection,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from bob.core import (
    Device,
    Occupancy,
    PropertyReference,
    System,
    bind_model_namespace,
    dump,
    quantitykind,
    unit,
)
from bob.devices.architectural import Window
from bob.devices.electricity.starter import MotorStarter
from bob.devices.hvac.actuator import ElectricalActuator
from bob.devices.hvac.coil import HotWaterCoil
from bob.devices.hvac.damper import ElectricalActuatedDamper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.gas import GasMonitor
from bob.devices.hvac.stats import NetworkRoomSensor, NetworkThermostat
from bob.devices.hvac.valve import TwoWayActuatedValve
from bob.functions.g36 import AnalogIn, AnalogOut, BinaryIn, BinaryOut, G36Sequence
from bob.functions.occupancy import OccupancyControl
from bob.properties import Flow, PercentCommand, Temperature, temperature
from bob.properties.states import OccupancyStatus
from bob.properties.volume import Gallons
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.movement import IntrusionSensor, OccupancySensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3601", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

co2Sensor_template = {
    "params": {
        "label": "CO2",
        "comment": "CO2 Room Sensor",
    },
    "sensors": {
        ("CO2", CO2Sensor): {
            "hasExternalReference": "bacnet://",
            "hasMinRange": QuantifiableObservableProperty(
                0, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
            "hasMaxRange": QuantifiableObservableProperty(
                2000, hasQuantityKind=quantitykind.DimensionlessRatio, unit=unit.PPM
            ),
        }
    },
}

Thermostat_template = {
    "params": {
        "label": "ZONE-THERMOSTAT",
        "comment": "Zone Thermostat with setpoint adj and local override",
    },
    "cp": {"mstp": RS485BidirectionalConnectionPoint},
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": unit.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {"unit": unit.DEG_C},
        ("local_override", OccupancySensor): {},
    },
}

valve2w_template = {
    "cp": {
        "waterInlet": HotWaterInletConnectionPoint,
        "waterOutlet": HotWaterOutletConnectionPoint,
        "positionInlet": ModulationSignalInletConnectionPoint,
        "onOffInlet": OnOffSignalInletConnectionPoint,
    },
    "properties": {("flowCoefficient", Gallons): {}},
    "devices": {("actuator", ElectricalActuator): {}},
}

vav_system_template = {
    "params": {
        "label": "VAV_FIG.A2",
        "comment": "VAV with Airflow + Damper + Dual Duct",
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {"unit": unit.L_PER_SEC, "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-OCC-SENSOR", OccupancySensor): {},
        ("ZN-WINDOW-SWITCH", IntrusionSensor): {},
    },
    "properties": {
        ("occupancy", OccupancyStatus): {},
        ("zoneTemperature", Temperature): {"unit": unit.DEG_C},
        ("supplyAirTemperature", Temperature): {"unit": unit.DEG_C},
        ("damperPosition", PercentCommand): {},
        ("valvePosition", PercentCommand): {},
        ("airFlow", Flow): {"unit": unit.L_PER_SEC},
    },
    "devices": {
        ("ZONE-THERMOSTAT", NetworkRoomSensor): {"config": Thermostat_template},
        ("DPR", ElectricalActuatedDamper): {
            "comment": "VAV Box Damper with electrical actuator"
        },
        ("ZN-CO2", GasMonitor): {
            "config": co2Sensor_template,
            "comment": "CO2 of space",
        },
        ("HTG-COIL", HotWaterCoil): {"comment": "Hot Water Coil"},
        ("HTG-VLV", TwoWayActuatedValve): {"config": valve2w_template},
    },
}


class VAV_FIGA2(System):
    """
    This is a clone of VAV found in bob.system.hvac.vav VAV_Simple
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"].airInlet
        self.airOutlet.mapsTo = self["HTG-COIL"].airOutlet

        self.airFlow = self["SA-F"].observesProperty
        self.zoneTemperature = self["ZONE-THERMOSTAT"][
            "temperature_sensor"
        ].observesProperty
        self.supplyAirTemperature = self["DA-T"].observesProperty
        self.damperPosition = self["DPR"]["actuator"].position
        self.valvePosition = self["HTG-VLV"]["actuator"].position

        self["SA-F"].hasMeasurementLocation = self["DPR"].airInlet
        self["DA-T"].hasMeasurementLocation = self["HTG-COIL"].airOutlet


supply_air = AirConnection(label="SA_In", comment="Supply Air for VAV")
plenum = AirConnection(label="Plenum_In", comment="Plenum Air Returning to VAV")
discharge_air = AirConnection(label="SA_Out", comment="Supply Air from VAV")

hws = HotWaterConnection(label="HWS", comment="Hot Water Supply")
hwr = HotWaterConnection(label="HWR", comment="Hot Water Return")

hvac_space = HVACSpace(label="space", comment="Where sensors TS, CO2, WS and OCC are")
# We'll need this property
hvac_space.occupancy = OccupancyStatus()

window = Window(label="Window")
window.indoor >> hvac_space.windows
vav = VAV_FIGA2(config=vav_system_template)
supply_air >> vav["DPR"] >> vav["HTG-COIL"] >> discharge_air >> hvac_space.ductAirInlet
hws >> vav["HTG-COIL"]
vav["HTG-COIL"] >> vav["HTG-VLV"] >> hwr

vav["ZONE-THERMOSTAT"]["temperature_sensor"].hasMeasurementLocation = hvac_space
vav["ZN-CO2"]["CO2"].hasMeasurementLocation = hvac_space
vav["ZN-WINDOW-SWITCH"].hasMeasurementLocation = window
vav["ZN-OCC-SENSOR"].hasMeasurementLocation = hvac_space


# Not sure if it's really required...but I think readings should be in space
hvac_space.temperature = vav["ZONE-THERMOSTAT"]["temperature_sensor"].observesProperty
hvac_space.co2 = vav["ZN-CO2"]["CO2"].observesProperty
hvac_space.window_switch = vav["ZN-WINDOW-SWITCH"].observesProperty

# Now that space is full of devices and connections...
# Zone are meant for control, let's define the control side of the thing
# temperature, co2, etc of zone.... could be the result of a function block
# making calculation from multiple hvac space readings...
# This will also make easier the relationship in G36Sequence later
hvac_zone = HVACZone(label="HVACZone", comment="Contains HVACSpace")
hvac_zone > hvac_space
hvac_zone.airInlet.mapsTo = hvac_space.ductAirInlet
hvac_zone.temperature = hvac_space.temperature
hvac_zone.temperature_setpoint = vav["ZONE-THERMOSTAT"]["temperature_setpoint"]
hvac_zone.co2 = hvac_space.co2
hvac_zone.windows_switch = hvac_space.window_switch

# Occupancy.... we need a function block
occupancy = OccupancyControl(
    label="OccControl",
    comment="This define occupancy for the zone. The occupancy sensor or the local override on the thermostat will turn the occupancy -> OCCUPIED",
)
occupancy.uses_input(
    vav["ZN-OCC-SENSOR"].observesProperty, BinaryIn, "occupancy-sensor"
)
occupancy.uses_input(
    vav["ZONE-THERMOSTAT"]["local_override"].observesProperty,
    BinaryIn,
    "local-override",
)
occupancy.hasOccupancyStatus = OccupancyStatus()
occupancy.produces_output(occupancy.hasOccupancyStatus)
occupancy.produces_output(hvac_space.occupancy)
vav.occupancy = hvac_space.occupancy


class G36_FigA2(G36Sequence):
    zoneSetpointAdj: AnalogIn
    LocalOverride: BinaryIn
    zoneTemp: AnalogIn
    zoneCO2: AnalogIn
    zonewindowSwitch: BinaryIn
    zoneOccupancySensor: BinaryIn


# TODO : Complete
sequence = "Lorem ipsum of sequence"

g36fig_a_2 = G36_FigA2(label="G36_FIG_A_2", comment=sequence)
g36fig_a_2.uses_input(vav.airFlow, AnalogIn, "supplyAirFlow")
g36fig_a_2.uses_input(
    hvac_zone.temperature_setpoint, AnalogIn, "zoneTemperatureSetpoint"
)
g36fig_a_2.uses_input(hvac_zone.temperature, AnalogIn, "zoneTemperature")
g36fig_a_2.uses_input(vav["supplyAirTemperature"], AnalogIn, "supplyAirTemprature")
g36fig_a_2.uses_input(hvac_zone.co2, AnalogIn, "zoneCO2")
g36fig_a_2.uses_input(hvac_zone.windows_switch, BinaryIn, "window-switch")
g36fig_a_2.uses_input(occupancy.hasOccupancyStatus, BinaryIn, "occupancy-status")
g36fig_a_2.produces_output(vav["damperPosition"], AnalogOut, "damperPosition")
g36fig_a_2.produces_output(vav["valvePosition"], AnalogOut, "valvePosition")

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
