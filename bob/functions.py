"""
Function Blocks
"""

from __future__ import annotations

import inspect
import logging
from datetime import datetime
from typing import Any, AnyStr, Dict

from rdflib import Literal, URIRef, RDF  # type: ignore

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


class FunctionInput(Property):
    def __new__(cls, arg, **kwargs) -> Any:
        _log.debug(f"FunctionInput.__new__ {cls} {arg} {kwargs}")
        if isinstance(arg, Property):
            return arg
        elif isinstance(arg, FunctionBlock):
            return object.__new__(cls)
        elif isinstance(arg, (int, float, str, datetime)):
            return Property(arg)
        else:
            raise TypeError(f"property expected: {arg}")

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        _log.debug(
            f"FunctionInput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasInput, self._node_iri))


class FunctionOutput(Property):
    def __new__(cls, arg, **kwargs) -> Any:
        _log.debug(f"FunctionOutput.__new__ {cls} {arg} {kwargs}")
        if isinstance(arg, Property):
            return arg
        elif isinstance(arg, FunctionBlock):
            return object.__new__(cls)
        else:
            raise TypeError(f"property expected: {arg}")

    def __init__(self, function_block: FunctionBlock, **kwargs: Any) -> None:
        _log.debug(
            f"FunctionOutput({self.__class__.__name__}).__init__ {function_block} {kwargs}"
        )

        super().__init__(**kwargs)

        data_graph.add((function_block._node_iri, S223.hasOutput, self._node_iri))


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


class FunctionBlock(Node):
    """
    Function blocks are black boxes representing a sequence or an
    algorithm. Function blocks use inputs and produce outputs that are
    related to observable and actuatable properties.
    Functions are executed by a s223:Contoller.
    """

    _class_iri: URIRef = S223.FunctionBlock

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"FunctionBlock.__init__ {kwargs}")

        if not self._resolved:
            self._resolve_annotations()
        _log.debug("    - continue FunctionBlock.__init__")

        # super().__init__(_config, **kwargs)
        super().__init__(**kwargs)

        # instantiate and associate all of the inputs and outputs
        for attr_name, attr_type in self._nodes.items():
            if not inspect.isclass(attr_type):
                continue

            if issubclass(attr_type, (FunctionInput, FunctionOutput)):
                # check if an instance was passed as a kwarg
                attr_element = getattr(self, attr_name, None)
                if attr_element is None:
                    attr_element = attr_type(self, label=self.label + "." + attr_name)
                    _log.debug(f"    - setting {attr_name}: {attr_element}")
                    setattr(self, attr_name, attr_element)

                # if this is used as a function input/output, make it so
                if issubclass(attr_type, FunctionInput):
                    data_graph.add(
                        (self._node_iri, S223.hasInput, attr_element._node_iri)
                    )
                    data_graph.add(
                        (attr_element._node_iri, RDF.type, S223.FunctionInput)
                    )
                elif issubclass(attr_type, FunctionOutput):
                    data_graph.add(
                        (self._node_iri, S223.hasOutput, attr_element._node_iri)
                    )
                    data_graph.add(
                        (attr_element._node_iri, RDF.type, S223.FunctionOutput)
                    )

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
