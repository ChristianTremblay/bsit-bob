import logging
from typing import Dict

from rdflib import URIRef

from bob.equipment.electricity.vfd import VFD
from bob.properties.flow import Flow
from bob.properties.ratio import Percent, PercentCommand

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
)
from ...core import (
    BOB,
    QUANTITYKIND,
    S223,
    UNIT,
    ConnectionPoint,
    Equipment,
    PropertyReference,
    template_update,
)
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty
from ..electricity.starter import MotorStarter
from ..electricity.vfd import VFD

_namespace = BOB

fan_template = {
    "cp": {"electricalInlet": Electricity_575V_60HzInletConnectionPoint},
    "properties": {
        ("speedRatio", PercentCommand): {},
        ("staticPressure", Pressure): {"unit": UNIT.PA},
        ("amps", Amps): {},
        ("rpm", RPM): {},
        ("cfm", Flow): {"unit": UNIT["FT3-PER-MIN"]},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("powerFactor", PowerFactor): {},
        ("efficiency", Percent): {},
    },
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
        logging.debug(f"Fan.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)


starter_addon_template = {
    "equipment": {
        ("starter", MotorStarter): {
            "config": {
                "cp": {
                    "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
                    "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
                }
            },
        }
    },
    "properties": {("speedRatio", PercentCommand): {}},
}


class FanWithStarter(Fan):
    """
    This fan is composed of a blower, an electrical motor and a starter
    """

    _class_iri: URIRef = S223.Fan

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[fan_template, starter_addon_template],
            config=config,
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"FanWithStarter.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)
        self.onOffCommand = self["starter"]["onOffCommand"]
        self.onOffStatus = self["starter"]["starter.current_sensor"].observes
        self["starter"].actuatesProperty = self["speedRatio"]
        self["starter"].electricalOutlet >> self.electricalInlet


VFD_addon_template = {
    "equipment": {("vfd", VFD): {}},
    "properties": {},
}


class FanWithVFD(Fan):
    """
    This fan is composed of a blower, an electrical motor and a VFD
    """

    _class_iri: URIRef = S223.Fan

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(
            bases=[fan_template, VFD_addon_template],
            config=config,
        )
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"FanWithVFD.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self.onOffCommand = self["vfd"]["run_command"]
        self.onOffStatus = self["vfd"]["drive_running"]
        self["vfd"].actuatesProperty = self["speedRatio"]
        self["vfd"].electricalOutlet >> self.electricalInlet
