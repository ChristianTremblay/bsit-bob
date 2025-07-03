"""
Function Blocks
"""

from __future__ import annotations

import inspect
import logging
from datetime import datetime
from typing import Any, AnyStr, Dict, Union

from rdflib import URIRef  # type: ignore

from .core import (
    G36,
    S223,
    Node,
    Property,
    PropertyReference,
    data_graph,
)
from .template import template_update

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = S223


class FunctionInput(PropertyReference):
    def __new__(cls, arg: Any = None, **kwargs) -> Any:
        _log.debug(f"FunctionInput.__new__ {cls} {arg} {kwargs}")
        if (arg is None) or (arg == ()):
            obj = Property(**kwargs)
        elif isinstance(arg, Property):
            obj = arg
        elif isinstance(arg, (int, float, str, datetime)):
            obj = Property(arg, **kwargs)

        else:
            raise TypeError(f"property expected: {arg}")

        return obj


class FunctionOutput(PropertyReference):
    def __new__(cls, arg: Any = None, **kwargs) -> Any:
        _log.debug(f"FunctionOutput.__new__ {cls} {arg} {kwargs}")
        if (arg is None) or (arg == ()):
            obj = Property(**kwargs)
        elif isinstance(arg, Property):
            obj = arg
        elif isinstance(arg, (int, float, str, datetime)):
            obj = Property(arg, **kwargs)
        else:
            raise TypeError(f"property expected: {arg}")

        return obj


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


class Function(Node):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks use inputs and produce outputs that are
    related to observable and actuatable properties.
    Functions are executed by a s223:Contoller.
    """

    _class_iri: URIRef = S223.Function

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"Function.__init__ {kwargs}")
        self.inputs = {}
        self.outputs = {}

        if not self._resolved:
            self._resolve_annotations()
        _log.debug("    - continue Function.__init__")

        # super().__init__(_config, **kwargs)
        super().__init__(**kwargs)

    def __setattr__(
        self, attr: str, value: Any, klass: Union[FunctionInput, FunctionOutput] = None
    ) -> None:
        """
        .
        """
        super().__setattr__(attr, value)
        # A property can be use as a function input on multiple functions, so we
        # need to keep track of the functions that use this property as an input.
        if klass is None:
            klass = self.__annotations__.get(attr)
        if klass == FunctionInput:
            if not hasattr(value, "_is_function_input_of"):
                value._is_function_input_of = set()
            self.inputs[attr] = value
            data_graph.add((self._node_iri, S223.hasInput, value._node_iri))
        elif klass == FunctionOutput:
            if not hasattr(value, "_is_function_output_of"):
                value._is_function_output_of = set()
            self.outputs[attr] = value
            data_graph.add((self._node_iri, S223.hasOutput, value._node_iri))




    def hasInput(
        self,
        prop: Property,
        attr: AnyStr = None, 
        klass: FunctionInput = FunctionInput,
    ) -> None:
        label = f"{prop.label}" if attr is None else attr
        function_input_ref = klass(prop, function=self, label=label)
        self.__setattr__(label, function_input_ref, klass=klass)

    def hasOutput(
        self,
        prop: Property,
        attr: AnyStr = None, 
        klass: FunctionOutput = FunctionOutput,
    ) -> None:
        label = f"{prop.label}" if attr is None else attr
        function_output_ref = klass(prop, function=self, label=label)
        self.__setattr__(label, function_output_ref, klass=klass)

    #   Convenience methods for hasInput and hasOutput for retro-compatibility
    #   with the old FunctionInput and FunctionOutput classes
    def uses(self, *args, **kwargs) -> FunctionInput:
        self.hasInput(*args, **kwargs)

    def produces(self, *args, **kwargs) -> FunctionOutput:
        self.hasOutput(*args, **kwargs)
