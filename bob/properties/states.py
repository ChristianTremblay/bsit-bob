from rdflib import Graph, URIRef

from ..core import (
    EnumerationKind,
    ExternalReference,
    Light,
    Medium,
    SchemaGraph,
    Substance,
    BOB,
    P223,
    QUANTITYKIND,
    S223,
    UNIT,
)
from ..enum import (
    NormalAlarmEnum,
    OccupancyEnum,
    OnOffEnum,
    OpenCloseEnum,
    Smoke,
    YesNoEnum,
)
from ..property import (
    ActuatableProperty,
    EnumerableProperty,
    EnumeratedActuatableProperty,
    EnumeratedObservableProperty,
    ObservableProperty,
)

_namespace = BOB


# On Off Status is telemetry so the value depends on hasExternalReference
# Using EnumerationKind will lead to the reading being written down in the model
# which is not what we want. We want to know where to find this real time status.


class OnOffStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = OnOffEnum
    hasValue: OnOffEnum


class OnOffCommand(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = OnOffEnum
    hasValue: OnOffEnum


class NormalAlarmStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = NormalAlarmEnum
    hasValue: NormalAlarmEnum


class OpenCloseCommand(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = OpenCloseEnum
    hasValue: OpenCloseEnum


class OpenCloseStatus(EnumeratedActuatableProperty):
    _class_iri: URIRef = S223.EnumeratedActuatableProperty
    hasEnumerationKind = OpenCloseEnum
    hasValue: OpenCloseEnum


class Schedule(EnumerableProperty):
    _class_iri: URIRef = S223.EnumerableProperty
    hasEnumerationKind = OccupancyEnum
    hasValue: OccupancyEnum


class OccupancyStatus(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = OccupancyEnum
    hasValue: OccupancyEnum


class Movement(EnumeratedObservableProperty):
    _class_iri: URIRef = S223.EnumeratedObservableProperty
    hasEnumerationKind = OnOffEnum
    hasValue: OnOffEnum


class SmokePresence(EnumeratedObservableProperty):
    ofMedium: Medium  # set from the sensor
    ofSubstance: Substance = Smoke
    # isObservedBy: Sensor
    hasEnumerationKind = YesNoEnum
    hasValue: YesNoEnum


class DaylightDetected(EnumeratedObservableProperty):
    ofMedium: Light.Visible
    hasEnumerationKind: YesNoEnum
    hasValue: YesNoEnum
