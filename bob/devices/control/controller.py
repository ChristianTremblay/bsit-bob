from pyclbr import Function
from typing import Dict, Any

from rdflib import URIRef
from bob.functions import FunctionBlock
from bob.multimethods import multimethod

from bob.properties import Nm, Percent, PercentCommand
from bob.properties.states import OnOffCommand, OnOffStatus

from ...connections.electricity import (
    ModulationSignalInletConnectionPoint,
    ModulationSignalOutletConnectionPoint,
    OnOffSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
    RS485BidirectionalConnectionPoint,
    Electricity_24V_60HzInletConnectionPoint,
)

from ...core import (
    INCLUDE_INVERSE,
    data_graph,
    Device,
    Property,
    PropertyReference,
    logging,
    BOB,
    P223,
    S223,
    template_update,
)

from ...externalreference import NetworkProfile

_namespace = P223

# Controller
analogInput = ModulationSignalInletConnectionPoint
analogOutput = ModulationSignalOutletConnectionPoint
binaryInput = OnOffSignalInletConnectionPoint
binaryOutput = OnOffSignalOutletConnectionPoint
bacnet_mstp = RS485BidirectionalConnectionPoint

controller_template = {
    "cp": {
        "electricalInlet": Electricity_24V_60HzInletConnectionPoint,
        "zone_temperature_sensor": analogInput,
        "airflow_sensor": analogInput,
        "damper_output": analogOutput,
    },
    "properties": {},
}


class Controller(Device):
    """
    A controller executes function blocks and connect to other devices
    through different connection points (AI, AO, BI, BO)
    """

    _class_iri: URIRef = P223.Controller
    # electricalInlet: Electricity_24V_60HzInletConnectionPoint
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
def connect_mm(controller: Controller, network_device: NetworkProfile) -> None:
    """Controller >> FucntionBlock"""
    logging.info(f"connect from {controller} to {network_device}")

    data_graph.add(
        (controller._node_iri, P223.hasNetworkProfile, network_device._node_iri)
    )
    if INCLUDE_INVERSE:
        data_graph.add(
            (network_device._node_iri, P223.isNetworkProfileOf, controller._node_iri)
        )
