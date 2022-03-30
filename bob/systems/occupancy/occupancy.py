from ...core import (
    ExternalReference,
    Device,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    System,
    s223,
    p223,
    quantitykind,
    unit,
    Property,
    EnumerationKind,
    Graph,
    schema_graph,
)
from rdflib import URIRef

from ...properties.states import OccupancyStatus, Schedule
from ..functionblock import FunctionBlock
from ...devices import contains_devices_list
from ...sensor import define_sensors

from typing import Any, Dict

__namespace__ = p223


occupancy_template = {
    "params": {"label": "Name", "comment": "Description"},
    "sensors": {},
    "contains": {("sub_device1_label", Device): {"comment": "SubDev comment"}},
}


class OccupancyControl(FunctionBlock):
    hasOccupancyStatus: OccupancyStatus
    hasSchedule: Schedule
    occupancyInlet: InletSystemConnectionPoint
    occupancyOutlet: OutletSystemConnectionPoint

    def __init__(self, config: Dict = None, **kwargs):
        if not config and not kwargs:
            raise ValueError(
                "Please provide configuration dict or kwargs, at least a label"
            )

        sensors = define_sensors(config)
        devices, device_kwargs = contains_devices_list(config, **kwargs)

        super().__init__(**device_kwargs)
        # for sensor in sensors:
        #    self > sensor
        for dev in devices:
            self > dev
        self._contains = devices
        self._contains.extend(sensors)

    def __getitem__(self, name: str) -> Any:
        for each in self._contains:
            if each.label == name:
                return each
