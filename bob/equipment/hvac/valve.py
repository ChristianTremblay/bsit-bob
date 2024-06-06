from rdflib import URIRef

from ...connections.air import (
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.mechanical import MechanicalInletConnectionPoint
from ...connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)

from ...connections.liquid import (
    WaterInletConnectionPoint,
    WaterOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, PropertyReference, logging
from ...properties import Gallons

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


class Valve(Equipment):
    """
    Base class for a valve. Must be subclassed to provide inlet and outlet
    depending on configuration
    """

    _class_iri: URIRef = S223.Valve
    linkageInlet: MechanicalInletConnectionPoint
    position: PropertyReference
    command: PropertyReference
    position_feedback: PropertyReference
    flowCoefficient: Gallons


class TwoWayValve(Valve):
    """
    Two-way valve have 1 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.TwoWayValve
    waterInlet: WaterInletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint
    is_open: PropertyReference
    is_closed: PropertyReference


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = S223.ThreeWayValve
    waterInletAB: WaterInletConnectionPoint
    waterOutletA: WaterOutletConnectionPoint
    waterOutletB: WaterOutletConnectionPoint


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.ThreeWayValve
    waterInletA: WaterInletConnectionPoint
    waterInletB: WaterOutletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint


class NaturalGasValve(Valve):
    _class_iri = S223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(Valve):
    _class_iri = S223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint
