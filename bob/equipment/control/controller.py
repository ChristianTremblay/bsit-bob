from pyclbr import Function
from typing import Any, Dict

from rdflib import URIRef

from bob.multimethods import multimethod
from bob.producer import FunctionBlock
from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import (
    Electricity_24V_1Ph_60HzInletConnectionPoint,
)
from ...connections.network import (
    RS485BidirectionalConnectionPoint,
)
from ...core import (
    BOB,
    INCLUDE_INVERSE,
    P223,
    S223,
    Equipment,
    Property,
    PropertyReference,
    data_graph,
    logging,
    template_update,
)
from ...externalreference import NetworkProfile
from . import AnalogInput, AnalogOutput, BinaryInput, BinaryOutput

_namespace = P223

# empty, because other equipments can be defined as controller
# and I don't want them to inherit from example properties
controller_template = {
    "cp": {},
    "properties": {},
}

controller_template_example = {
    "cp": {
        "electricalInlet": Electricity_24V_1Ph_60HzInletConnectionPoint,
        "bacnet_mstp": RS485BidirectionalConnectionPoint,
        "zone_temperature_sensor": AnalogInput,
        "airflow_sensor": AnalogInput,
        "damper_output": AnalogOutput,
    },
    "properties": {},
}


class Controller(Equipment):
    """
    A controller executes function blocks and connect to other Equipment
    through different connection points (AI, AO, BI, BO)
    """

    _class_iri: URIRef = S223.Controller
    _attr_uriref = {"hasNetworkProfile": P223.hasNetworkProfile}
    # electricalInlet: Electricity_24V_1Ph_60HzInletConnectionPoint
    # executes: FunctionBlock
    hasNetworkProfile: NetworkProfile

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(controller_template, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"Controller.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)

    def executes(self, function_block: FunctionBlock):
        logging.debug(
            f"Controller {self._node_iri} executes  {function_block._node_iri}"
        )
        data_graph.add((self._node_iri, S223.executes, function_block._node_iri))

    def __rshift__(self, other: Any) -> Any:
        """Build a connection from this thing to another thing."""
        connect_mm(self, other)
        return other

    def __lshift__(self, other: Any) -> Any:
        """Build a connection to this thing from another thing."""
        connect_mm(other, self)
        return self


@multimethod
def connect_mm(controller: Controller, function_block: FunctionBlock) -> None:
    """Controller >> FucntionBlock"""
    logging.info(f"connect from {controller} to {function_block}")

    data_graph.add((controller._node_iri, P223.executes, function_block._node_iri))
    if INCLUDE_INVERSE:
        data_graph.add(
            (function_block._node_iri, P223.isExecutedBy, controller._node_iri)
        )


@multimethod
def connect_mm(controller: Controller, network_Equipment: NetworkProfile) -> None:
    """Controller >> FucntionBlock"""
    logging.info(f"connect from {controller} to {network_Equipment}")

    data_graph.add(
        (controller._node_iri, P223.hasNetworkProfile, network_Equipment._node_iri)
    )
    if INCLUDE_INVERSE:
        data_graph.add(
            (network_Equipment._node_iri, P223.isNetworkProfileOf, controller._node_iri)
        )
