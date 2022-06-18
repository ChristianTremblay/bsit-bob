from ..core import PropertyReference, bob, p223, s223
from ..functions import FunctionBlock
from ..properties import OccupancyStatus, Schedule

_namespace = bob


class OccupancyControl(FunctionBlock):
    _class_iri = p223.OccupancyFunctionBlock
    occupancyStatus: OccupancyStatus
    schedule: Schedule
    # hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
