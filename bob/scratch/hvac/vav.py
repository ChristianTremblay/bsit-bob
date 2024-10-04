import logging
from typing import Dict

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.core import (
    SCRATCH,
    UNIT,
    BoundaryConnectionPoint,
    Equipment,
    PropertyReference,
    System,
)
from bob.equipment.control.controller import Controller
from bob.equipment.hvac.coil import ElectricalHeatingCoil, HotWaterCoil
from bob.properties.flow import Flow
from bob.properties.ratio import Percent
from bob.properties.temperature import Temperature
from bob.scratch.control.controller import VAVController

# Prototypes
from bob.scratch.hvac.damper import Damper, ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.scratch.hvac.valve import TwoWayActuatedProportionalValve
from bob.sensor.flow import AirFlowSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

vav_system_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "properties": {
        ("SystemDamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("SystemZoneTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("SystemAirFlow", Flow): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air Flow",
        },
    },
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
        ("DPR", Damper): {
            "comment": "Damper",
            "config": {
                "properties": {("position", Percent): {"hasUnit": UNIT.PERCENT}}
            },
        },
    },
}

vav_dual_template = {
    "params": {"label": "VAV", "comment": "VAV Dual Description"},
    "properties": {
        ("SystemDamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("SystemZoneTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("SystemAirFlow", Flow): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air Flow",
        },
    },
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
        ("DPR", Damper): {
            "comment": "Damper",
            "config": {
                "properties": {("position", Percent): {"hasUnit": UNIT.PERCENT}}
            },
        },
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("HTGCOIL", HotWaterCoil): {"comment": "Hot Water Coil"},
        ("HTGVLV", TwoWayActuatedProportionalValve): {"comment": "VAV Box Damper"},
        ("FAN", Fan): {"comment": "Fan"},
    },
}

vav_withreheat_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "properties": {
        ("SystemDamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("SystemZoneTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("SystemAirFlow", Flow): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air Flow",
        },
    },
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
        ("DPR", Damper): {
            "comment": "Damper",
            "config": {
                "properties": {("position", Percent): {"hasUnit": UNIT.PERCENT}}
            },
        },
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("REHEAT", HotWaterCoil): {"comment": "VAV Hot Water Coil"},
    },
}

vav_withelectricreheat_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "properties": {
        ("SystemDamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("SystemZoneTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("SystemAirFlow", Flow): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air Flow",
        },
    },
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
        ("DPR", Damper): {
            "comment": "Damper",
            "config": {
                "properties": {("position", Percent): {"hasUnit": UNIT.PERCENT}}
            },
        },
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("REHEAT", ElectricalHeatingCoil): {"comment": "VAV Electrical Heating Coil"},
    },
}


# class VAV(System):
#    _class_iri = SCRATCH.SingleDuctTerminal
#    airInlet: BoundaryConnectionPoint
#    airOutlet: BoundaryConnectionPoint
#    #damper: ElectricalActuatedProportionalDamper
#    #airFlow: PropertyReference
#    #damperPosition: PropertyReference###
#
#    def __init__(self, config: Dict = {}, **kwargs) -> None:
#        _config = template_update(vav_system_template, config=config)
#        kwargs = {**_config.pop("params", {}), **kwargs}
#        _log.debug(f"VAV.__init__ {_config} {kwargs}")
#        super().__init__(_config, **kwargs)#
#
#        self.damper = ElectricalActuatedProportionalDamper(label=self.label + ".damper")
#        self.airInlet = self.add_boundary_connection_point(self.damper.airInlet)
#        self.airOutlet = self.add_boundary_connection_point(self.damper.airOutlet)


class VAV(System):
    _class_iri = SCRATCH.SingleDuctTerminal
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint
    airFlow: PropertyReference
    # occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    # zoneTemperature: PropertyReference

    def __init__(self, config: Dict = None, **kwargs) -> None:
        _config = template_update(vav_system_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VAV_Simple.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        # Boundaries
        self.airInlet = self.add_boundary_connection_point(self["DPR"].airInlet)
        self.airOutlet = self.add_boundary_connection_point(self["DPR"].airOutlet)

        # internal references
        self["SystemDamperPosition"] @ self["DPR"]["position"]
        self["SystemZoneTemperature"] @ self["ZN-T"].observedProperty
        self["SystemAirFlow"] @ self["SA-F"].observedProperty

        # Measure location
        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["DPR"].airOutlet


class VAV_Dual(System):
    _class_iri = SCRATCH.DualDuctTerminal
    airInlet: BoundaryConnectionPoint
    plenumInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint
    # supplyAirFlow: PropertyReference
    # occupancyStatus: PropertyReference
    # damperPosition: PropertyReference
    # zoneTemperature: PropertyReference

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        _config = template_update(vav_system_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VAV_Dual.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        # Boundaries
        self.airInlet = self.add_boundary_connection_point(self["DPR"].airInlet)
        self.airOutlet = self.add_boundary_connection_point(self["DPR"].airOutlet)

        # internal references
        self["SystemDamperPosition"] @ self["DPR"]["position"]
        self["SystemZoneTemperature"] @ self["ZN-T"].observedProperty
        self["SystemAirFlow"] @ self["SA-F"].observedProperty

        # Measure location
        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["DPR"].airOutlet


# Cannot inherit from VAV_Simple for now because DA-T will not point to the same thing and DRP connected to reheat, etc...
class VAV_Reheat(System):
    _class_iri = SCRATCH.SingleDuctTerminalWithReheat
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint
    # airFlow: PropertyReference
    # occupancyStatus: PropertyReference
    # damperPosition: PropertyReference
    # supplyAirTemperature: PropertyReference

    def __init__(self, config: Dict = None, reheat_type="water", **kwargs) -> None:
        if "water" in reheat_type.lower():
            template = vav_withreheat_template
        elif "elec" in reheat_type.lower():
            template = vav_withelectricreheat_template
        else:
            raise ValueError("Please provide reheat_type as water or electrical")
        _config = template_update(template, config=config)
        kwargs = {
            **_config.pop("params", {}),
            **_config.pop("reheat_type", {}),
            **kwargs,
        }
        _log.debug(f"VAV_Reheat.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)

        # Boundaries
        self.airInlet = self.add_boundary_connection_point(self["DPR"].airInlet)
        self.airOutlet = self.add_boundary_connection_point(self["REHEAT"].airOutlet)

        # Internal references
        self["SystemDamperPosition"] @ self["DPR"]["position"]
        self["SystemZoneTemperature"] @ self["ZN-T"].observedProperty
        self["SystemAirFlow"] @ self["SA-F"].observedProperty

        # Measure location
        self["SA-F"] % self["DPR"].airOutlet
        self["DA-T"] % self["REHEAT"].airOutlet

        # Airflow
        self["DPR"] >> self["REHEAT"]
        self["VAVController"] >> self["DPR"]
