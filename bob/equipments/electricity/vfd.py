from typing import Dict

from rdflib import URIRef

from bob.equipments.electricity import _VFD

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_575V_60HzInletConnectionPoint,
    Electricity_575V_60HzOutletConnectionPoint,
    EthernetBidirectionalConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    ConnectionPoint,
    Equipment,
    Property,
    logging,
    template_update,
)
from ...properties import (
    HP,
    RPM,
    Amps,
    ElectricPowerkW,
    NormalAlarmStatus,
    OnOffCommand,
    OnOffStatus,
    Percent,
    PercentCommand,
    PowerFactor,
    Temperature,
)

_namespace = BOB

vfd_template = {
    "cp": {
        "electricalInlet": Electricity_575V_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_575V_60HzOutletConnectionPoint,
        "ethernet_port": EthernetBidirectionalConnectionPoint,
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        ("amps", Amps): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("speed_reference", PercentCommand): {},
        ("rpm", RPM): {},
        ("motor_temp", Temperature): {},
        ("drive_running", OnOffStatus): {},
        ("run_command", OnOffCommand): {},
        ("alarm_status", NormalAlarmStatus): {},
    },
}


class VFD(_VFD):
    _class_iri: URIRef = S223.VFD

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(vfd_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"VFD.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
