from rdflib import URIRef

from ..core import BOB, P223, QUANTITYKIND, UNIT, Air, Medium, Substance
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = BOB


class Air_Change_Per_Hour(QuantifiableObservableProperty):
    """
    airflow / volume * 1hour


    ft^3           1
    ____   *   __________  *  60min = ACH
    min        vol (ft^3)

    """

    _class_iri = P223.AirChangePerHour
    hasQuantityKind = QUANTITYKIND.Dimensionless
    unit = UNIT.UNITLESS


class Count(QuantifiableObservableProperty):
    _class_iri = BOB.Count
    hasQuantityKind = QUANTITYKIND.Dimensionless
    unit = UNIT["NUM"]
    ofMedium: Medium
