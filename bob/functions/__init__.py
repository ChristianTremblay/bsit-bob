"""
Function Blocks

This is a facade for ASHRAE 231 Controls Description Language
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from rdflib import URIRef  # type: ignore

from ..core import (
    bind_namespace,
    data_graph,
    INCLUDE_INVERSE,
    Node,
    Property,
    resolve_reference,
    s223,
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
    """

    node_type: URIRef = s223.FunctionBlock
    _connectors: Dict[str, Connector]
    _parameters: Dict[str, Parameter]

    def __init__(self, **kwargs: Any) -> None:
        logging.debug(f"FunctionBlock.__init__ {kwargs}")

        # merge the annotations
        merged_annotations = {}
        for cls in reversed(self.__class__.__mro__[:-1]):
            merged_annotations.update(cls.__annotations__)
        logging.debug(f"    - merged_annotations: {merged_annotations}")

        # pull out the parameters and constants
        parameter_inits: Dict[str, Any] = {}
        for kw_name, kw_value in kwargs.items():
            if kw_name in merged_annotations:
                var_annotation = merged_annotations[kw_name]
                if isinstance(var_annotation, str):
                    annotation_resolved = resolve_reference(var_annotation)
                    if not annotation_resolved:
                        logging.debug(
                            f"resolving {var_annotation!r} for attribute {kw_name!r}, class not found"
                        )
                        continue
                    var_annotation = annotation_resolved
                if issubclass(var_annotation, Parameter):
                    parameter_inits[kw_name] = kw_value
        for parm_name in parameter_inits:
            del kwargs[parm_name]
        logging.debug(f"    - parameter_inits: {parameter_inits}")
        logging.debug(f"    - remaining kwargs: {kwargs}")

        # continue with initialization
        super().__init__(**kwargs)

        # instantiate and associate all of the connectors and parameters
        self._connectors = {}
        self._parameters = {}
        for var_name, var_annotation in merged_annotations.items():
            if var_name.startswith("_"):
                continue
            var_label = self.label + "." + var_name

            if isinstance(var_annotation, str):
                annotation_resolved = resolve_reference(var_annotation)
                if not annotation_resolved:
                    logging.debug(
                        f"resolving {var_annotation!r} for attribute {var_name!r}, class not found"
                    )
                    continue
                var_annotation = annotation_resolved

            if issubclass(var_annotation, Connector):
                if var_name in self._connectors:
                    raise RuntimeError("existing connector")
                if var_name in self._parameters:
                    raise RuntimeError("existing parameter")

                var_element = var_annotation(self, label=var_label)
                logging.debug(f"    - connector {var_name}: {var_element}")

                self._connectors[var_name] = var_element

            elif issubclass(var_annotation, Parameter):
                if var_name in self._connectors:
                    raise RuntimeError("existing connector")
                if var_name in self._parameters:
                    raise RuntimeError("existing parameter")

                # maybe a value was provided
                var_value = parameter_inits.pop(var_name, None)
                var_element = var_annotation(self, value=var_value, label=var_label)
                logging.debug(f"    - parameter {var_name}: {var_element}")

                self._parameters[var_name] = var_element

            else:
                continue

            setattr(self, var_name, var_element)

    def uses_input(self, prop: Property) -> None:
        connector = InputConnector(self, label=f"{self.label}.input")
        prop >> connector

    def produces_output(self, prop: Property) -> None:
        connector = OutputConnector(self, label=f"{self.label}.output")
        connector >> prop


class ElementaryBlock(FunctionBlock):
    node_type: URIRef = s223.ElementaryBlock


class CompositeBlock(FunctionBlock):
    node_type: URIRef = s223.CompositeBlock
