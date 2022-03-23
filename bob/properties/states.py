from msilib.schema import Property
from rdflib import URIRef

from ..property import ActuatableProperty, ObservableProperty
from ..core import EnumerationKind, ExternalReference, quantitykind, unit, p223

__namespace__ = p223


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(ObservableProperty):
    node_type: URIRef = p223.OnOffStatus
    hasExternalReference: ExternalReference
