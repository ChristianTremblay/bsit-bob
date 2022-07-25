"""
Function Blocks

This is a facade for ASHRAE 231 Controls Description Language
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, AnyStr, Dict

from rdflib import Literal, URIRef  # type: ignore

from ..core import INCLUDE_INVERSE, S223, Node, Property, data_graph
from ..multimethods import multimethod

_namespace = S223


#
#   Function Inputs and Outputs
#


class FunctionInput(Node):
    _class_iri: URIRef = S223.FunctionInput

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
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


class FunctionOutput(Node):
    _class_iri: URIRef = S223.FunctionOutput

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasOutput, self._node_iri))

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self


@multimethod
def connect_mm(
    output_connector: FunctionOutput, input_connector: FunctionInput
) -> None:
    """FunctionOutput >> FunctionInput"""
    logging.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add(
        (output_connector._node_iri, S223.connect, input_connector._node_iri)
    )


@multimethod
def connect_mm(prop: Property, input_connector: FunctionInput) -> None:
    """Property >> FunctionInput"""
    logging.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, prop: Property) -> None:
    """FunctionOutput >> Property"""
    logging.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector._node_iri, S223.produces, prop._node_iri))


#
#   Connector types, parameters, and constants
#


class AnalogInput(FunctionInput):
    _class_iri: URIRef = S223.AnalogInput


class AnalogOutput(FunctionOutput):
    _class_iri: URIRef = S223.AnalogOutput


class BinaryInput(FunctionInput):
    _class_iri: URIRef = S223.BinaryInput


class BinaryOutput(FunctionOutput):
    _class_iri: URIRef = S223.BinaryOutput


class Parameter(Node):
    _class_iri: URIRef = S223.Parameter
    _volatile = ("hasValue",)

    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        logging.debug(f"{self.__class__.__name__}.__init__ {value!r} {kwargs}")

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


class Constant(Parameter):
    _class_iri: URIRef = S223.Constant


class AnalogConstant(Constant):
    _class_iri: URIRef = None


class BinaryConstant(Constant):
    _class_iri: URIRef = None


#
#   Function Block
#


class FunctionBlock(Node):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks have inputs and produce outputs that are
    related to observable and actuatable properties.
    """

    _class_iri: URIRef = S223.FunctionBlock
    # _connectors: Dict[str, Connector]
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

            if issubclass(attr_type, (FunctionInput, FunctionOutput)):
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

    def uses_input(
        self,
        prop: Property,
        klass: FunctionInput = FunctionInput,
        label: AnyStr = "input",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        prop >> connector

    def produces_output(
        self,
        prop: Property,
        klass: FunctionOutput = FunctionOutput,
        label: AnyStr = "output",
    ) -> None:
        connector = klass(self, label=f"{self.label}.{label}")
        connector >> prop
