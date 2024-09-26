import logging
from pathlib import Path
from typing import Dict

from header import sample_header

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.electricity import Electricity_240VLL_1Ph_60HzInletConnectionPoint
from bob.core import (
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
from bob.enum import R410a
from bob.equipment.hvac.airhandlingunit import AirHandlingUnit
from bob.equipment.hvac.coil import Coil, HeatpumpCoil
from bob.equipment.hvac.compressor import RefrigeartionGasCompressor
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor
from bob.equipment.hvac.valve import ExpansionValve, ReversingValve

# Prototypes
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.sensor.temperature import AirTemperatureSensor
from bob.template import configure_relations, template_update

_log = logging.getLogger(__name__)

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")

VALIDATE = True

heatpump_template = {
    "params": {"label": "HeatPump", "comment": "Heatpump"},
    "sensors": {
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Discharge Air temperature after indoor coil",
        },
        ("RA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Return Air temperature (S2)",
        },
    },
    "equipment": {
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("OUTDOORUNITFAN", Fan): {
            "comment": "Outdoor Unit Fan",
            "electricalInlet": Electricity_240VLL_1Ph_60HzInletConnectionPoint,
        },
        ("INDOORCOIL", HeatpumpCoil): {"comment": "Indoor Coil"},
        ("OUTDOORCOIL", HeatpumpCoil): {"comment": "Outdoor coil"},
        ("COMPRESSOR", RefrigeartionGasCompressor): {"comment": "Compressor"},
        ("EXPANSIONVALVE", ExpansionValve): {"comment": "Expansion Valve"},
        ("REVERSINGVALVE", ReversingValve): {"comment": "Reversing Valve"},
        ("FILTER", Filter): {"comment": "Filter"},
    },
}


class AirToAirHeatPump(Equipment):
    """
    A heatpump with refrigeration cycle
    """

    _class_iri: URIRef = S223.HeatPump
    electricalInlet: Electricity_240VLL_1Ph_60HzInletConnectionPoint  # needs to be in a template so other templates can override it.
    airInlet: AirInletConnectionPoint  # return
    airOutlet: AirOutletConnectionPoint  # supply

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(heatpump_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Fan.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        # self["EXPANSIONVALVE"].set_gas_type(R410a)
        # self["REVERSINGVALVE"].set_gas_type(R410a)
        # self["COMPRESSOR"].set_gas_type(R410a)
        # self["INDOORCOIL"].set_gas_type(R410a)
        # self["OUTDOORCOIL"].set_gas_type(R410a)

        self["OUTDOORCOIL"] += Role.Condenser
        self["OUTDOORCOIL"] += Role.Evaporator
        self["INDOORCOIL"] += Role.Condenser
        self["INDOORCOIL"] += Role.Evaporator
        self["INDOORCOIL"] += Role.Cooling
        self["INDOORCOIL"] += Role.Heating

        (
            self["COMPRESSOR"].dischargePort
            >> self["REVERSINGVALVE"].refrigerantHighPressureInlet
        )
        (
            self["REVERSINGVALVE"].refrigerantLowPressureOutlet
            >> self["COMPRESSOR"].returnPort
        )
        self["REVERSINGVALVE"].refrigerantIndoorCoilPort >> self["INDOORCOIL"].gasPortB
        self["INDOORCOIL"].gasPortA >> self["EXPANSIONVALVE"].portB
        self["EXPANSIONVALVE"].portA >> self["OUTDOORCOIL"].gasPortA
        (
            self["OUTDOORCOIL"].gasPortB
            >> self["REVERSINGVALVE"].refrigerantOutdoorCoilPort
        )

        self["FILTER"].airInlet.mapsTo = self.airInlet
        self["FILTER"].airOutlet >> self["INDOORCOIL"].airInlet
        self["INDOORCOIL"].airOutlet >> self["SF"].airInlet
        self["SF"].airOutlet.mapsTo = self.airOutlet

        # takes air from outdoor
        # ambiant -> self['OUTDOORCOIL'].airInlet
        self["OUTDOORCOIL"].airOutlet >> self["OUTDOORUNITFAN"].airInlet
        # self['OUTDOORUNITFAN'].airOutlet -> ambiant
        # push air to outdoor

        self["DA-T"].hasObservationLocation = self.airOutlet
        self["RA-T"].hasObservationLocation = self.airInlet


hp = AirToAirHeatPump(config=heatpump_template)

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
