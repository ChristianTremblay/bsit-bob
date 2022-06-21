from ...core import Device, Property, s223
from .coil import ChilledWaterCoil, ElectricalHeatingCoil, HotWaterCoil
from .fan import Fan
from .gas import GasConcentrationSensor, GasMonitor
from .particlecounter import (
    CoarseParticulateSensor,
    FineParticulateSensor,
    ParticleCounter,
    UltraFineParticulateSensor,
)

# TODO : Include everything here as it's created.

# ISSUE : Actually, everything is in the same module... that could lead to potential mess. But I don't want to create too much subfolders either... (monitoring, equipment, etc...)

_namespace = s223


class _Actuator(Device):
    """
    This is required here so actuatesProperty gets its namespace from s223
    """

    _class_iri = s223.Actuator
    actuatesProperty: Property
