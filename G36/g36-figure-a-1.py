"""
Figure A-1 | VAV Terminal Unit with Reheat
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
from bob.enum import AnalogSignalTypeEnum

from header import g36_header

from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from bob.connections.electricity import (
    Electricity_24V_60HzInletConnectionPoint,
    RS485BidirectionalConnectionPoint,
)
from bob.core import (
    G36,
    QUANTITYKIND,
    UNIT,
    Device,
    PropertyReference,
    System,
    bind_model_namespace,
    dump,
)
from bob.devices.architectural import Window
from bob.devices.control import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput
from bob.devices.control.controller import Controller
from bob.devices.hvac.damper import ElectricalActuatedProportionalDamper
from bob.devices.hvac.gas import GasMonitor
from bob.devices.hvac.stats import NetworkRoomSensor, NetworkThermostat
from bob.functions import (
    FunctionBlock,
    G36AnalogInput,
    G36AnalogOutput,
    G36BinaryInput,
    G36BinaryOutput,
)
from bob.functions.g36 import G36Figure_A_1, G36Sequence
from bob.functions.occupancy import OccupancyFunction
from bob.properties import Flow, PercentCommand, Temperature, temperature
from bob.properties.states import OccupancyStatus
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.light import IntrusionSensor, OccupancySensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.space.hvac import HVACSpace, HVACZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3601", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

controller_template = {
    "cp": {
        "electricalInlet": Electricity_24V_60HzInletConnectionPoint,
        "zone_temperature_sensor": AnalogInput,
        "zone_co2_sensor": AnalogInput,
        "airflow_sensor": AnalogInput,
        "window_switch": BinaryInput,
        "occupancy_sensor": BinaryInput,
        "damper_output": AnalogOutput,
        "bacnet_mstp": RS485BidirectionalConnectionPoint,
    },
    "properties": {("occupancy", FunctionBlock): {}, ("g36_figa1", FunctionBlock): {}},
}

controller = Controller(label="Controller for G36 Fig A-1", config=controller_template)

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


vav_system_template = {
    "params": {"label": "VAV_FIG.A1", "comment": "VAV with Airflow + Damper"},
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
        ("damperPosition", PercentCommand): {},
        ("airFlow", Flow): {"unit": UNIT["L-PER-SEC"]},
    },
    "devices": {
        ("ZONE-THERMOSTAT", NetworkRoomSensor): {"config": Thermostat_template},
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box Damper with electrical actuator"
        },
        ("ZN-CO2", GasMonitor): {
            "config": co2Sensor_template,
            "comment": "CO2 of space",
        },
    },
}


class VAV_FIGA1(System):
    """
    This is a clone of VAV found in bob.system.hvac.vav VAV_Simple
    """

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    occupancyStatus: PropertyReference

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"].airInlet
        self.airOutlet.mapsTo = self["DPR"].airOutlet

        self.airFlow = self["SA-F"].observesProperty
        self["zoneTemperature"].mapsTo = self["ZONE-THERMOSTAT"][
            "temperature_sensor"
        ].observesProperty
        self["damperPosition"].mapsTo = self["DPR"]["position"]

        self["SA-F"].hasMeasurementLocation = self["DPR"].airInlet
        self["DA-T"].hasMeasurementLocation = self["DPR"].airOutlet


supply_air = AirConnection(label="SA_In", comment="Supply Air for VAV")
discharge_air = AirConnection(label="SA_Out", comment="Supply Air from VAV")
hvac_space = HVACSpace(label="space", comment="Where sensors TS, CO2, WS and OCC are")
# We'll need this property
hvac_space.occupancy = OccupancyStatus()

window = Window(label="Window")
window.indoor >> hvac_space.windows
vav = VAV_FIGA1(config=vav_system_template)
supply_air >> vav["DPR"].airInlet

vav["DPR"].airOutlet >> discharge_air >> hvac_space.ductAirInlet
vav["DPR"]["actuator"].proportional_signal << controller.damper_output
vav["DPR"]["actuator"].proportional_signal.hasSignalType = AnalogSignalTypeEnum.VDC_0_10
vav["ZONE-THERMOSTAT"]["temperature_sensor"].hasMeasurementLocation = hvac_space
vav["ZONE-THERMOSTAT"].mstp << controller.bacnet_mstp
vav["ZN-CO2"]["CO2"].hasMeasurementLocation = hvac_space
# vav['ZN-CO2'] << controller.zone_co2_sensor
vav["ZN-WINDOW-SWITCH"].hasMeasurementLocation = window
vav["ZN-WINDOW-SWITCH"].onoff_contact >> controller.window_switch
vav["ZN-OCC-SENSOR"].hasMeasurementLocation = hvac_space
# vav['ZN-OCC-SENSOR'] << controller['occupancy_sensor'] not ready yet

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
occupancy = OccupancyFunction(
    label="OccControl",
    comment="This define occupancy for the zone. The occupancy sensor or the local override on the thermostat will turn the occupancy -> OCCUPIED",
)
occupancy.uses(
    vav["ZN-OCC-SENSOR"].observesProperty, G36BinaryInput, "occupancy-sensor"
)
occupancy.uses(
    vav["ZONE-THERMOSTAT"]["local_override"].observesProperty,
    G36BinaryInput,
    "local-override",
)
occupancy.hasOccupancyStatus = OccupancyStatus()
# Here, no need to specify G36AnalogOutput, or other... it is just a FunctionOutput
occupancy.produces(occupancy.hasOccupancyStatus)
occupancy.produces(hvac_space.occupancy)

# TODO : Complete
sequence = "Lorem ipsum of sequence"

g36fig_a_1 = FunctionBlock(label="G36_FIG_A_1", comment=sequence)

# uses will create a connector node named supplyAirFlow and connect it to property
# G36AnalogInput refer to the notion of AI in the context of G36
# We could have used FunctionInput or FunctionOutput
g36fig_a_1.uses(vav.airFlow, G36AnalogInput, "supplyAirFlow")
g36fig_a_1.uses(
    hvac_zone.temperature_setpoint, G36AnalogInput, "zoneTemperatureSetpoint"
)
g36fig_a_1.uses(hvac_zone.temperature, G36AnalogInput, "zoneTemperature")
g36fig_a_1.uses(hvac_zone.co2, G36AnalogInput, "zoneTemperature")
g36fig_a_1.uses(hvac_zone.windows_switch, G36BinaryInput, "window-switch")
g36fig_a_1.produces(
    vav["DPR"]["actuator"]["command"], G36AnalogOutput, "damperPosition"
)

# controller executes
controller >> occupancy
controller >> g36fig_a_1

# relationship between a FB output and a Controller output
g36fig_a_1.damperPosition >> controller.damper_output

controller.damper_output.hasSignalType = AnalogSignalTypeEnum.VDC_0_10

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
