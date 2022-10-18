from ..core import BOB, P223, S223, PropertyReference
from ..functions import FunctionBlock, FunctionInput, FunctionOutput
from ..properties import OccupancyStatus, Schedule

_namespace = BOB


class OccupancyFunction(FunctionBlock):
    """
    This function takes the the occupancy as detected by a sensor (inStatus,
    perhaps from a motion sensor), the occupancy schedule (inSchedule with
    an external reference to a BACnet Schedule Object) and outputs
    "occupied" if the space/room/zone should be considered occupied.
    """

    _class_iri = P223.OccupancyFunction

    inStatus: FunctionInput
    inSchedule: FunctionInput
    outStatus: FunctionOutput
