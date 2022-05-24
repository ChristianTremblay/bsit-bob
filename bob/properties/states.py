from rdflib import Graph, URIRef

from ..core import (
    EnumerationKind,
    ExternalReference,
    Medium,
    OnOffEnum,
    OccupancyEnum,
    SchemaGraph,
    Substance,
    YesNoEnum,
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
from ..enum import Smoke

_namespace = p223


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(EnumeratedObservableProperty):
    node_type: URIRef = s223.EnumeratedObservableProperty
    hasExternalReference: ExternalReference
    hasEnumerationKind: OnOffEnum


class OnOffCommand(EnumeratedActuatableProperty):
    node_type: URIRef = s223.EnumeratedActuatableProperty
    hasExternalReference: ExternalReference
    hasEnumerationKind: OnOffEnum


class Schedule(EnumerableProperty):
    node_type: URIRef = s223.EnumerableProperty
    hasExternalReference: ExternalReference
    hasEnumerationKind: OccupancyEnum


class OccupancyStatus(EnumeratedObservableProperty):
    node_type: URIRef = s223.EnumeratedObservableProperty
    hasEnumerationKind: OccupancyEnum


class Movement(EnumeratedObservableProperty):
    node_type: URIRef = s223.EnumeratedObservableProperty
    hasExternalReference: ExternalReference
    hasEnumerationKind: OnOffEnum


class SmokePresence(EnumeratedObservableProperty):
    ofMedium: Medium  # set from the sensor
    ofSubstance: Substance = Smoke
    # isObservedBy: Sensor
    hasEnumerationKind: YesNoEnum
