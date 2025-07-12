from typing import Any, Tuple


from bob.functions import Function
from bob.properties.force import DifferentialStaticPressure, Pressure

from ..core import BOB, INCLUDE_INVERSE, S223, Node, PropertyReference, LocationReference
from ..enum import Air, Water
from ..properties import DifferentialStaticPressure
from .sensor import Sensor, split_kwargs

_namespace = BOB


class PressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference  # Temperature
    # hasObservationLocation: LocationReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        if "hasUnit" not in _property_kwargs:
            raise ValueError("You must provide hasUnit when defining a pressure sensor")
        if "ofMedium" not in _property_kwargs:
            raise ValueError(
                "You must provide ofMedium when defining a pressure sensor"
            )

        super().__init__(**_sensor_kwargs)

        self.observes = Pressure(
            # isObservedBy=self,
            label=f"{self.label}.GaugePressure",
            **_property_kwargs,
        )


class DifferentialStaticPressureSensor(Sensor):
    _class_iri = S223.PressureSensor
    observes: PropertyReference
    observation_pressure: Pressure
    reference_pressure: Pressure
    differential_static_pressure: DifferentialStaticPressure
    hasObservationLocation: LocationReference
    hasReferenceLocation: LocationReference

    def __init__(self, **kwargs: Any) -> None:
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)

        super().__init__(**_sensor_kwargs)

    def add_hasReferenceLocation(self, node: Node) -> None:
        # link the two together
        reference_location = node
        self._data_graph.add(
            (self._node_iri, S223.hasReferenceLocation, reference_location._node_iri)
        )
        self.hasReferenceLocation = reference_location

    def add_hasObservationLocation(self, node: Node) -> None:
        """
        When defining the observation localtion and the reference location with a template
        we can use the same function twice. First run will set the observation location, 
        second run will set the reference location.
        """ 
        if self.hasObservationLocation is not None:
            self.add_hasReferenceLocation(node)

        else:
            self._data_graph.add(
                (self._node_iri, S223.hasObservationLocation, node._node_iri)
            )
            self.hasObservationLocation = node


class AirDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.PressureSensor
    # observes: PropertyReference

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Air,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ObservationPressure",
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Air,
            label=f"{self.label}.ReferencePressure",
            **_property_kwargs,
        )

        diff_function = Function(
            label="differential calculation", comment="Will output High minus Low"
        )
        self > diff_function
        diff_function.hasInput(self.observation_pressure)
        diff_function.hasInput(self.reference_pressure)
        diff_function.hasOutput(self.differential_static_pressure)

        self.observes = self.differential_static_pressure


class WaterDifferentialStaticPressureSensor(DifferentialStaticPressureSensor):
    _class_iri = S223.PressureSensor

    def __init__(self, **kwargs):
        _sensor_kwargs, _property_kwargs = split_kwargs(kwargs)
        super().__init__(**_sensor_kwargs)
        self.differential_static_pressure = DifferentialStaticPressure(
            ofMedium=Water,
            label=f"{self.label}.DifferentialStaticPressure",
            **_property_kwargs,
        )
        self.observation_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ObservationPressure",
            **_property_kwargs,
        )
        self.reference_pressure = Pressure(
            ofMedium=Water,
            label=f"{self.label}.ReferencePressure",
            **_property_kwargs,
        )

        diff_function = Function(
            label="differential calculation", comment="Will output High minus Low"
        )
        self > diff_function
        diff_function.hasInput(self.observation_pressure)
        diff_function.hasInput(self.reference_pressure)
        diff_function.hasOutput(self.differential_static_pressure)

        self.observes = self.differential_static_pressure
