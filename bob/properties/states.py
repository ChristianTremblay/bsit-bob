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
)
from ..property import ActuatableProperty, ObservableProperty

_namespace = p223


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(ObservableProperty):
    node_type: URIRef = p223.OnOffStatus
    hasExternalReference: ExternalReference


class NormalAlarmStatus(ObservableProperty):
    node_type: URIRef = p223.NormalAlarmStatus
    hasExternalReference: ExternalReference
    measuresMedium: Medium


class OpenCloseStatus(ObservableProperty):
    node_type: URIRef = p223.OpenCloseStatus
    hasExternalReference: ExternalReference
    measuresMedium: Medium


class OnOffCommand(ActuatableProperty):
    node_type: URIRef = p223.OnOffCommand
    hasExternalReference: ExternalReference


Occupancy = EnumerationKind(node_iri=p223["EnumerationKind-Occupancy"])


class Schedule(ObservableProperty):
    node_type: URIRef = p223.Schedule
    hasExternalReference: ExternalReference


class OccupancyStatus(ObservableProperty):
    node_type: URIRef = p223.OccupancyStatus
    hasEnumerationKind: EnumerationKind = Occupancy


class Movement(ObservableProperty):
    hasExternalReference: ExternalReference


Smoke = Substance(node_iri=p223["Substance-Smoke"])


class SmokePresence(ObservableProperty):
    ofMedium: Medium  # set from the sensor
    ofSubstance: Substance = Smoke
    # isObservedBy: Sensor
