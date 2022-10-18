from ..core import BOB, P223, S223, PropertyReference
from ..functions import FunctionBlock
from ..properties import OccupancyStatus, PercentCommand, Schedule, Temperature

_namespace = BOB

# WIP : For now, it won't be in hvacspace by default


class IndoorAir(FunctionBlock):
    # uses_input
    heating: PercentCommand
    cooling: PercentCommand
    # produces_output
    temperture: Temperature
    hasOccupancySensor: PropertyReference
    # What if I need to connect more than 1 ???
    # def __init__(self, **kwargs):
