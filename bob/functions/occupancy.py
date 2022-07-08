from ..core import PropertyReference, BOB, P223, S223
from ..functions import FunctionBlock, InputConnector, OutputConnector
from ..properties import OccupancyStatus, Schedule

_namespace = BOB


class OccupancyFunction(FunctionBlock):
    """
    This function takes the the occupancy as detected by a sensor (inStatus,
    perhaps from a motion sensor), the occupancy schedule (inSchedule with
    an external reference to a BACnet Schedule Object) and outputs
    "occupied" if the space/room/zone should be considered occupied.
    """
    _class_iri = P223.OccupancyFunctionBlock

    inStatus: InputConnector
    inSchedule: InputConnector
    outStatus: OutputConnector


class OccupancyControl(FunctionBlock):
    _class_iri = P223.OccupancyFunctionBlock
    occupancyStatus: OccupancyStatus
    schedule: Schedule
    # hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
