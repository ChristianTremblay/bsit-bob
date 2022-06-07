from rdflib import URIRef

from ..core import Air, Medium, Substance, p223, quantitykind, unit
from ..property import QuantifiableActuatableProperty, QuantifiableObservableProperty

_namespace = p223


class Air_Change_Per_Hour(QuantifiableObservableProperty):
    """
    airflow / volume * 1hour


    ft^3           1
    ____   *   __________  *  60min = ACH
    min        vol (ft^3)

    """

    hasQuantityKind = quantitykind.Dimensionless
    unit = unit.UNITLESS
