from ..core import PropertyReference, p223
from ..functions import FunctionBlock
from ..properties import OccupancyStatus, Schedule

__namespace__ = p223


class OccupancyControl(FunctionBlock):
    hasOccupancyStatus: OccupancyStatus
    hasSchedule: Schedule
    hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
