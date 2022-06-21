from ..core import PropertyReference, BOB, P223, S223
from ..functions import FunctionBlock
from ..properties import OccupancyStatus, Schedule

_namespace = BOB


class OccupancyControl(FunctionBlock):
    _class_iri = P223.OccupancyFunctionBlock
    occupancyStatus: OccupancyStatus
    schedule: Schedule
    # hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
