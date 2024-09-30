from rdflib import URIRef

from ...connections.air import (
    CompressedAirInletConnectionPoint,
    CompressedAirOutletConnectionPoint,
)
from ...connections.liquid import WaterInletConnectionPoint, WaterOutletConnectionPoint
from ...connections.mechanical import MechanicalInletConnectionPoint
from ...connections.naturalgas import (
    NaturalGasInletConnectionPoint,
    NaturalGasOutletConnectionPoint,
)
from ...connections.refrigerant import (
    RefrigerantBidirectionalConnectionPoint,
    RefrigerantInletConnectionPoint,
    RefrigerantOutletConnectionPoint,
)
from ...core import BOB, S223, Equipment, PropertyReference, logging
from ...enum import (  # , R134a, R404a, R407c, R448a, R449a, R452a, R454b, R507a
    R22,
    R32,
    Fluid,
    R410a,
    Refrigerant,
)
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

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["waterInlet", "waterOutlet"], fluid)


class ThreeWayValveDiverting(Valve):
    """
    A diverting valve has 1 inlet and 2 outlets
    """

    _class_iri = S223.ThreeWayValve
    waterInletAB: WaterInletConnectionPoint
    waterOutletA: WaterOutletConnectionPoint
    waterOutletB: WaterOutletConnectionPoint

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["waterInletAB", "waterOutletA", "waterOutletB"], fluid)


class ThreeWayValveMixing(Valve):
    """
    A mixing valve has 2 inlet and 1 outlet
    """

    _class_iri: URIRef = S223.ThreeWayValve
    waterInletA: WaterInletConnectionPoint
    waterInletB: WaterOutletConnectionPoint
    waterOutlet: WaterOutletConnectionPoint

    def set_fluid_type(self, fluid: Fluid):
        self.set_medium(["waterInletA", "waterInletB", "waterOutlet"], fluid)


class NaturalGasValve(Valve):
    _class_iri = S223.Valve
    naturalGasInlet: NaturalGasInletConnectionPoint
    naturalGasOutlet: NaturalGasOutletConnectionPoint


class PneumaticValve(Valve):
    _class_iri = S223.Valve
    compressedAirInlet: CompressedAirInletConnectionPoint
    compressedAirOutlet: CompressedAirOutletConnectionPoint


class ExpansionValve(Valve):
    _class_iri = S223.Valve
    portA: RefrigerantBidirectionalConnectionPoint
    portB: RefrigerantBidirectionalConnectionPoint

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(["portA", "portB"], gas)


class ReversingValve(Valve):
    _class_iri = S223.Valve
    refrigerantHighPressureInlet: RefrigerantInletConnectionPoint
    refrigerantLowPressureOutlet: RefrigerantOutletConnectionPoint
    refrigerantIndoorCoilPort: RefrigerantBidirectionalConnectionPoint
    refrigerantOutdoorCoilPort: RefrigerantBidirectionalConnectionPoint
    position: PropertyReference

    def set_gas_type(self, gas: Refrigerant):
        self.set_medium(
            [
                "refrigerantHighPressureInlet",
                "refrigerantLowPressureOutlet",
                "refrigerantIndoorCoilPort",
                "refrigerantOutdoorCoilPort",
            ],
            gas,
        )
