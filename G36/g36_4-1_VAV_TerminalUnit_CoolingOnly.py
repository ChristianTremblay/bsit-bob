"""
g36_4-1_VAV_TerminalUnit_CoolingOnly
"""

from __future__ import annotations

from pathlib import Path

from header import g36_header

from bob.connections.air import (
    AirConnection,
)
from bob.connections.electricity import Electricity_24VLN_1Ph_60HzInletConnectionPoint
from bob.connections.network import RS485BidirectionalConnectionPoint
from bob.core import (
    QUANTITYKIND,
    UNIT,
    bind_model_namespace,
    dump,
)
from bob.enum import AnalogSignalTypeEnum
from bob.equipment.architectural import Window
from bob.equipment.control import AnalogInput, AnalogOutput, BinaryInput
from bob.equipment.control.controller import Controller

from bob.equipment.hvac.gas import GasMonitor
from bob.equipment.hvac.stats import NetworkRoomSensor

from bob.producer.g36 import G36VAVCoolingOnly
from bob.producer.occupancy import OccupancyFunction
from bob.properties.states import OccupancyStatus
from bob.property import QuantifiableObservableProperty
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.motion import OccupantMotionSensor
from bob.sensor.security import IntrusionSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.space.hvac import HVACSpace, HVACZone

# Prototypes
from bob.scratch.hvac.vav import VAV_Simple
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper

model_name = Path(__file__).stem
_namespace = bind_model_namespace(
    "exg3601", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

controller_template = {
    "cp": {
        "electricalInlet": Electricity_24VLN_1Ph_60HzInletConnectionPoint,
        "zone_temperature_sensor": AnalogInput,
        "zone_co2_sensor": AnalogInput,
        "airflow_sensor": AnalogInput,
        "window_switch": BinaryInput,
        "occupancy_sensor": BinaryInput,
        "damper_output": AnalogOutput,
        "bacnet_mstp": RS485BidirectionalConnectionPoint,
    },
    "properties": {},
}

controller = Controller(
    label="Controller for G36 VAV Cooling Only", config=controller_template
)

co2Sensor_template = {
    "params": {
        "label": "CO2",
        "comment": "CO2 Room Sensor",
    },
    "sensors": {
        ("CO2", CO2Sensor): {
            # external references need the whole URL
            # "hasExternalReference": "bacnet://",
            "hasMinRange": QuantifiableObservableProperty(
                0,
                hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                hasUnit=UNIT.PPM,
                label="Minimum Range",
            ),
            "hasMaxRange": QuantifiableObservableProperty(
                2000,
                hasQuantityKind=QUANTITYKIND.DimensionlessRatio,
                hasUnit=UNIT.PPM,
                label="Maximum Range",
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
    "properties": {
        ("temperature_setpoint", TemperatureSetpoint): {"hasUnit": UNIT.DEG_C}
    },
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {"hasUnit": UNIT.DEG_C},
        ("local_override", OccupantMotionSensor): {},
    },
}


vav_system_template = {
    "params": {"label": "VAV_CoolingOnly", "comment": "VAV with Airflow + Damper"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"hasUnit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-OCC-SENSOR", OccupantMotionSensor): {},
        ("ZN-WINDOW-SWITCH", IntrusionSensor): {},
    },
    "equipment": {
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

supply_air = AirConnection(label="SA_In", comment="Supply Air for VAV")
discharge_air = AirConnection(label="SA_Out", comment="Supply Air from VAV")
hvac_space = HVACSpace(label="space", comment="Where sensors TS, CO2, WS and OCC are")
# We'll need this property
hvac_space.occupancy = OccupancyStatus(label="Occupancy Status of Domain Space")

window = Window(label="Window")
window.indoor >> hvac_space.windows
vav = VAV_Simple(config=vav_system_template)

supply_air >> vav.airInlet
vav.airOutlet >> discharge_air >> hvac_space.ductAirInlet

vav["DPR"]["actuator"].proportional_signal << controller.damper_output
vav["DPR"]["actuator"].proportional_signal.hasSignalType = AnalogSignalTypeEnum.VDC_0_10
vav["ZONE-THERMOSTAT"]["temperature_sensor"] % hvac_space
vav["ZONE-THERMOSTAT"].mstp << controller.bacnet_mstp
vav["ZN-CO2"]["CO2"] % hvac_space
# vav['ZN-CO2'] << controller.zone_co2_sensor
# vav["ZN-WINDOW-SWITCH"] % window
####vav["ZN-WINDOW-SWITCH"].onoff_contact >> controller.window_switch
vav["ZN-OCC-SENSOR"] % hvac_space
# vav['ZN-OCC-SENSOR'] << controller['occupancy_sensor'] not ready yet

# Not sure if it's really required...but I think readings should be in space
hvac_space.temperature = vav["ZONE-THERMOSTAT"]["temperature_sensor"].observedProperty
hvac_space.co2 = vav["ZN-CO2"]["CO2"].observedProperty
hvac_space.window_switch = vav["ZN-WINDOW-SWITCH"].observedProperty

# Now that space is full of Equipment and connections...
# Zone are meant for control, let's define the control side of the thing
# temperature, co2, etc of zone.... could be the result of a function block
# making calculation from multiple hvac space readings...
# This will also make easier the relationship in G36Sequence later
hvac_zone = HVACZone(label="HVACZone", comment="Contains HVACSpace")
hvac_zone > hvac_space
# hvac_zone.airInlet.mapsTo = hvac_space.ductAirInlet
hvac_zone.temperature = hvac_space.temperature
hvac_zone.temperature_setpoint = vav["ZONE-THERMOSTAT"]["temperature_setpoint"]
hvac_zone.co2 = hvac_space.co2
hvac_zone.windows_switch = hvac_space.window_switch

# vav.serves_zone(hvac_zone)
hvac_zone.add_property(hvac_space.occupancy)

# Occupancy.... we need a function block
occupancy = OccupancyFunction(
    label="OccControl",
    comment="This define occupancy for the zone. The occupancy sensor or the local override on the thermostat will turn the occupancy -> OCCUPIED",
    inOccSensor=vav["ZN-OCC-SENSOR"].observedProperty,
    inLocalOverride=vav["ZONE-THERMOSTAT"]["local_override"].observedProperty,
    outStatus=hvac_space.occupancy,
)


# TODO : Complete
sequence = "Lorem ipsum of sequence"

# my_VAV_CoolingOnly_template['functions']['occupancyControl'] = occupancy
# my_VAV_CoolingOnly_template['cp']['boxDamperPosition'] = occupancy
g36fig_a_1 = G36VAVCoolingOnly(
    label="Bob G36 VAV Cooling Only",
    comment=sequence,
    supplyAirFlow=vav.airFlow,
    zoneTemperature=hvac_zone.temperature,
    zoneCO2=hvac_zone.co2,
    zonewindowSwitch=hvac_zone.windows_switch,
    boxDamperPosition=vav["DPR"]["actuator"]["command"],
    effectiveOccupancy=hvac_space.occupancy,
)

# uses will create a connector node named supplyAirFlow and connect it to property
# G36AnalogInput refer to the notion of AI in the context of G36
# We could have used FunctionInput or FunctionOutput
# controller executes
# controller >> occupancy
# controller >> g36fig_a_1
controller.damper_output.hasSignalType = AnalogSignalTypeEnum.VDC_0_10

dump(filename=f"G36/ttl/{model_name}.ttl", header=g36_header(model_name))
