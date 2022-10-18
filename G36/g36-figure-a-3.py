"""
Figure A-3 | Parallel Fan-Powered Terminal Unit, Constant Volume Fan
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
    QUANTITYKIND,
    UNIT,
    Equipment,
    PropertyReference,
    System,
    bind_model_namespace,
    dump,
)
from bob.equipments.architectural import Window
from bob.equipments.electricity.starter import MotorStarter
from bob.equipments.hvac.actuator import ElectricalProportionalActuator
from bob.equipments.hvac.coil import HotWaterCoil
from bob.equipments.hvac.damper import ElectricalActuatedProportionalDamper
from bob.equipments.hvac.fan import Fan
from bob.equipments.hvac.gas import GasMonitor
from bob.equipments.hvac.stats import NetworkRoomSensor, NetworkThermostat
from bob.equipments.hvac.valve import TwoWayActuatedProportionalValve
from bob.functions import (
    AnalogInput,
    AnalogOutput,
    BinaryInput,
    BinaryOutput,
    FunctionBlock,
)
from bob.functions.g36 import G36Sequence
from bob.functions.occupancy import OccupancyFunction
from bob.properties import Flow, PercentCommand, Temperature, temperature
from bob.properties.states import OccupancyStatus, OnOffCommand, OnOffStatus
from bob.properties.volume import Gallons
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.motion import IntrusionSensor, OccupancySensor
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
                0, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, unit=UNIT.PPM
            ),
            "hasMaxRange": QuantifiableObservableProperty(
                2000, hasQuantityKind=QUANTITYKIND.DimensionlessRatio, unit=UNIT.PPM
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
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": UNIT.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {"unit": UNIT.DEG_C},
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
    "equipments": {("actuator", ElectricalProportionalActuator): {}},
}

vav_system_template = {
    "params": {
        "label": "VAV_FIG.A2",
        "comment": "VAV with Airflow + Damper + Dual Duct",
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {"unit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "unit": UNIT.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-OCC-SENSOR", OccupancySensor): {},
        ("ZN-WINDOW-SWITCH", IntrusionSensor): {},
    },
    "properties": {
        ("zoneTemperature", Temperature): {"unit": UNIT.DEG_C},
        ("supplyAirTemperature", Temperature): {"unit": UNIT.DEG_C},
        ("occupancy", OccupancyStatus): {},
        ("damperPosition", PercentCommand): {},
        ("valvePosition", PercentCommand): {},
        ("airFlow", Flow): {"unit": UNIT.L_PER_SEC},
        ("fanStatus", OnOffStatus): {},
        ("fanCommand", OnOffCommand): {},
    },
    "equipments": {
        ("ZONE-THERMOSTAT", NetworkRoomSensor): {"config": Thermostat_template},
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box Damper with electrical actuator"
        },
        ("ZN-CO2", GasMonitor): {
            "config": co2Sensor_template,
            "comment": "CO2 of space",
        },
        ("HTG-COIL", HotWaterCoil): {"comment": "Hot Water Coil"},
        ("HTG-VLV", TwoWayActuatedProportionalValve): {"config": valve2w_template},
        ("FAN", Fan): {"electricalInlet": Electricity_120V_60HzInletConnectionPoint},
        ("FAN-STARTER", MotorStarter): {
            "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
            "electricalOutlet": Electricity_120V_60HzOutletConnectionPoint,
        },
    },
}


class VAV_FIGA3(System):
    """
    This is a clone of VAV found in from bob.equipments.hvac.vav VAV_Simple
    """

    supplyAirInlet: AirInletSystemConnectionPoint
    plenumAirInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.supplyAirInlet.mapsTo = self["DPR"].airInlet
        self.plenumAirInlet.mapsTo = self["HTG-COIL"].airInlet
        self.airOutlet.mapsTo = self["DPR"].airOutlet

        self.airFlow = self["SA-F"].observesProperty
        self.zoneTemperature = self["ZONE-THERMOSTAT"][
            "temperature_sensor"
        ].observesProperty
        self.supplyAirTemperature = self["DA-T"].observesProperty
        self.damperPosition = self["DPR"]["actuator"].command
        self.valvePosition = self["HTG-VLV"]["actuator"].command
        self.fanStatus = self["FAN-STARTER"].onOffStatus
        self.fanCommand = self["FAN-STARTER"].onOffCommand

        self["SA-F"].hasMeasurementLocation = self["DPR"].airInlet


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
vav = VAV_FIGA3(config=vav_system_template)
supply_air >> vav["DPR"] >> discharge_air
plenum >> vav["HTG-COIL"].airInlet
vav["HTG-COIL"] >> vav["FAN"] >> discharge_air >> hvac_space.ductAirInlet
vav["FAN-STARTER"] >> vav["FAN"]
hws >> vav["HTG-COIL"]
vav["HTG-COIL"] >> vav["HTG-VLV"] >> hwr

vav["ZONE-THERMOSTAT"]["temperature_sensor"].hasMeasurementLocation = hvac_space
vav["ZN-CO2"]["CO2"].hasMeasurementLocation = hvac_space
vav["ZN-WINDOW-SWITCH"].hasMeasurementLocation = window
vav["ZN-OCC-SENSOR"].hasMeasurementLocation = hvac_space
vav["DA-T"].hasMeasurementLocation = discharge_air

# Not sure if it's really required...but I think readings should be in space
hvac_space.temperature = vav["ZONE-THERMOSTAT"]["temperature_sensor"].observesProperty
hvac_space.co2 = vav["ZN-CO2"]["CO2"].observesProperty
hvac_space.window_switch = vav["ZN-WINDOW-SWITCH"].observesProperty

# Now that space is full of Equipments and connections...
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
occupancy = OccupancyFunction(
    label="OccControl",
    comment="This define occupancy for the zone. The occupancy sensor or the local override on the thermostat will turn the occupancy -> OCCUPIED",
)
occupancy.uses(vav["ZN-OCC-SENSOR"].observesProperty, BinaryInput, "occupancy-sensor")
occupancy.uses(
    vav["ZONE-THERMOSTAT"]["local_override"].observesProperty,
    BinaryInput,
    "local-override",
)
occupancy.hasOccupancyStatus = OccupancyStatus()
occupancy.produces(occupancy.hasOccupancyStatus)
occupancy.produces(hvac_space.occupancy)


# TODO : Complete
sequence = "Lorem ipsum of sequence"

# g36fig_a_3 = G36_FigA3(label="G36_FIG_A_3", comment=sequence)
# g36fig_a_2 = G36_FigA2(label="G36_FIG_A_2", comment=sequence)
g36fig_a_3 = FunctionBlock(label="G36_FIG_A_1", comment=sequence)
# zoneSetpointAdj = AnalogInput(label='Zone Setpoint Adjust', function_block=g36fig_a_3)
# LocalOverride = BinaryInput(label='Local Override', function_block=g36fig_a_3)
# zoneTemp = AnalogInput(label='Zone Temp', function_block=g36fig_a_3)
# zoneCO2 = AnalogInput(label='Zone CO2', function_block=g36fig_a_3)
# zonewindowSwitch = BinaryInput(label='Zone Window Switch', function_block=g36fig_a_3)
# zoneOccupancySensor = BinaryInput(label='Zone Occupancy Sensor', function_block=g36fig_a_3)

g36fig_a_3.uses(vav.airFlow, AnalogInput, "supplyAirFlow")
g36fig_a_3.uses(hvac_zone.temperature_setpoint, AnalogInput, "zoneTemperatureSetpoint")
g36fig_a_3.uses(hvac_zone.temperature, AnalogInput, "zoneTemperature")
g36fig_a_3.uses(vav["supplyAirTemperature"], AnalogInput, "supplyAirTemprature")
g36fig_a_3.uses(hvac_zone.co2, AnalogInput, "zoneCO2")
g36fig_a_3.uses(hvac_zone.windows_switch, BinaryInput, "window-switch")
g36fig_a_3.uses(vav["fanStatus"], BinaryInput, "fanStatus")
g36fig_a_3.uses(occupancy.hasOccupancyStatus, BinaryInput, "occupancy-status")
g36fig_a_3.produces(vav["damperPosition"], AnalogOutput, "damperPosition")
g36fig_a_3.produces(vav["valvePosition"], AnalogOutput, "valvePosition")
g36fig_a_3.produces(vav["fanCommand"], BinaryOutput, "fanCommand")

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
