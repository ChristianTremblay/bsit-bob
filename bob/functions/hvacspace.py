from ..core import PropertyReference, bob, p223, s223
from ..functions import FunctionBlock
from ..properties import OccupancyStatus, PercentCommand, Schedule, Temperature

_namespace = bob

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
