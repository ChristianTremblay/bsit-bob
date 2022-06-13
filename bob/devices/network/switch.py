import logging
from typing import Dict

from rdflib import URIRef

from bob.properties.network import Mbit_per_seconds

from ...connections.air import AirInletConnectionPoint, AirOutletConnectionPoint
from ...connections.electricity import (
    Electricity_120V_60HzInletConnectionPoint,
    EthernetBidirectionalConnectionPoint,
)
from ...core import ConnectionPoint, Device, PropertyReference, quantitykind, s223, unit
from ...properties import HP, RPM, Amps, ElectricPowerkW, PowerFactor, Pressure
from ...properties.states import OnOffCommand, OnOffStatus
from ...property import QuantifiableObservableProperty

_namespace = s223

ip_switch_template = {
    "cp": {
        "electricalInlet": Electricity_120V_60HzInletConnectionPoint,
    },
    "properties": {},
}


class EthernetSwitch(Device):
    """
    An Ethernet Switch
    """

    _class_iri: URIRef = s223.EthernetSwitch

    def __init__(self, config: Dict = None, **kwargs):
        if "ports" in kwargs:
            _number_of_ports = int(kwargs.pop("ports"))
        else:
            raise ValueError("Please provide number of IP ports using ports=x")
        if "data_rate" in kwargs:
            _data_rate = float(kwargs.pop("data_rate"))
        else:
            raise ValueError("Please provide data rate using data_rate=x in Mbit/s")
        _config = ip_switch_template
        for i, each in enumerate(range(_number_of_ports)):
            _config["cp"][f"port{i}"] = EthernetBidirectionalConnectionPoint
        if config:
            _config.update(config)
        kwargs = {**_config.get("params", {}), **kwargs}
        super().__init__(_config, **kwargs)
        for k, v in self._connection_points.items():
            if isinstance(v, EthernetBidirectionalConnectionPoint):
                v.data_rate = Mbit_per_seconds(_data_rate)
