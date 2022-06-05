"""
A system is a portion of the universe that has been chosen for studying the changes that 
take place within it in response to varying conditions. A system may be complex, such as a 
planet, or relatively simple, as the liquid within a glass. Those portions of a system that 
are physically distinct and mechanically separable from other portions of the system are called phases.

[ref : https://www.britannica.com/science/phase-state-of-matter#ref507387]

"""

from rdflib import URIRef

from ..connections.air import (
    AirBidirectionalConnectionPoint,
    AirBidirectionalSystemConnectionPoint,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
)
from ..core import Air, Medium, System, p223, s223
from ..property import QuantifiableObservableProperty

_namespace = p223


class PhysicSystem(System):
    """
    This building block is an abstraction of a physic system
    It is meant to semantically model the effect of various environmental variables
    on a medium. (By opposition to mathematically model)

    ex. Indoor air in a space may be affected and its properties changed
    by opening a window or by using a baseboard heater.

    This system models the variation of the properties that will be seen
    in the medium of the object.

    It works a little like a function block in the sense that it is
    a black box that do not have to be defined in details (as all
    the mathematic details are outside of the scope of the standard).
    But it maps to devices and makes it clear that devices in a space, for
    example, have an effect on the indoor air.

    Unlike a typical system that contains devices, Physic Systems do not need
    this. It model the intrinsec behaviour of the medium defined by the mapped connections

    """

    _class_iri = p223.PhysicSystem


class IndoorAir(PhysicSystem):
    """
    This building block is an abstraction of a physic system
    It is meant to model the effect of various environmental variables
    on a medium.

    ex. Indoor air in a space may be affected and its properties changed
    by opening a window or by using a baseboard heater.

    This system models the variation of the properties that will be seen
    in the medium of the object.

    IT works a little like a function block in the sense that it is
    a black box that do not have to be defined in details (as all
    the mathematic details are outside of the scope of the standard).
    But it maps to devices and makes it clear that devices in a space, for
    example, have an effect on the indoor air.

    Unlike a typical system that contains devices, Physic Systems do not need
    this. It model the intrinsec behaviour of the medium defined by the mapped connections

    """

    _class_iri = p223.PhysicSystem
    hasMedium: Medium = Air
    ductAirInlet: AirInletSystemConnectionPoint
    ductAirOutlet: AirOutletSystemConnectionPoint
    airTransfer: AirBidirectionalSystemConnectionPoint
    doors: AirBidirectionalSystemConnectionPoint
    windows: AirBidirectionalSystemConnectionPoint
    radiantHeating: AirBidirectionalSystemConnectionPoint
    radiantCooling: AirBidirectionalSystemConnectionPoint
