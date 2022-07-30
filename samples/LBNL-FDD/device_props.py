from __future__ import annotations

from pathlib import Path
from typing import Any

from header import lbnl_header
from rdflib import URIRef

from bob.connections.air import (
    AirConnection,
    AirInletSystemConnectionPoint,
    AirOutletSystemConnectionPoint,
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from bob.core import Junction, System, bind_model_namespace, dump, QUANTITYKIND, UNIT
from bob.devices.hvac.damper import Damper
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.electricity.vfd import VFD
from bob.property import QuantifiableObservableProperty, Setpoint
from bob.sensor.flow import AirFlowSensor
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.pressure import AirDifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor, TemperatureSetpoint
from bob.systems.archives.coolingcoil import ChilledWaterCoil2
from bob.systems.archives.heatingcoil import HotWaterCoil2

# not sure of the difference between differential pressure and differential static pressure in this case


model_name = Path(__file__).stem
_namespace = ex = bind_model_namespace(
    "LBNL", f"http://data.ashrae.org/standard223/data/{model_name}#"
)

# Should have library of properties
class Percent_Rotational_Speed(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = (
        QUANTITYKIND.AngularFrequency
    )  # really don't know if this is right, just make it Speed?
    unit: URIRef = UNIT["PERCENT"]


class Electric_Power(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = QUANTITYKIND.ElectricPower
    unit: URIRef = UNIT["W"]


class Speed_Setpoint(Setpoint):
    hasQuantityKind: URIRef = QUANTITYKIND.ElectricPower
    unit: URIRef = UNIT["W"]


class DDAHU_Fan(Fan):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        properties = {
            "Electric_Power": Electric_Power,
            "Speed": Percent_Rotational_Speed,
        }
        vfd = VFD(label=self.label + ".fan_vfd", properties=properties)
        self > vfd
        speed_sp = Speed_Setpoint()
        vfd.hasSetpoint = speed_sp


fan = DDAHU_Fan(label="Test_Fan")

lbnl_header(model_name)
dump()
