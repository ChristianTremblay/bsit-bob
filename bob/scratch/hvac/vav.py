import logging
from typing import Dict


from bob.sensor.temperature import AirTemperatureSensor

from bob.connections.air import (
    AirInletConnectionPoint,
    AirOutletConnectionPoint,
)
from bob.core import SCRATCH, UNIT, Equipment, PropertyReference
from bob.equipment.hvac.coil import ElectricalHeatingCoil, HotWaterCoil
from bob.equipment.control.controller import Controller
from bob.sensor.flow import AirFlowSensor
from bob.template import template_update

# Prototypes
from bob.scratch.hvac.damper import Damper, ElectricalActuatedProportionalDamper

from bob.scratch.hvac.fan import Fan
from bob.scratch.hvac.valve import TwoWayActuatedProportionalValve
from bob.scratch.control.controller import VAVController

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

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
        ("DPR", Damper): {"comment": "VAV Controller with damper"},
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
        ("DPR", Damper): {"comment": "VAV Controller with damper"},
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
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
        ("DPR", Damper): {"comment": "VAV Controller with damper"},
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("REHEAT", HotWaterCoil): {"comment": "VAV Hot Water Coil"},
    },
}

vav_withelectricreheat_template = {
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
        ("DPR", Damper): {"comment": "Damper"},
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("REHEAT", ElectricalHeatingCoil): {"comment": "VAV Electrical Heating Coil"},
    },
}


class VAV(Equipment):
    _class_iri = SCRATCH.SingleDuctTerminal
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
    _class_iri = SCRATCH.SingleDuctTerminal
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

        # Mapping internal of the group composed of damper and actuator
        self["DPR"].airInlet.maps_to(self.airInlet)
        self["DPR"].airOutlet.maps_to(self.airOutlet)

        # Equivalence
        #self.damperPosition = self["DPR"].position
        self.zoneTemperature = self["ZN-T"].observedProperty
        self.airFlow = self["SA-F"].observedProperty

        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["DPR"].airOutlet


class VAV_Dual(Equipment):
    _class_iri = SCRATCH.DualDuctTerminal
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
        self["DPR"].airInlet.maps_to(self.airInlet)
        self["DPR"].airOutlet.maps_to(self.airOutlet)
        self.zoneTemperature = self["ZN-T"].observedProperty
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observedProperty

        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["DPR"].airOutlet


# Cannot inherit from VAV_Simple for now because DA-T will not point to the same thing and DRP connected to reheat, etc...
class VAV_Reheat(Equipment):
    _class_iri = SCRATCH.SingleDuctTerminalWithReheat
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    airFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    supplyAirTemperature: PropertyReference

    def __init__(self, config: Dict = None, reheat_type="water", **kwargs) -> None:
        if "water" in reheat_type.lower():
            template = vav_withreheat_template
        elif "elec" in reheat_type.lower():
            template = vav_withelectricreheat_template
        else:
            raise ValueError("Please provide reheat_type as water or electrical")
        _config = template_update(template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VAV_Simple.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        # Mapping internal of the group composed of damper and actuator
        self["DPR"].airInlet.maps_to(self.airInlet)
        self["REHEAT"].airOutlet.maps_to(self.airOutlet)

        # Equivalence
        #self['DPR'].damperPosition = self["DPR"].position
        self.zoneTemperature = self["ZN-T"].observedProperty
        self.airFlow = self["SA-F"].observedProperty

        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["REHEAT"].airOutlet

        self["DPR"] >> self["REHEAT"]
        self['VAVController'] >> self['DPR']
