from ...sensor.pressure import DifferentialStaticPressureSensor
from ...sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from ...sensor.humidity import AirHumiditySensor

from ...connections.electricity import (
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
    RS485BidirectionalConnectionPoint,
)

from bob.core import s223, p223, Device, Property

__namespace__ = p223


class MechanicalOnOffThermostat(Device):
    """
    A mechanical thermostat have no network connection
    Outputs are turned on and off depending on the setpoint
    and the temperature read by the sensor inside the thermostat
    """

    sensor: AirTemperatureSensor
    heatingOutput: OnOffSignalOutletConnectionPoint
    coolingOutput: OnOffSignalOutletConnectionPoint
    fanOutput: OnOffSignalOutletConnectionPoint
    setpoint: TemperatureSetpoint


class MechanicalModulatingThermostat(Device):
    """
    A mechanical thermostat have no network connection
    This model is modulating so all output are modulation signals
    Outputs are controller depending on the setpoint
    and the temperature read by the sensor inside the thermostat
    """

    sensor: AirTemperatureSensor
    heatingOutput: ModulationSignalOutletConnectionPoint
    coolingOutput: ModulationSignalOutletConnectionPoint
    fanOutput: OnOffSignalOutletConnectionPoint
    setpoint: TemperatureSetpoint


class NetworkThermostat(Device):
    sensor: AirTemperatureSensor
    heatingOnOffOutput: OnOffSignalOutletConnectionPoint
    setpoint: TemperatureSetpoint
    mstp: RS485BidirectionalConnectionPoint


class NetworkRoomSensor(Device):
    sensor: AirTemperatureSensor
    setpoint: TemperatureSetpoint
    mstp: RS485BidirectionalConnectionPoint


# Pressure
class HighStaticPressureStat(Device):
    resetInput: Property  # mechanical switch button?
    highStaticPressureOutput: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        sensor = DifferentialStaticPressureSensor(label=f"{self.label}.sensor")
        self._sensors = [sensor]
        self > sensor


class FlowSwitch(Device):
    """
    A contact On Off controlled by static pressure in duct
    """

    flowOutput: OnOffSignalOutletConnectionPoint

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        sensor = DifferentialStaticPressureSensor(label=f"{self.label}.sensor")
        self._sensors = [sensor]
        self > sensor
