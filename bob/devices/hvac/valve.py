from typing import Any

from rdflib import URIRef

from bob.connections.air import (
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from bob.connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)

from ...connections.electricity import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalInletConnectionPoint,
)
from ...connections.water import (
    ChilledWaterInletConnectionPoint,
    ChilledWaterOutletConnectionPoint,
    HotWaterInletConnectionPoint,
    HotWaterOutletConnectionPoint,
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import Device, PropertyReference, s223
from ...properties import Gallons, Percent

_namespace = s223

# ISSUE
# Technically, valve are manual, electrical, pneumatic... should we define
# all classes or find a way to make it ?


class Valve(Device):
    _class_iri: URIRef = s223.Valve
    positionInlet: ModulationSignalInletConnectionPoint
    onOffInlet: OnOffSignalInletConnectionPoint
    flowCoefficient: Gallons
    hasPositionCommand: Percent
    hasPositionFeedback: Percent

    def __init__(self, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        super().__init__(**kwargs)
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))


class TwoWayValve(Valve):
    _class_iri: URIRef = s223.Valve

    def __init__(self, **kwargs):
        _waterInlet = kwargs.pop("waterInlet", WaterInletConnectionPoint)
        _waterOutlet = kwargs.pop("waterOutlet", WaterOutletConnectionPoint)
        super().__init__(**kwargs)
        self.waterInlet = _waterInlet(self)
        self.waterOutlet = _waterOutlet(self)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri: URIRef = s223.Valve

    def __init__(self, **kwargs):
        _waterInletAB = kwargs.pop("waterInletAB", WaterInletConnectionPoint)
        _waterOutletA = kwargs.pop("waterOutletA", WaterOutletConnectionPoint)
        _waterOutletB = kwargs.pop("waterOutletB", WaterOutletConnectionPoint)
        super().__init__(**kwargs)
        self.waterInletAB = _waterInletAB(self)
        self.waterOutletA = _waterOutletA(self)
        self.waterOutletB = _waterOutletB(self)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = s223.Valve

    def __init__(self, **kwargs):
        _waterInletA = kwargs.pop("waterInletA", WaterInletConnectionPoint)
        _waterInletB = kwargs.pop("waterInletB", WaterInletConnectionPoint)
        _waterOutletAB = kwargs.pop("waterOutletAB", WaterOutletConnectionPoint)
        super().__init__(**kwargs)
        self.waterInletA = _waterInletA(self)
        self.waterInletB = _waterInletB(self)
        self.waterOutletAB = _waterOutletAB(self)


class NaturalGasValve(Valve):
    _class_iri: URIRef = s223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(Valve):
    _class_iri: URIRef = s223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint
