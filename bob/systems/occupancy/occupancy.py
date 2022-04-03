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

from typing import Any, Dict

__namespace__ = p223


class OccupancyControl(FunctionBlock):
    hasOccupancyStatus: OccupancyStatus
    hasSchedule: Schedule
    occupancyInlet: InletSystemConnectionPoint
    occupancyOutlet: OutletSystemConnectionPoint
