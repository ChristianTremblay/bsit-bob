from typing import Dict

from rdflib import URIRef

from bob.core import Device, Property, PropertyReference, p223, s223, unit
from bob.properties.states import OnOffStatus

from ...connections.electricity import (
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
    OnOffSignalSystemConnectionPoint,
    RS485BidirectionalConnectionPoint,
)
from ...sensor.humidity import AirHumiditySensor
from ...sensor.pressure import AirDifferentialStaticPressureSensor
from ...sensor.temperature import AirTemperatureSensor, TemperatureSetpoint

_namespace = s223


class Thermostat(Device):
    node_type: URIRef = s223.Thermostat
    temperature: PropertyReference
    setpoint: PropertyReference
    differential: PropertyReference
    onOffCommand: PropertyReference


class Pressurestat(Device):
    node_type: URIRef = s223.Pressurestat
    pressure: PropertyReference
    setpoint: PropertyReference
    differential: PropertyReference
    onOffCommand: PropertyReference


class Humidistat(Device):
    node_type: URIRef = s223.Humidistat
    humidity: PropertyReference
    setpoint: PropertyReference
    differential: PropertyReference
    onOffCommand: PropertyReference


MechanicalOnOffThermostat_template = {
    "cp": {
        "mstp": RS485BidirectionalConnectionPoint,
        "heatingOutput": OnOffSignalOutletConnectionPoint,
        "coolingOutput": OnOffSignalOutletConnectionPoint,
        "fanOutput": OnOffSignalOutletConnectionPoint,
    },
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": unit.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {},
        ("humidity_sensor", AirHumiditySensor): {},
    },
}


class MechanicalOnOffThermostat(Thermostat):
    """
    A mechanical thermostat have no network connection
    Outputs are turned on and off depending on the setpoint
    and the temperature read by the sensor inside the thermostat
    """

    def __init__(self, config: Dict = MechanicalOnOffThermostat_template, **kwargs):
        config["properties"] = config.get(
            "properties", MechanicalOnOffThermostat_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


MechanicalModulatingThermostat_template = {
    "cp": {
        "mstp": RS485BidirectionalConnectionPoint,
        "heatingOutput": ModulationSignalOutletConnectionPoint,
        "coolingOutput": ModulationSignalOutletConnectionPoint,
        "fanOutput": OnOffSignalOutletConnectionPoint,
    },
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": unit.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {},
        ("humidity_sensor", AirHumiditySensor): {},
    },
}


class MechanicalModulatingThermostat(Thermostat):
    """
    A mechanical thermostat have no network connection
    This model is modulating so all output are modulation signals
    Outputs are controller depending on the setpoint
    and the temperature read by the sensor inside the thermostat
    """

    def __init__(
        self, config: Dict = MechanicalModulatingThermostat_template, **kwargs
    ):
        config["properties"] = config.get(
            "properties", MechanicalModulatingThermostat_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


NetworkThermostat_template = {
    "cp": {
        "mstp": RS485BidirectionalConnectionPoint,
        "heatingOutput": OnOffSignalOutletConnectionPoint,
        "coolingOutput": OnOffSignalOutletConnectionPoint,
    },
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": unit.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {"unit": unit.DEG_C},
        ("humidity_sensor", AirHumiditySensor): {},
    },
}


class NetworkThermostat(Thermostat):
    """
    A network thermostat has the ability to control loads
    direclty from outputs.
    ex. TEC3000
    """

    def __init__(self, config: Dict = NetworkThermostat_template, **kwargs):
        config["properties"] = config.get(
            "properties", NetworkThermostat_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


NetworkRoomSensor_template = {
    "cp": {"mstp": RS485BidirectionalConnectionPoint},
    "properties": {("temperature_setpoint", TemperatureSetpoint): {"unit": unit.DEG_C}},
    "sensors": {
        ("temperature_sensor", AirTemperatureSensor): {"unit": unit.DEG_C},
        ("humidity_sensor", AirHumiditySensor): {},
    },
}


class NetworkRoomSensor(Device):
    """
    A network Room Sensor tells information on the room and accept setpoints
    Will communicate thoses information by network.
    But no outputs to activate loads.
    """

    node_type: URIRef = s223.NetworkRoomSensor

    def __init__(self, config: Dict = NetworkRoomSensor_template, **kwargs):
        config["properties"] = config.get(
            "properties", NetworkRoomSensor_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


HighStaticPressureStat_template = {
    "cp": {
        "resetInput": OnOffSignalInletConnectionPoint,
        "signalOutput": OnOffSignalOutletConnectionPoint,
    },
    "properties": {("onOffStatus", OnOffStatus): {}},
    "sensors": {
        ("pressure_sensor", AirDifferentialStaticPressureSensor): {"unit": unit.PA}
    },
}

# Pressure
class HighStaticPressureStat(Pressurestat):
    def __init__(self, config: Dict = HighStaticPressureStat_template, **kwargs):
        config["properties"] = config.get(
            "properties", HighStaticPressureStat_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


flowswitch_template = {
    "cp": {"signalOutput": OnOffSignalOutletConnectionPoint},
    "properties": {("onOffStatus", OnOffStatus): {}},
    "sensors": {
        ("pressure_sensor", AirDifferentialStaticPressureSensor): {"unit": unit.PA}
    },
}


class FlowSwitch(Device):
    """
    A contact On Off controlled by static pressure in duct
    """

    node_type: URIRef = s223.Flowswitch

    def __init__(self, config: Dict = flowswitch_template, **kwargs):
        config["properties"] = config.get(
            "properties", flowswitch_template["properties"]
        )
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
