"""
Function Blocks

This is a facade for ASHRAE 231 Controls Description Language
"""

from __future__ import annotations

import inspect
import logging

from typing import Any, Dict, AnyStr

from rdflib import URIRef  # type: ignore

from ..core import (
    INCLUDE_INVERSE,
    Node,
    Property,
    s223,
    data_graph,
)
from ..multimethods import multimethod

_namespace = s223


#
#   Connectors
#


class Connector(Node):
    node_type: URIRef = s223.Connector

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


class InputConnector(Connector):
    node_type: URIRef = s223.InputConnector

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)

        data_graph.add((function_block.node, s223.input, self.node))


class OutputConnector(Connector):
    node_type: URIRef = s223.OutputConnector

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(function_block, **kwargs)

        data_graph.add((function_block.node, s223.output, self.node))


@multimethod
def connect_mm(
    output_connector: OutputConnector, input_connector: InputConnector
) -> None:
    """OutputConnector >> InputConnector"""
    logging.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add((output_connector.node, s223.connect, input_connector.node))


@multimethod
def connect_mm(prop: Property, input_connector: InputConnector) -> None:
    """Property >> InputConnector"""
    logging.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector.node, s223.usesInput, prop.node))
    if INCLUDE_INVERSE:
        data_graph.add((prop.node, s223.isUsedAsInputBy, input_connector.node))


@multimethod
def connect_mm(output_connector: OutputConnector, prop: Property) -> None:
    """OutputConnector >> Property"""
    logging.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector.node, s223.producesOutput, prop.node))
    if INCLUDE_INVERSE:
        data_graph.add((prop.node, s223.isProducedBy, output_connector.node))


#
#   Connector types, parameters, and constants
#


class AnalogInput(InputConnector):
    node_type: URIRef = s223.AnalogInput


class AnalogOutput(OutputConnector):
    node_type: URIRef = s223.AnalogOutput


class BinaryInput(InputConnector):
    node_type: URIRef = s223.BinaryInput


class BinaryOutput(OutputConnector):
    node_type: URIRef = s223.BinaryOutput


class Parameter(Node):
    node_type: URIRef = s223.Parameter


class Constant(Parameter):
    node_type: URIRef = s223.Constant


class AnalogConstant(Constant):
    node_type: URIRef = None


class BinaryConstant(Constant):
    node_type: URIRef = None


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

    node_type: URIRef = s223.FunctionBlock
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
                attr_element = attr_type(label=self.label + "." + attr_name)
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

    def uses_input(
        self,
        prop: Property,
        klass: InputConnector = InputConnector,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        prop >> connector

    def produces_output(
        self,
        prop: Property,
        klass: OutputConnector = OutputConnector,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        connector >> prop


class ElementaryBlock(FunctionBlock):
    node_type: URIRef = s223.ElementaryBlock


class CompositeBlock(FunctionBlock):
    node_type: URIRef = s223.CompositeBlock
