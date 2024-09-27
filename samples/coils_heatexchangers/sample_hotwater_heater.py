import logging
from pathlib import Path
from typing import Any, Dict

from header import sample_header

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.electricity import (
    ElectricalInletConnectionPoint,
    Electricity_240VLL_1Ph_60HzInletConnectionPoint,
)
from bob.connections.liquid import (
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterBidirectionalConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from bob.connections.naturalgas import NaturalGasInletConnectionPoint
from bob.core import (
    BOB,
    P223,
    S223,
    UNIT,
    Equipment,
    Role,
    URIRef,
    bind_model_namespace,
    data_graph,
    dump,
    schema_graph,
)
from bob.enum import DomesticHotWater, DomesticWater, Role
from bob.equipment.hvac.boiler import DomesticElectricalWaterHeater
from bob.equipment.hvac.coil import HeatpumpCoil, ImmersedResistanceHeaterElement
from bob.equipment.hvac.compressor import RefrigeartionGasCompressor
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.valve import ExpansionValve, ReversingValve
from bob.functions import Function, FunctionInput, FunctionOutput
from bob.template import template_update

_log = logging.getLogger(__name__)

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

VALIDATE = True

domesticwaterheater_template = {
    "cp": {"electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint},
}


class InsideTankHeatTransfer(Function):
    """ """

    _class_iri = BOB.InsideTankHeatTransfer

    waterFlow: FunctionInput
    resistanceHeaterPower1: FunctionInput
    resistanceHeaterModulation1: FunctionInput
    resistanceHeaterCommand1: FunctionInput
    resistanceHeaterPower2: FunctionInput
    resistanceHeaterModulation2: FunctionInput
    resistanceHeaterCommand2: FunctionInput
    leavingWaterTemp: FunctionOutput
    fluidTemp: FunctionOutput


class MyDomesticElectricalWaterHeater(DomesticElectricalWaterHeater):
    _class_iri = P223.DomesticHeatPumpWaterHeater

    def __init__(self, config: Dict = domesticwaterheater_template, **kwargs):
        _config = template_update({}, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)

        # Relate the temperature of the surface of the condenser coil and the water flow in the tank to the temperature of the water leaving the tank
        heat_transfer = InsideTankHeatTransfer(
            label="Heat Transfer Function",
            waterFlow=self["fluidFlow"],
            resistanceHeaterPower1=self["element1"]["kW"],
            resistanceHeaterModulation1=self["element1"]["modulation"],
            resistanceHeaterCommand1=self["element1"]["onOffCommand"],
            resistanceHeaterPower2=self["element2"]["kW"],
            resistanceHeaterModulation2=self["element2"]["modulation"],
            resistanceHeaterCommand2=self["element2"]["onOffCommand"],
            leavingWaterTemp=self["leavingFluidTemperature"],
            fluidTemp=self["tank"]["fluidTemperature"],
        )


hpwh = MyDomesticElectricalWaterHeater(
    config=domesticwaterheater_template, label="Electric Water Heater"
)


_folder = "ttl/validation" if VALIDATE else "ttl"
dump(
    data_graph,
    filename=f"samples/{_folder}/{model_name}.data.ttl",
    header=sample_header(model_name, "data"),
)
dump(
    schema_graph,
    filename=f"samples/{_folder}/{model_name}.schema.ttl",
    header=sample_header(model_name, "schema"),
)
