from typing import Any, Dict

from rdflib import URIRef

from ...core import (
    Device,
    EnumerationKind,
    ExternalReference,
    Graph,
    InletSystemConnectionPoint,
    OutletSystemConnectionPoint,
    Property,
    System,
    p223,
    quantitykind,
    s223,
    schema_graph,
    unit,
)
from ...properties.states import OccupancyStatus, Schedule
from ..functionblock import FunctionBlock

__namespace__ = p223


class OccupancyControl(FunctionBlock):
    hasOccupancyStatus: OccupancyStatus
    hasSchedule: Schedule
    occupancyInlet: InletSystemConnectionPoint
    occupancyOutlet: OutletSystemConnectionPoint
