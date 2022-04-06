import decimal
import logging
from typing import Any, List, Union

from rdflib import (
    RDF,
    RDFS,
    XSD,
    BNode,
    Graph,
    Literal,  # type: ignore
    Namespace,
    URIRef,
)

from .core import ExternalReference, Property, logging, quantitykind, qudt, s223, unit

__namespace__ = s223


class ActuatableProperty(Property):
    """
    Such as the setting of a switch.
    """

    node_type: URIRef = s223.ActuatableProperty
    hasExternalReference: ExternalReference


class ObservableProperty(Property):
    """
    Such as the state of an alarm detector.
    """

    node_type: URIRef = s223.ObservableProperty
    hasExternalReference: ExternalReference


class QuantifiableProperty(Property):
    """
    A property to be expressed as a quantity, it has units.
    """

    _attr_uriref = {"unit": qudt["unit"], "hasQuantityKind": qudt["quantityKind"]}

    node_type: URIRef = s223.QuantifiableProperty
    hasQuantityKind: URIRef
    unit: URIRef
    hasExternalReference: ExternalReference

    def __init__(self, value: Any = None, **kwargs: Any) -> None:
        logging.debug(f"QuantifiableProperty.__init__ {value!r} {kwargs}")

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        if init_value is not None:
            if isinstance(init_value, (int, float)):
                init_value = Literal(init_value, datatype=XSD.decimal)
            elif isinstance(init_value, Literal):
                init_value = Literal(init_value)
            else:
                raise TypeError(f"decimal expected: {init_value}")

        super().__init__(init_value, **kwargs)


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    node_type: URIRef = s223.QuantifiableActuatableProperty
    hasExternalReference: ExternalReference

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


# Setpoints are subclasses of properties currently, but should they be quantifiable actuatable subclass?
# Setpoint can be actuatable be they can also be the result of an algortithm in which case, they
# are observable
# There could be 2 subclasses of setpoint ?
class Setpoint(QuantifiableProperty):
    """
    Such as a numerical setpoint.
    """

    node_type: URIRef = s223.Setpoint

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    node_type: URIRef = s223.QuantifiableObservableProperty
    hasSetpoint: Setpoint

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
