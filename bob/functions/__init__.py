"""
Function Blocks

This is a facade for ASHRAE 231 Controls Description Language
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, AnyStr, Dict

from rdflib import URIRef  # type: ignore

from ..core import INCLUDE_INVERSE, Node, Property, data_graph, S223, P223, BOB
from ..multimethods import multimethod

_namespace = S223


class Connector(Node):
    """
    This is an abstract class that does not appear in the model and is just
    used to simplfy the modeling for properties to/from inputs and outputs.
    """

    _class_iri: URIRef = None

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        logging.debug(f"Connector.__init__ {function_block} {kwargs}")
        if "label" not in kwargs:
            raise ValueError("connector label required")
        if self.__class__ is Connector:
            raise RuntimeError("Connector is an abstract base class")

        super().__init__(**kwargs)

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self


class FunctionInput(Connector):
    _class_iri: URIRef = S223.FunctionInput

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)

        data_graph.add((function_block._node_iri, S223.hasInput, self._node_iri))


class FunctionOutput(Connector):
    _class_iri: URIRef = S223.FunctionOutput

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)

        data_graph.add((function_block._node_iri, S223.hasOutput, self._node_iri))


class Parameter(Node):
    _class_iri: URIRef = S223.Parameter

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)

        data_graph.add((function_block._node_iri, S223.hasParameter, self._node_iri))


class Constant(Parameter):
    _class_iri: URIRef = S223.Constant

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)


@multimethod
def connect_mm(function_output: FunctionOutput, function_input: FunctionInput) -> None:
    """FunctionOutput >> FunctionInput"""
    logging.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add((function_output._node_iri, S223.connect, function_input._node_iri))


@multimethod
def connect_mm(prop: Property, function_input: FunctionInput) -> None:
    """Property >> FunctionInput"""
    logging.info(f"connect from {prop} to {function_input}")

    # check to make sure it doesn't already use something
    uses_something = list(data_graph.objects(function_input._node_iri, S223.uses))
    if uses_something:
        raise RuntimeError(f"{function_input} already uses {uses_something[0]}")

    data_graph.add((function_input._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(function_output: FunctionOutput, prop: Property) -> None:
    """FunctionOutput >> Property"""
    logging.info(f"connect from {function_output} to {prop}")

    data_graph.add((function_output._node_iri, S223.produces, prop._node_iri))


@multimethod
def connect_mm(function_block: FunctionBlock, parameter: Parameter) -> None:
    """FunctionBlock >> Parameter"""
    logging.info(f"connect from {function_block} to {parameter}")

    data_graph.add((function_block._node_iri, S223.hasParameter, parameter._node_iri))
    if INCLUDE_INVERSE:
        data_graph.add(
            (parameter._node_iri, S223.isParameterOf, function_block._node_iri)
        )


@multimethod
def connect_mm(parameter: Parameter, function_block: FunctionBlock) -> None:
    """Parameter >> FunctionBlock"""
    logging.info(f"connect from {parameter} to {function_block}")

    data_graph.add((function_block._node_iri, S223.hasParameter, parameter._node_iri))
    if INCLUDE_INVERSE:
        data_graph.add(
            (parameter._node_iri, S223.isParameterOf, function_block._node_iri)
        )


#
#   Specialized inputs and outputs
#


class AnalogInput(FunctionInput):
    _class_iri: URIRef = S223.AnalogInput


class AnalogOutput(FunctionOutput):
    _class_iri: URIRef = S223.AnalogOutput


class BinaryInput(FunctionInput):
    _class_iri: URIRef = S223.BinaryInput


class BinaryOutput(FunctionOutput):
    _class_iri: URIRef = S223.BinaryOutput


#
#   Function Block
#


class FunctionBlock(Node):
    """
    In 223, function blocks are black boxes representing a sequence or
    an algorithm. Function blocks use inputs and produce outputs that can
    be related to observable and actuatable properties in the 223 model.

    Connections from or to a function block are made from/to properties only
    """

    _class_iri: URIRef = S223.FunctionBlock
    _connectors: Dict[str, Connector]
    _parameters: Dict[str, Parameter]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"FunctionBlock.__init__ {kwargs}")

        # pull out the parameters and constants
        parameter_inits: Dict[str, Any] = {}
        for attr_name, attr_type in self._nodes.items():
            if inspect.isclass(attr_type) and issubclass(attr_type, Parameter):
                if attr_name in kwargs:
                    parameter_inits[attr_name] = kwargs.pop(attr_name)
        logging.debug(f"    - parameter_inits: {parameter_inits}")
        logging.debug(f"    - remaining kwargs: {kwargs}")

        # continue with initialization
        super().__init__(**kwargs)

        # instantiate and associate all of the connectors and parameters
        self._connectors = {}
        self._parameters = {}
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, Connector):
                # build an instance of this connector
                attr_element = attr_type(self, label=self.label + "." + attr_name)
                self._connectors[attr_name] = attr_element
                logging.debug(f"    - connector {attr_name}: {attr_element}")

            elif issubclass(attr_type, Parameter):
                # build an instance of this parameter
                attr_element = attr_type(label=self.label + "." + attr_name)
                self._parameters[attr_name] = attr_element
                logging.debug(f"    - parameter {attr_name}: {attr_element}")

                if attr_name in parameter_inits:
                    logging.debug(f"        - init: {parameter_inits[attr_name]}")
            else:
                continue

            setattr(self, attr_name, attr_element)
