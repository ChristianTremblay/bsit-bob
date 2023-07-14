"""
Function Blocks
"""

from __future__ import annotations

import inspect
import logging
from typing import Any, AnyStr, Dict

from rdflib import Literal, URIRef  # type: ignore

from .core import (
    BOB,
    G36,
    INCLUDE_INVERSE,
    P223,
    S223,
    Container,
    LocationReference,
    Node,
    Property,
    data_graph,
    template_update,
)
from .equipment.control import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput
from .multimethods import multimethod

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = S223


class FunctionInput(Node):
    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        _log.debug(
            f"FunctionInput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
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


class FunctionOutput(Node):
    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        _log.debug(
            f"FunctionOutput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

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


class Parameter(Node):
    _class_iri: URIRef = S223.Parameter
    _volatile = ("hasValue",)

    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        _log.debug(f"Parameter({self.__class__.__name__}).__init__ {value!r} {kwargs}")

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


class ParameterReference:
    def __new__(cls, parameter):
        if not isinstance(parameter, Parameter):
            raise TypeError(f"parameter expected: {parameter}")
        return parameter


class Constant(Node):
    """
    Very similar to a Parameter, but a Constant does not have a volatile value.
    """

    _class_iri: URIRef = S223.Constant

    hasValue: Literal

    def __init__(self, value: Any = None, **kwargs: Any):
        _log.debug(f"Constant({self.__class__.__name__}).__init__ {value!r} {kwargs}")

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


class ConstantReference:
    def __new__(cls, constant):
        if not isinstance(parameter, constant):
            raise TypeError(f"constant expected: {constant}")
        return constant


@multimethod
def connect_mm(
    output_connector: FunctionOutput, input_connector: FunctionInput
) -> None:
    """FunctionOutput >> FunctionInput"""
    _log.info(f"connect from {output_connector} to {input_connector}")

    data_graph.add(
        (output_connector._node_iri, S223.connect, input_connector._node_iri)
    )


@multimethod
def connect_mm(prop: Property, input_connector: FunctionInput) -> None:
    """Property >> FunctionInput"""
    _log.info(f"connect from {prop} to {input_connector}")

    data_graph.add((input_connector._node_iri, S223.uses, prop._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, prop: Property) -> None:
    """FunctionOutput >> Property"""
    _log.info(f"connect from {output_connector} to {prop}")

    data_graph.add((output_connector._node_iri, S223.produces, prop._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: AnalogOutput) -> None:
    """ProducerOutput >> Property"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: BinaryOutput) -> None:
    """FunctionOutput >> Controller binary output connection point"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(output_connector: FunctionOutput, cp: AnalogOutput) -> None:
    """FunctionOutput >> Controller analog output connection point"""
    _log.info(f"connect from {output_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.hasProducerOutput, output_connector._node_iri))


@multimethod
def connect_mm(input_connector: FunctionInput, cp: BinaryInput) -> None:
    """FunctionInput >> Controller connection point"""
    _log.info(f"connect from {input_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.isInputOf, input_connector._node_iri))


@multimethod
def connect_mm(input_connector: FunctionInput, cp: AnalogInput) -> None:
    """FunctionInput >> Controller connection point"""
    _log.info(f"connect from {input_connector} to {cp}")

    data_graph.add((cp._node_iri, P223.isInputOf, input_connector._node_iri))


#
#   Connector types, parameters, and constants
#


class G36AnalogInput(FunctionInput):
    _class_iri: URIRef = G36.AnalogInput


class G36AnalogOutput(FunctionOutput):
    _class_iri: URIRef = G36.AnalogOutput


class G36DigitalInput(FunctionInput):
    _class_iri: URIRef = G36.DigitalInput


class G36DigitalOutput(FunctionOutput):
    _class_iri: URIRef = G36.DigitalOutput


class AnalogConstant(Constant):
    _class_iri: URIRef = None


class BinaryConstant(Constant):
    _class_iri: URIRef = None


class FunctionBlock(Node):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks use inputs and produce outputs that are
    related to observable and actuatable properties.
    Functions are executed by a s223:Contoller.
    """

    _class_iri: URIRef = S223.FunctionBlock
    # _connectors: Dict[str, Connector]
    _parameters: Dict[str, Parameter]

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"FunctionBlock.__init__ {kwargs}")

        # pull out the parameters and constants
        parameter_inits: Dict[str, Any] = {}

        # continue with initialization
        # super().__init__(_config, **kwargs)
        super().__init__(**kwargs)

        # instantiate and associate all of the connectors and parameters
        self._parameters = {}
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, (FunctionInput, FunctionOutput)):
                # check if an instance was already created
                attr_element = getattr(self, attr_name, None)
                if not attr_element:
                    attr_element = attr_type(self, label=self.label + "." + attr_name)
                    setattr(self, attr_name, attr_element)
                _log.debug(f"    - input/output {attr_name}: {attr_element}")

            elif issubclass(attr_type, Parameter):
                # check if an instance was already created
                attr_element = getattr(self, attr_name, None)
                if not attr_element:
                    attr_element = attr_type(label=self.label + "." + attr_name)
                    setattr(self, attr_name, attr_element)

                self._parameters[attr_name] = attr_element
                _log.debug(f"    - parameter {attr_name}: {attr_element}")

                data_graph.add(
                    (self._node_iri, S223.hasParameter, attr_element._node_iri)
                )

                # give it a value or override the value
                if attr_name in parameter_inits:
                    _log.debug(f"        - init: {parameter_inits[attr_name]}")
                    attr_element.hasValue = parameter_inits[attr_name]

            elif issubclass(attr_type, Constant):
                # check if an instance was already created
                attr_element = getattr(self, attr_name, None)
                if not attr_element:
                    attr_element = attr_type(label=self.label + "." + attr_name)
                    setattr(self, attr_name, attr_element)

                self._parameters[attr_name] = attr_element
                _log.debug(f"    - constant {attr_name}: {attr_element}")

                data_graph.add(
                    (self._node_iri, S223.hasConstant, attr_element._node_iri)
                )

                # give it a value (might fail if annotation provided value)
                if attr_name in parameter_inits:
                    _log.debug(f"        - init: {parameter_inits[attr_name]}")
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
