from typing import List, Union, Any
from rdflib import Graph, Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD  # type: ignore
from .core import (
    logging,
    s223,
)
from .node import Property

__namespace__ = s223


class ActuatableProperty(Property):
    """
    Such as the setting of a switch.
    """

    node_type: URIRef = s223.ActuatableProperty


class ObservableProperty(Property):
    """
    Such as the state of an alarm detector.
    """

    node_type: URIRef = s223.ObservableProperty


class QuantifiableProperty(Property):
    """
    A property to be expressed as a quantity, it has units.
    """

    node_type: URIRef = s223.QuantifiableProperty
    hasQuantityKind: URIRef
    hasUnits: URIRef

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    node_type: URIRef = s223.QuantifiableActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    node_type: URIRef = s223.QuantifiableObservableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
