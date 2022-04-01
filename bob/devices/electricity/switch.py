from bob.properties.states import OnOffStatus
from ...connections.electricity import *
from ...sensor.electricity import CurrentBinarySensor

from ...core import Device, Node, s223, p223
from ...devices import composite
from typing import Any

__namespace__ = s223


@composite
class CurrentSwitch(Device):
    """
    Current detection device that gives a OnOff status by the action
    of a dry contact when electricity is detected.

    This serves as motor status sensor

    """

    node_type = s223.CurrentSwitch
    hasStatusOutlet: OnOffSignalOutletConnectionPoint
    hasOnOffStatus: OnOffStatus

    def __init__(self, **kwargs):
        _measuresMedium = kwargs.pop("measuresMedium")
        _hasMeasurementLocation = kwargs.pop("hasMeasurementLocation", None)
        _label = kwargs["label"]

        super().__init__(**kwargs)
        self.sensors = CurrentBinarySensor(
            label=_label + "CurrentBinarySensor",
            measuresMedium=_measuresMedium,
            hasMeasurementLocation=_hasMeasurementLocation,
        )
