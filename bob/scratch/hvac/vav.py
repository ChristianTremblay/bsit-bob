import logging
from typing import Dict

from bob.core import (
    S223,
    SCRATCH,
    UNIT,
    BoundaryConnectionPoint,
    System,
)
from bob.equipment.hvac.coil import ElectricalHeatingCoil, HotWaterCoil
from bob.properties.flow import Flow
from bob.properties.ratio import Percent
from bob.properties.temperature import Temperature
from bob.scratch.control.controller import VAVController

# Prototypes
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.scratch.hvac.valve import TwoWayActuatedProportionalValve
from bob.sensor.flow import AirFlowSensor
from bob.sensor.temperature import AirTemperatureSensor
from bob.template import template_update, SystemFromTemplate

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

# Equipment Templates
vav_withelectricreheat_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "properties": {
        ("DamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("RoomTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("AirFlow", Flow): {
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
        ("DPR", ElectricalActuatedProportionalDamper): {},
        ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
        ("REHEAT", ElectricalHeatingCoil): {"comment": "VAV Heating Coil"},
    },
    "relations": [
        ("self.airInlet", "=", "self['DPR'].airInlet"),
        ("self.airOutlet", "=", "self['DPR'].airOutlet"),
        # internal references
        ("self['DamperPosition']", "@", 'self["DPR"]["position"]'),
        ("self['RoomTemperature']", "@", 'self["ZN-T"].observedProperty'),
        ("self['AirFlow']", "@", 'self["SA-F"].observedProperty'),
        # Measure location
        ('self["SA-F"]', "%", 'self["DPR"].airInlet'),
        ('self["DA-T"]', "%", 'self["REHEAT"].airOutlet'),
        # Equipment relations
        ('self["DPR"].airOutlet', ">>", 'self["REHEAT"].airInlet'),
        # ('self["VAVController"]["actuator"]', ">>", 'self["DPR"]'),
        ("self['DamperPosition']", "@", "self['DPR']['position']"),
        # ("self['DPR']['position']", "@", "self['VAVController']['position_feedback']"),
        (
            "self['VAVController']['damper_position_feedback']",
            "@",
            "self['DPR']['actuator']['position_feedback']",
        ),
        (
            "self['VAVController']['damper_command']",
            "@",
            "self['DPR']['actuator']['command']",
        ),
    ],
}

vav_withhotwaterreheat_template = vav_withelectricreheat_template.copy()
vav_withhotwaterreheat_template["equipment"] = {
    ("DPR", ElectricalActuatedProportionalDamper): {},
    ("VAVController", VAVController): {"comment": "VAV Controller with damper"},
    ("REHEAT", HotWaterCoil): {"comment": "VAV Heating Coil"},
}

# Template of Flat equipment grouped as a system
vav_system_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "properties": {
        ("DamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("RoomTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("AirFlow", Flow): {
            "hasUnit": UNIT["L-PER-SEC"],
            "comment": "Air Flow",
        },
    },
    "sensors": {
        ("SA-F", AirFlowSensor): {"hasUnit": UNIT["L-PER-SEC"], "comment": "Air Flow"},
        ("ZN-T", AirTemperatureSensor): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "equipment": {
        ("DPR", ElectricalActuatedProportionalDamper): {
            "comment": "Damper",
            "config": {
                "properties": {("position", Percent): {"hasUnit": UNIT.PERCENT}}
            },
        },
    },
    "relations": [
        ("self.airInlet", "=", "self['DPR'].airInlet"),
        ("self.airOutlet", "=", "self['DPR'].airOutlet"),
        # internal references
        ("self['DamperPosition']", "@", 'self["DPR"]["position"]'),
        ("self['RoomTemperature']", "@", 'self["ZN-T"].observedProperty'),
        ("self['AirFlow']", "@", 'self["SA-F"].observedProperty'),
        # Measure location
        ('self["SA-F"]', "%", 'self["DPR"].airInlet'),
    ],
}


class VAV(SystemFromTemplate):
    _class_iri = S223.SingleDuctTerminal
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        """
        If no template is provided, the default template is used.
        The default template contains the following properties:
        - DamperPosition
        - RoomTemperature
        - AirFlow
        The default template contains the following sensors:
        - SA-F: AirFlowSensor
        - ZN-T: AirTemperatureSensor
        The default template contains the following equipment:
        - DPR: Damper
        - VAVController: VAVController
        The default template contains the following relations:
        - self.airInlet = self['DPR'].airInlet
        - self.airOutlet = self['DPR'].airOutlet
        - self['DamperPosition'] @ self["DPR"]["position"]
        - self["SRoomTemperature"] @ self["ZN-T"].observedProperty
        - self["AirFlow"] @ self["SA-F"].observedProperty
        - self["SA-F"] % self["DPR"].airInlet
        """
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VAV.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)


vav_dual_template = {
    "params": {"label": "VAV", "comment": "VAV Dual Description"},
    "properties": {
        ("DamperPosition", Percent): {
            "hasUnit": UNIT.PERCENT,
            "comment": "Damper Position",
        },
        ("RoomTemperature", Temperature): {
            "hasUnit": UNIT.DEG_C,
            "comment": "Temperature of space",
        },
        ("AirFlow", Flow): {
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
        ("DPR", ElectricalActuatedProportionalDamper): {
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


class VAV_Dual(System):
    _class_iri = S223.DualDuctTerminal
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
