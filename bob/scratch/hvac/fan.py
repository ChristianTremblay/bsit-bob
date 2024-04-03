import logging
from typing import Dict

from bob.properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from bob.properties.flow import Flow
from bob.properties.ratio import Percent, PercentCommand


from bob.template import configure_relations, template_update
from rdflib import URIRef

from bob.connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from bob.connections.electricity import (
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from bob.core import (
    SCRATCH,
    UNIT,
    PropertyReference,
)

from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.equipment.hvac.fan import Fan as _BasicFan

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = SCRATCH

fan_properties_template = {
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
}


class Fan(_BasicFan):
    """
    Prototype of a Fan based on the Bob Fan class
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

    _class_iri: URIRef = SCRATCH.Fan
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    onOffStatus: PropertyReference
    onOffCommand: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(fan_properties_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.info(f"Fan.__init__ {_config} {kwargs}")
        _relations = _config.pop("relations", [])
        super().__init__(_config, **kwargs)
        configure_relations(self, _relations)


# Prototype of a 600V Fan with a starter providing status and command
system_600VFan_with_Starter_template = {
    # "params": {
    #    "comment": "Prototype of a 600V Fan with a starter providing status and command"
    # },
    "equipment": {
        ("fan", Fan): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint
                },
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
            },
        },
        ("starter", MotorStarter): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
                    "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
                },
                "properties": {("speedRatio", PercentCommand): {}},
            },
        },
    },
    "relations": [
        ("['fan'].onOffCommand", "=", '["starter"]["onOffCommand"]'),
        (
            "['fan'].onOffStatus",
            "=",
            '["starter"].onOffStatus',
        ),
        ('["starter"].actuatesProperty', "=", '["fan"]["speedRatio"]'),
        ('["starter"].electricalOutlet', ">>", "['fan'].electricalInlet"),
    ],
}

system_600VFan_with_VFD_template = {
    "params": {
        "comment": "Prototype of a 600V Fan with a VFD providing status and command. VFD is a controller executing a function providing relations between different properties of the VFD itself"
    },
    "equipment": {
        ("fan", Fan): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint
                },
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
            },
        },
        ("vfd", VFD): {},
    },
    "relations": [
        ("self['fan'].onOffCommand", "=", 'self["vfd"]["run_command"]'),
        ("self['fan'].onOffStatus", "=", 'self["vfd"]["drive_running"]'),
        ('self["vfd"].actuatesProperty', "=", 'self["fan"]["speedRatio"]'),
        ('self["vfd"].electricalOutlet', ">>", "self['fan'].electricalInlet"),
    ],
}
