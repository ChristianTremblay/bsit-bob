from typing import Dict

from bob.properties.states import OnOffStatus
from ...connections.electricity import *
from ...sensor.electricity import CurrentBinarySensor

from ...core import Device, Node, s223, p223

__namespace__ = s223


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
        _measuresMedium = kwargs.pop("measuresMedium")
        _hasMeasurementLocation = kwargs.pop("hasMeasurementLocation", None)

        _label = kwargs["label"]

        super().__init__(config, **kwargs)

        sensor = CurrentBinarySensor(
            label=_label + "CurrentBinarySensor",
            measuresMedium=_measuresMedium,
            hasMeasurementLocation=_hasMeasurementLocation,
        )
        self._sensors = [sensor]
        self > sensor
