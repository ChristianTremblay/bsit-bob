import decimal
import logging
from typing import Any, List, Union

from rdflib import Literal  # type: ignore
from rdflib import RDF, RDFS, XSD, BNode, Graph, Namespace, URIRef

from .core import (
    EnumerationKind,
    ExternalReference,
    Node,
    Property,
    logging,
    QUANTITYKIND,
    QUDT,
    S223,
    UNIT,
)

_namespace = S223


class ActuatableProperty(Property):
    """
    Such as the setting of a switch.
    """

    _class_iri: URIRef = S223.ActuatableProperty
    hasExternalReference: ExternalReference


class ObservableProperty(Property):
    """
    Such as the state of an alarm detector.
    """

    _class_iri: URIRef = S223.ObservableProperty
    hasExternalReference: ExternalReference
    isObservedBy: Node


class QuantifiableProperty(Property):
    """
    A property to be expressed as a quantity, it has units.
    """

    _attr_uriref = {"unit": QUDT["unit"], "hasQuantityKind": QUDT["hasQuantityKind"]}

    _class_iri: URIRef = S223.QuantifiableProperty
    hasExternalReference: ExternalReference
    unit: URIRef
    hasQuantityKind: URIRef

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

    def set_value(self, value):
        self.hasValue = Literal(value, datatype=XSD.decimal)


class QuantifiableActuatableProperty(QuantifiableProperty, ActuatableProperty):
    """
    Such as a numerical setpoint.
    """

    _class_iri: URIRef = S223.QuantifiableActuatableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


# Setpoints are subclasses of properties currently, but should they be quantifiable actuatable subclass?
# Setpoint can be actuatable be they can also be the result of an algortithm in which case, they
# are observable
# There could be 2 subclasses of setpoint ?
class Setpoint(QuantifiableProperty):
    _class_iri: URIRef = S223.Setpoint
    hasApsect: EnumerationKind
    hasDeadband: Literal
    hasValue: Literal

    def __init__(self, **kwargs):
        _properties = {}
        for k, v in self.__annotations__.items():
            if k in kwargs:
                _properties[k] = kwargs.pop(k)
        super().__init__(**kwargs)
        for k, v in _properties.items():
            if v is not None:
                setattr(self, k, self.__annotations__[k](v))


class QuantifiableObservableProperty(QuantifiableProperty, ObservableProperty):
    """
    Such as a temperature reading.
    """

    _class_iri: URIRef = S223.QuantifiableObservableProperty
    hasSetpoint: Setpoint

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class EnumerableProperty(Property):
    """
    A property to be expressed as an EnumerationKind.
    """

    # _attr_uriref = {}

    _class_iri: URIRef = S223.EnumerableProperty
    hasEnumerationKind: EnumerationKind
    hasExternalReference: ExternalReference

    def __init__(self, value: Any = None, **kwargs: Any) -> None:
        logging.debug(f"EnumerableProperty.__init__ {value!r} {kwargs}")

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        # TODO : Find a way to be sure it's a good Enumeration for the EnumerationKind ?
        if init_value is not None:
            if isinstance(init_value, Literal):
                init_value = Literal(init_value)
            else:
                raise TypeError(f"enumeration expected: {init_value}")

        super().__init__(init_value, **kwargs)


class EnumeratedObservableProperty(EnumerableProperty, ObservableProperty):
    """
    Such as a On-Off Status.
    """

    _class_iri: URIRef = S223.EnumeratedObservableProperty

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class EnumeratedActuatableProperty(EnumerableProperty, ActuatableProperty):
    """
    Such as a On-Off command.
    """

    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasExternalReference: ExternalReference

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
