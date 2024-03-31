import logging
from typing import Dict

from rdflib import URIRef

from bob.equipment.electricity.vfd import VFD
from bob.properties.flow import Flow
from bob.properties.ratio import Percent, PercentCommand

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    ConnectionPoint,
    Equipment,
    PropertyReference,
)
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty
from ...template import configure_relations, template_update
from ..electricity.starter import MotorStarter
from ..electricity.vfd import VFD

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB

fan_template = {
    "cp": {"electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint},
    "properties": {
        ("speedRatio", PercentCommand): {},
        ("staticPressure", Pressure): {"hasUnit": UNIT.PA},
        ("amps", Amps): {},
        ("rpm", RPM): {},
        ("cfm", Flow): {"hasUnit": UNIT["FT3-PER-MIN"]},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("powerFactor", PowerFactor): {},
        ("efficiency", Percent): {},
    },
    "relations": [],
}


class Fan(Equipment):
    """
    A fan is composed of a blower and an electrical motor

    Fan speed is an important property
    The intrinsic property I want to make `actuatedby` a starter or a VFD, I'd like it to be
    a PercentCommand.
    Because RPM, cfm, amps, etc... will all depend of this and I would not want having to make multiple
    `actuatesProperty` relationships between the starter/vfd and the fan.
    I only want 1 property.
    Then if required, it'll be possible to calculate RPM, amps, cfm, etc, based on the `PercentCommand` actuated property

    RPM of the fan, can be different from RPM of motor (ex. belt and pulley)
    So here, speed_ratio != RPM because if a fan can deliver x RPM, the ratio of pulley can be changed and
    giving 100% speed_ratio to a fan, may mean a different speed than RPM of fan.

    A motor starter will give 0% or 100% of speed_ratio depending on being On or Off
    A VFD will modulate this speed ratio from 0% to 100%.
    Depending on the configuration of the drive, this ratio can represent 0-60Hz... or 20-50Hz
    (if freq are configured different than 0-60Hz), etc...

    Using speed_ratio will isolate the model from the real time data by providing an agnostic way
    of actuating the fan.
    """

    _class_iri: URIRef = S223.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(fan_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Fan.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)
        configure_relations(self, _config.get("relations", []))


starter_addon_template = {
    "equipment": {
        ("starter", MotorStarter): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
                    "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
                }
            },
        }
    },
    "properties": {("speedRatio", PercentCommand): {}},
    "relations": [
        ("self.onOffCommand", "=", 'self["starter"]["onOffCommand"]'),
        (
            "self.onOffStatus",
            "=",
            'self["starter"]["currentRelay"]["currentSensor"].observes',
        ),
        ('self["starter"].actuatesProperty', "=", 'self["speedRatio"]'),
        ('self["starter"].electricalOutlet', ">>", "self.electricalInlet"),
    ],
}


fan_with_starter_template = template_update(fan_template, starter_addon_template)


VFD_addon_template = {
    "equipment": {("vfd", VFD): {}},
    "properties": {},
    "relations": [
        ("self.onOffCommand", "=", 'self["vfd"]["run_command"]'),
        ("self.onOffStatus", "=", 'self["vfd"]["drive_running"]'),
        ('self["vfd"].actuatesProperty', "=", 'self["speedRatio"]'),
        ('self["vfd"].electricalOutlet', ">>", "self.electricalInlet"),
    ],
}

fan_with_vfd_template = template_update(fan_template, VFD_addon_template)
