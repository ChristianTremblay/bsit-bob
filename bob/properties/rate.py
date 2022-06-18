from rdflib import URIRef

from ..core import Air, Medium, Substance, bob, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = bob


class Air_Change_Per_Hour(QuantifiableObservableProperty):
    """
    airflow / volume * 1hour


    ft^3           1
    ____   *   __________  *  60min = ACH
    min        vol (ft^3)

    """

    _class_iri = p223.AirChangePerHour
    hasQuantityKind = quantitykind.Dimensionless
    unit = unit.UNITLESS
