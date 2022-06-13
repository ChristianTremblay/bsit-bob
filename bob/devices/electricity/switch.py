from typing import Dict

from bob.properties.electricity import Amps
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import *
from ...core import Device, Node, PropertyReference, logging, p223, s223
from ...properties.time import Hour
from ...sensor.electricity import CurrentBinarySensor

_namespace = s223

# TODO : Use templates

switch_template = {
    "cp": {
        "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_120V_60HzOutletConnectionPoint,
    },
    "properties": {
        ("amps", Amps): {},
    },
}


class Switch(Device):
    _class_iri = s223.ElectricalSwitch
    # electricalInlet: ElectricalInletConnectionPoint
    # electricalOutlet: ElectricalOutletConnectionPoint
    hasMaxRange: Amps

    def __init__(self, config: Dict = None, **kwargs):
        _config = switch_template
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}

        super().__init__(_config, **kwargs)


class SinglePoleSwitch(Switch):
    """
    One inlet and one outlet
    hasMaxRange = current max of switch
    A rule could check inlet and outlet are same class
    """

    _cross_ref = {
        "120": (
            Electricity_120V_60HzInletConnectionPoint,
            Electricity_120V_60HzOutletConnectionPoint,
        ),
        "277": (
            Electricity_277V_60HzInletConnectionPoint,
            Electricity_277V_60HzOutletConnectionPoint,
        ),
        "347": (
            Electricity_347V_60HzInletConnectionPoint,
            Electricity_347V_60HzOutletConnectionPoint,
        ),
    }

    def __init__(self, config: Dict = {}, **kwargs):
        _config = switch_template
        if config:
            _config.update(config)
        _voltage = kwargs.pop("voltage") if "voltage" in kwargs else None
        if _voltage:
            _electricalInlet, _electricalOutlet = self._cross_ref[str(_voltage)]
            _config["cp"]["electricalInlet"] = _electricalInlet
            _config["cp"]["electricalOutlet"] = _electricalOutlet
        kwargs = {**_config.get("params", {}), **kwargs}

        super().__init__(_config, **kwargs)


class CurrentRelay(Device):
    """
    Current detection device that gives a OnOff status by the action
    of a dry contact when electricity is detected.

    This serves as motor status sensor

    """

    _class_iri = s223.CurrentRelay
    outputSignal: OnOffSignalOutletConnectionPoint
    onOffStatus: OnOffStatus

    def __init__(self, config: Dict = {}, **kwargs):
        kwargs = {**config.get("params", {}), **kwargs}
        _ofMedium = kwargs.pop("ofMedium")
        _hasMeasurementLocation = kwargs.pop("hasMeasurementLocation", None)

        _label = kwargs["label"]

        super().__init__(config, **kwargs)

        sensor = CurrentBinarySensor(
            label=_label + "CurrentBinarySensor",
            ofMedium=_ofMedium,
            hasMeasurementLocation=_hasMeasurementLocation,
        )
        self.onOffStatus = sensor.observesProperty
        self._sensors = [sensor]
        self > sensor


class TimerSwitch(SinglePoleSwitch):
    """
    Manuel switch with integrated timer
    Typically used for exhaust fan in bathrooms for example
    """

    delay: Hour
    # onOffStatus: PropertyReference
    # onOffCommand: OnOffCommand

    def __init__(self, config: Dict = {}, **kwargs):
        _config = switch_template
        if config:
            _config.update(config)
        _delay = kwargs.pop("delay") if "delay" in kwargs else None
        if _delay:
            _config["properties"][("delay", Hour)] = {"hasValue": _delay}
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
