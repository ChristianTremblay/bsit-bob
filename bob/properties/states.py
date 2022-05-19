from rdflib import Graph, URIRef

from ..core import (
    EnumerationKind,
    ExternalReference,
    Medium,
    SchemaGraph,
    Substance,
    p223,
    quantitykind,
    unit,
    s223,
)
from ..property import (
    ActuatableProperty,
    EnumerableProperty,
    EnumeratedActuatableProperty,
    EnumeratedObservableProperty,
    ObservableProperty,
)

_namespace = p223


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(EnumeratedObservableProperty):
    node_type: URIRef = s223.EnumeratedObservableProperty
    hasExternalReference: ExternalReference


class OnOffCommand(EnumeratedActuatableProperty):
    node_type: URIRef = s223.EnumeratedActuatableProperty
    hasExternalReference: ExternalReference


Occupancy = EnumerationKind(node_iri=p223["EnumerationKind-Occupancy"])


class Schedule(EnumerableProperty):
    node_type: URIRef = s223.EnumerableProperty
    hasExternalReference: ExternalReference


class OccupancyStatus(EnumeratedObservableProperty):
    node_type: URIRef = s223.EnumeratedObservableProperty
    hasEnumerationKind: EnumerationKind = Occupancy


class Movement(ObservableProperty):
    hasExternalReference: ExternalReference


Smoke = Substance(node_iri=p223["Substance-Smoke"])


class SmokePresence(ObservableProperty):
    ofMedium: Medium  # set from the sensor
    ofSubstance: Substance = Smoke
    # isObservedBy: Sensor
