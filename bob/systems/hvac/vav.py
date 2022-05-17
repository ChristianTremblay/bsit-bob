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
from ...connections.electricity import Electricity_575V_60HzSystemInletConnectionPoint
from ...core import Device, PropertyReference, System, p223, unit
from ...devices.hvac.coil import HotWaterCoil
from ...devices.hvac.damper import Damper, ElectricalActuatedProportionalDamper
from ...devices.hvac.fan import Fan
from ...devices.hvac.valve import TwoWayActuatedProportionalValve
from ...sensor.flow import AirFlowSensor

_namespace = p223

vav_system_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"unit": unit.L_PER_SEC, "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "devices": {
        ("DPR", ElectricalActuatedProportionalDamper): {"comment": "VAV Box Damper"}
    },
}

vav_dual_template = {
    "params": {"label": "VAV", "comment": "VAV Dual Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"unit": unit.L_PER_SEC, "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "devices": {
        ("DPR", ElectricalActuatedProportionalDamper): {"comment": "VAV Box Damper"},
        ("HTGCOIL", HotWaterCoil): {"comment": "Hot Water Coil"},
        ("HTGVLV", TwoWayActuatedProportionalValve): {"comment": "VAV Box Damper"},
        ("FAN", Fan): {"comment": "Fan"},
    },
}

vav_withreheat_template = {
    "params": {"label": "VAV", "comment": "VAV Description"},
    "sensors": {
        ("SA-F", AirFlowSensor): {"unit": unit.L_PER_SEC, "comment": "Air Flow"},
        ("DA-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Discharge Air Temperature",
        },
        ("ZN-T", AirTemperatureSensor): {
            "unit": unit.DEG_C,
            "comment": "Temperature of space",
        },
    },
    "devices": {
        ("DPR", ElectricalActuatedProportionalDamper): {"comment": "VAV Box Damper"},
        ("HWC", HotWaterCoil): {"comment": "VAV Hot Water Coil"},
    },
}


class VAV(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint

    def __init__(self, config: Dict = {}, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)


class VAV_Simple(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    zoneTemperature: PropertyReference

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"].airInlet
        self.airOutlet.mapsTo = self["DPR"].airOutlet
        self.zoneTemperature = self["ZN-T"].observesProperty
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observesProperty

        self["SA-F"].hasMeasurementLocation = self["DPR"].airOutlet
        self["DA-T"].hasMeasurementLocation = self["DPR"].airOutlet


class VAV_Dual(System):
    airInlet: AirInletSystemConnectionPoint
    plenumInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    supplyAirFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference
    zoneTemperature: PropertyReference

    def __init__(self, config: Dict = vav_system_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"].airInlet
        self.airOutlet.mapsTo = self["DPR"].airOutlet
        self.zoneTemperature = self["ZN-T"].observesProperty
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observesProperty

        self["SA-F"].hasMeasurementLocation = self["DPR"].airOutlet
        self["DA-T"].hasMeasurementLocation = self["DPR"].airOutlet


class VAV_Reheat(System):
    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: PropertyReference
    occupancyStatus: PropertyReference
    damperPosition: PropertyReference

    def __init__(self, config: Dict = vav_withreheat_template, **kwargs) -> None:
        kwargs = {**config.get("params", {}), **kwargs}
        super().__init__(config, **kwargs)
        self.airInlet.mapsTo = self["DPR"].airInlet
        self.airOutlet.mapsTo = self["DPR"].airOutlet
        # self.damperPosition = self['DPR'].position
        # self.airFlow = self['SA-F'].observesProperty

        self["SA-F"].hasMeasurementLocation = self["DPR"].airOutlet
        self["DA-T"].hasMeasurementLocation = self["HWC"].airOutlet

        self["DPR"] >> self["HWC"]
