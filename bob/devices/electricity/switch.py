from typing import Dict

from bob.properties.states import OnOffStatus

from ...connections.electricity import *
from ...core import Device, Node, p223, s223
from ...sensor.electricity import CurrentBinarySensor

_namespace = s223


class CurrentSwitch(Device):
    """
    Current detection device that gives a OnOff status by the action
    of a dry contact when electricity is detected.

    This serves as motor status sensor

    """

    node_type = s223.CurrentSwitch
    hasStatusOutlet: OnOffSignalOutletConnectionPoint
    hasOnOffStatus: OnOffStatus

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
        self._sensors = [sensor]
        self > sensor
