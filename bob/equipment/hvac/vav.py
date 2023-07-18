import logging
from typing import Any, Dict

from attr import set_run_validators
from rdflib import URIRef

from bob.properties import Flow, PercentCommand
from bob.sensor.temperature import AirTemperatureSensor

from ...connections.air import (
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    UNIT,
    Equipment,
    PropertyReference,
    System,
    template_update,
)
from ...equipment.hvac.coil import HotWaterCoil
from ...equipment.hvac.damper import Damper, ElectricalActuatedProportionalDamper
from ...equipment.hvac.fan import Fan
from ...equipment.hvac.valve import TwoWayActuatedProportionalValve
from ...sensor.flow import AirFlowSensor

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

vav_system_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"hasUnit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {"comment": "VAV Box Damper"}
    },
}

vav_dual_template = {
    "params": {"label": "VAV", "comment": "VAV Dual Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"hasUnit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "VAV Box Damper with its actuator"
        },
        ("HTGCOIL", HotWaterCoil): {"comment": "Hot Water Coil"},
        ("HTGVLV", TwoWayActuatedProportionalValve): {"comment": "VAV Box Damper"},
        ("FAN", Fan): {"comment": "Fan"},
    },
}

vav_withreheat_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"hasUnit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {"comment": "VAV Box Damper"},
        ("HWC", HotWaterCoil): {"comment": "VAV Hot Water Coil"},
    },
}


class VAV(Equipment):
    _class_iri = S223.VAV
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    damper: ElectricalActuatedProportionalDamper

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)

        self.damper = ElectricalActuatedProportionalDamper(label=self.label + ".damper")
        self.damper.airInlet.mapsTo = self.airInlet
        self.damper.airOutlet.mapsTo = self.airOutlet


class VAV_Simple(Equipment):
    _class_iri = S223.VAV
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    airFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    zoneTemperature: PropertyReference

    def __init__(self, config: Dict = None, **kwargs) -> None:
        _config = template_update(vav_system_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VAV_Simple.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        # Mapping internal
        self["DPR"].airInlet.mapsTo = self.airInlet
        self["DPR"].airOutlet.mapsTo = self.airOutlet

        # Equivalence
        self.damperPosition = self["DPR"].position
        self.zoneTemperature = self["ZN-T"].observedProperty
        self.airFlow = self["SA-F"].observedProperty

        self["SA-F"] % self["DPR"]["damper"].airOutlet
        self["DA-T"] % self["DPR"]["damper"].airOutlet


class VAV_Dual(Equipment):
    _class_iri = S223.VAV
    airInlet: AirInletConnectionPoint
    plenumInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    supplyAirFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    zoneTemperature: PropertyReference

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"]["damper"].airInlet
        self.airOutlet.mapsTo = self["DPR"]["damper"].airOutlet
        self.zoneTemperature = self["ZN-T"].observedProperty
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observedProperty

        self["SA-F"] % self["DPR"]["damper"].airOutlet
        self["DA-T"] % self["DPR"]["damper"].airOutlet


class VAV_Reheat(Equipment):
    _class_iri = S223.VAV
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    airFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference

    def __init__(self, config: Dict = vav_withreheat_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"]["damper"].airInlet
        self.airOutlet.mapsTo = self["DPR"]["damper"].airOutlet
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observedProperty

        self["SA-F"] % self["DPR"]["damper"].airOutlet
        self["DA-T"] % self["HWC"].airOutlet

        self["DPR"]["damper"] >> self["HWC"]
