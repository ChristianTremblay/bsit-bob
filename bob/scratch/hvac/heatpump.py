from typing import Dict

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.electricity import Electricity_240VLL_1Ph_60HzInletConnectionPoint
from bob.core import (
    S223,
    SCRATCH,
    UNIT,
    BoundaryConnectionPoint,
    Equipment,
    Role,
    URIRef,
)
from bob import application
from bob.enum import R410a
from bob.equipment.hvac.coil import HeatpumpCoil
from bob.equipment.hvac.compressor import RefrigerationGasCompressor
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.valve import ExpansionValve, ReversingValve

# Prototypes
from bob.scratch.hvac.fan import Fan
from bob.sensor.temperature import AirTemperatureSensor
from bob.template import SystemFromTemplate, configure_relations, template_update

_namespace = SCRATCH

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
        ("COMPRESSOR", RefrigerationGasCompressor): {"comment": "Compressor"},
        ("EXPANSIONVALVE", ExpansionValve): {"comment": "Expansion Valve"},
        ("REVERSINGVALVE", ReversingValve): {"comment": "Reversing Valve"},
        ("FILTER", Filter): {"comment": "Filter"},
    },
}


class _AirToAirHeatPump(Equipment, application.AirToAirHeatPump):
    """
    A heatpump with refrigeration cycle
    Created as an s223:Equipment member of a s223:HeatPump system
    """

    _class_iri: URIRef = SCRATCH.AirToAirHeatPump
    electricalInlet: Electricity_240VLL_1Ph_60HzInletConnectionPoint  # needs to be in a template so other templates can override it.
    indoorAirInlet: AirInletConnectionPoint  # return
    indoorAirOutlet: AirOutletConnectionPoint  # supply
    outdoorAirInlet: AirInletConnectionPoint  # return
    outdoorAirOutlet: AirOutletConnectionPoint  # supply

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(heatpump_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)
        self["EXPANSIONVALVE"].set_gas_type(R410a)
        self["REVERSINGVALVE"].set_gas_type(R410a)
        self["COMPRESSOR"].set_gas_type(R410a)
        self["INDOORCOIL"].set_gas_type(R410a)
        self["OUTDOORCOIL"].set_gas_type(R410a)

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

        self["FILTER"].airInlet.mapsTo = self.indoorAirInlet
        self["FILTER"].airOutlet >> self["INDOORCOIL"].airInlet
        self["INDOORCOIL"].airOutlet >> self["SF"].airInlet
        self["SF"].airOutlet.mapsTo = self.indoorAirOutlet

        # takes air from outdoor
        # ambiant -> self['OUTDOORCOIL'].airInlet
        self["OUTDOORCOIL"].airOutlet >> self["OUTDOORUNITFAN"].airInlet
        self["OUTDOORCOIL"].airInlet.mapsTo = self.outdoorAirInlet
        self["OUTDOORUNITFAN"].airOutlet.mapsTo = self.outdoorAirOutlet
        # push air to outdoor

        self["DA-T"].hasObservationLocation = self.indoorAirOutlet
        self["RA-T"].hasObservationLocation = self.indoorAirInlet


scratch_system_template = {
    "params": {"label": "Air to Air Heat Pump", "comment": "Air to Air Heat Pump"},
    "equipment": {
        ("AirToAirHeatPump", _AirToAirHeatPump): {},
    },
    "relations": [
        ("self.indoorAirInlet", "=", "self['AirToAirHeatPump'].indoorAirInlet"),
        ("self.indoorAirOutlet", "=", "self['AirToAirHeatPump'].indoorAirOutlet"),
        ("self.outdoorAirInlet", "=", "self['AirToAirHeatPump'].outdoorAirInlet"),
        ("self.outdoorAirOutlet", "=", "self['AirToAirHeatPump'].outdoorAirOutlet"),
    ],
}


class AirToAirHeatPump(SystemFromTemplate, application.AirToAirHeatPump):
    _class_iri = SCRATCH.AirSourceHeatPump
    indoorAirInlet: BoundaryConnectionPoint
    indoorAirOutlet: BoundaryConnectionPoint
    outdoorAirInlet: BoundaryConnectionPoint
    outdoorAirOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = scratch_system_template, **kwargs) -> None:
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        self += Role.Heating
        self += Role.Cooling
