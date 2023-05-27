"""
Function Blocks

This is a facade for ASHRAE 231 Controls Description Language
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, AnyStr, Dict

from rdflib import Literal, URIRef  # type: ignore

from ..core import (
    G36,
    INCLUDE_INVERSE,
    P223,
    S223,
    Container,
    LocationReference,
    Node,
    Property,
    _Producer,
    data_graph,
    template_update,
)
from ..equipment.control import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput
from ..multimethods import multimethod

_namespace = S223


#
#   Function Inputs and Outputs
#


class ProducerInput(Node):
    _class_iri: URIRef = P223.ProducerInput
    hasCauseLocation: LocationReference

    def __init__(self, function_block: Producer, **kwargs: Any) -> None:
        logging.info(
            f"ProducerInput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasInput, self._node_iri))

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self


class ProducerOutput(Node):
    _class_iri: URIRef = P223.ProducerOutput
    hasEffectLocation: LocationReference

    def __init__(self, function_block: Producer, **kwargs: Any) -> None:
        logging.info(
            f"ProducerOutput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasOutput, self._node_iri))

    def add_hasEffectLocation(self, node: Node) -> None:
        # Must be from a sensor
        self.hasEffectLocation = node

        # link the two together
        self._data_graph.add((self._node_iri, P223.hasEffectLocation, node._node_iri))
        if INCLUDE_INVERSE:
            node.isEffectLocationOf = self

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self

    def __mod__(self, other: Node) -> Node:
        """This producer output has effect location on other node."""
        logging.debug(f"Container.__mod__ {self} % {other}")

        self.add_hasEffectLocation(other)
        return self


class FunctionInput(ProducerInput):
    _class_iri: URIRef = S223.FunctionInput


class FunctionOutput(ProducerOutput):
    _class_iri: URIRef = S223.FunctionOutput


@multimethod
def connect_mm(
    output_connector: ProducerOutput, input_connector: ProducerInput
) -> None:
    """ProducerOutput >> ProducerInput"""
    logging.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add(
        (output_connector._node_iri, S223.connect, input_connector._node_iri)
    )


@multimethod
def connect_mm(prop: Property, input_connector: ProducerInput) -> None:
    """Property >> ProducerInput"""
    logging.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(output_connector: ProducerOutput, prop: Property) -> None:
    """ProducerOutput >> Property"""
    logging.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector._node_iri, S223.produces, prop._node_iri))


@multimethod
def connect_mm(
    output_connector: FunctionOutput, input_connector: FunctionInput
) -> None:
    """ProducerOutput >> ProducerInput"""
    logging.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add(
        (output_connector._node_iri, S223.connect, input_connector._node_iri)
    )


@multimethod
def connect_mm(prop: Property, input_connector: FunctionInput) -> None:
    """Property >> ProducerInput"""
    logging.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, prop: Property) -> None:
    """ProducerOutput >> Property"""
    logging.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector._node_iri, S223.produces, prop._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: AnalogOutput) -> None:
    """ProducerOutput >> Property"""
    logging.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: BinaryOutput) -> None:
    """ProducerOutput >> Controller connection point"""
    logging.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: AnalogOutput) -> None:
    """ProducerOutput >> Controller connection point"""
    logging.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(input_connector: FunctionInput, cp: BinaryInput) -> None:
    """ProducerInput >> Controller connection point"""
    logging.info(f"connect from {input_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.isInputOf, input_connector._node_iri))


@multimethod
def connect_mm(input_connector: FunctionInput, cp: AnalogInput) -> None:
    """ProducerOutput >> Controller connection point"""
    logging.info(f"connect from {input_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.isInputOf, input_connector._node_iri))


#
#   Connector types, parameters, and constants
#


class G36AnalogInput(FunctionInput):
    _class_iri: URIRef = G36.AnalogInput


class G36AnalogOutput(FunctionOutput):
    _class_iri: URIRef = G36.AnalogOutput


class G36BinaryInput(FunctionInput):
    _class_iri: URIRef = G36.BinaryInput


class G36BinaryOutput(FunctionOutput):
    _class_iri: URIRef = G36.BinaryOutput


class Parameter(Node):
    _class_iri: URIRef = S223.Parameter
    _volatile = ("hasValue",)

    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        logging.debug(
            f"Parameter({self.__class__.__name__}).__init__ {value!r} {kwargs}"
        )

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        super().__init__(**kwargs)

        # if there is an initial value, link to it
        if init_value is not None:
            if not isinstance(init_value, Literal):
                init_value = Literal(init_value)
            self.hasValue = init_value


class Constant(Node):
    """
    Very similar to a Parameter, but a Constant does not have a volatile value.
    """

    _class_iri: URIRef = S223.Constant

    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        logging.debug(
            f"Constant({self.__class__.__name__}).__init__ {value!r} {kwargs}"
        )

        init_value = None
        if value is None:
            if "hasValue" in kwargs:
                init_value = kwargs.pop("hasValue")
        elif "hasValue" in kwargs:
            raise RuntimeError("initialization conflict")
        else:
            init_value = value

        super().__init__(**kwargs)

        # if there is an initial value, link to it
        if init_value is not None:
            if not isinstance(init_value, Literal):
                init_value = Literal(init_value)
            self.hasValue = init_value


class AnalogConstant(Constant):
    _class_iri: URIRef = None


class BinaryConstant(Constant):
    _class_iri: URIRef = None


#
#   Producer
#


class Producer(_Producer):
    """
    Producers are black boxes representing causality.
    Their inputs are causes and they produce an effect on a property
    It is very similar to a function, but it is meant to show the relation
    between an input and an output of something not-driven by an algorithm.
    A common example would be a relay. You feed it voltage and the relay contact
    is actuated.
    """

    _class_iri: URIRef = P223.Producer
    # _connectors: Dict[str, Connector]

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}

        logging.debug(f"Producer.__init__ {kwargs}")

        # resolve annotations if necessary
        if not self._resolved:
            self._resolve_annotations()
        logging.debug(f"    - continue Producer.__init__")

        # pull out the parameters and constants
        connector_inits: Dict[str, Any] = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and (attr_name in kwargs):
                if issubclass(attr_type, (ProducerInput, ProducerOutput)):
                    connector_inits[attr_name] = kwargs.pop(attr_name)
        logging.debug(f"    - connector_inits: {connector_inits}")
        logging.debug(f"    - remaining kwargs: {kwargs}")

        # continue with initialization
        super().__init__(_config, **kwargs)

        # instantiate and associate all of the connectors
        self._connectors = {}
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, (ProducerInput, ProducerOutput)):
                # build an instance of this connector
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._connectors[attr_name] = attr_element
                logging.debug(f"    - connector {attr_name}: {attr_element}")

                if attr_name in connector_inits:
                    logging.debug(f"        - init: {connector_inits[attr_name]}")
                    if issubclass(attr_type, ProducerInput):
                        connector_inits[attr_name] >> attr_element
                    if issubclass(attr_type, ProducerOutput):
                        attr_element >> connector_inits[attr_name]

                setattr(self, attr_name, attr_element)

    def uses(
        self,
        prop: Property,
        klass: ProducerInput = ProducerInput,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        prop >> connector

    def produces(
        self,
        prop: Property,
        klass: ProducerOutput = ProducerOutput,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        connector >> prop


# TODO : at some point their will be a clash where no label was given...


class FunctionBlock(Producer):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks have inputs and produce outputs that are
    related to observable and actuatable properties.
    Functions are executed by a s223:contoller
    """

    _class_iri: URIRef = S223.FunctionBlock
    # _connectors: Dict[str, Connector]
    _parameters: Dict[str, Parameter]

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"FunctionBlock.__init__ {kwargs}")

        # pull out the parameters and constants

        parameter_inits: Dict[str, Any] = {}

        # continue with initialization
        super().__init__(_config, **kwargs)

        # instantiate and associate all of the connectors and parameters
        self._parameters = {}
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, Parameter):
                # check if an instance was already created
                attr_element = getattr(self, attr_name, None)
                if not attr_element:
                    attr_element = attr_type(label=self.label + "." + attr_name)
                    setattr(self, attr_name, attr_element)

                self._parameters[attr_name] = attr_element
                logging.debug(f"    - parameter {attr_name}: {attr_element}")

                data_graph.add(
                    (self._node_iri, S223.hasParameter, attr_element._node_iri)
                )

                # give it a value or override the value
                if attr_name in parameter_inits:
                    logging.debug(f"        - init: {parameter_inits[attr_name]}")
                    attr_element.hasValue = parameter_inits[attr_name]

            elif issubclass(attr_type, Constant):
                # check if an instance was already created
                attr_element = getattr(self, attr_name, None)
                if not attr_element:
                    attr_element = attr_type(label=self.label + "." + attr_name)
                    setattr(self, attr_name, attr_element)

                self._parameters[attr_name] = attr_element
                logging.debug(f"    - constant {attr_name}: {attr_element}")

                data_graph.add(
                    (self._node_iri, S223.hasConstant, attr_element._node_iri)
                )

                # give it a value (might fail if annotation provided value)
                if attr_name in parameter_inits:
                    logging.debug(f"        - init: {parameter_inits[attr_name]}")
                    attr_element.hasValue = parameter_inits[attr_name]

    def uses(
        self,
        prop: Property,
        klass: FunctionInput = FunctionInput,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        prop >> connector

    def produces(
        self,
        prop: Property,
        klass: FunctionOutput = FunctionOutput,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        setattr(self, label, connector)
        connector >> prop
