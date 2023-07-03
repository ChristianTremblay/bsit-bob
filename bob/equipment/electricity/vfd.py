from typing import Dict

from rdflib import URIRef

from bob.equipment.control.controller import Controller
from bob.equipment.electricity import _VFD
from bob.producer import FunctionBlock, FunctionInput, FunctionOutput
from bob.producer.causality import Causality
from bob.properties.electricity import Frequency, Volts
from bob.sensor.electricity import CurrentSensor, VoltageSensor
from bob.sensor.motion import PositionSensor

from ...connections.electricity import (
    ElectricalInletConnectionPoint,
    ElectricalOutletConnectionPoint,
    Electricity_600VLL_3Ph_60HzInletConnectionPoint,
    Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
)
from ...connections.controlsignal import (
    ModulationSignalInletConnectionPoint,
    OnOffSignalOutletConnectionPoint,
)
from ...connections.network import (
    RS485BidirectionalConnectionPoint,
    EthernetBidirectionalConnectionPoint,
)
from ...core import (
    BOB,
    P223,
    S223,
    ConnectionPoint,
    Equipment,
    Property,
    PropertyReference,
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

# logging
_log = logging.getLogger(__name__)

# namespace
_namespace = BOB


class VFD_FB(FunctionBlock):
    _class_iri = BOB.VFDFunctionBlock

    speed_ref: FunctionInput
    amps_load: FunctionInput
    volts_load: FunctionInput
    frequency_load: FunctionOutput
    kW_load: FunctionOutput
    alarm: FunctionOutput
    rpm: FunctionOutput
    drive_running: FunctionOutput
    speed_ref_percent: FunctionOutput


vfd_template = {
    "cp": {
        "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
        "electricalOutlet": Electricity_600VLL_3Ph_60HzOutletConnectionPoint,
        "ethernet_port": EthernetBidirectionalConnectionPoint,
        "mstp_port": RS485BidirectionalConnectionPoint,
        "speedrefInlet": ModulationSignalInletConnectionPoint,
        "drive_running_dry_contact": OnOffSignalOutletConnectionPoint,
        "alarm_dry_contact": OnOffSignalOutletConnectionPoint,
    },
    "properties": {
        # ("actuatesProperty", PercentCommand): {},
        # ("amps", PropertyReference): {},
        # ("volts", PropertyReference): {},
        ("hp", HP): {},
        ("kW", ElectricPowerkW): {},
        ("frequency", Frequency): {},
        ("speed_reference", PercentCommand): {},
        ("rpm", RPM): {},
        ("motor_temp", Temperature): {},
        ("drive_running", OnOffStatus): {},
        ("run_command", OnOffCommand): {},
        ("alarm_status", NormalAlarmStatus): {},
    },
    "parts": {
        ("motor_temp_effect", Causality): {},
        ("current_sensor", CurrentSensor): {},
        ("voltage_sensor", VoltageSensor): {},
        ("speed_ref_voltage_sensor", VoltageSensor): {},
        ("controller_function_block", VFD_FB): {},
    },
}


class VFD(_VFD):
    _class_iri: URIRef = S223.VFD
    amps: PropertyReference
    volts: PropertyReference

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update(vfd_template, config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"VFD.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
        self["current_sensor"] % self.electricalOutlet
        self.amps = self["current_sensor"].observedProperty
        self["voltage_sensor"] % self.electricalOutlet
        self.volts = self["voltage_sensor"].observedProperty
        self["speed_ref_voltage_sensor"] % self.speedrefInlet

        # Feed the controller
        self.executes = self["controller_function_block"]
        (
            self["speed_ref_voltage_sensor"].observedProperty
            >> self["controller_function_block"].speed_ref
        )
        self["controller_function_block"].amps_load << self.amps
        self["controller_function_block"].volts_load << self.volts

        # Controlle rmkaes its job
        self["controller_function_block"].frequency_load >> self["frequency"]
        self["controller_function_block"].frequency_load % self.electricalOutlet
        self["controller_function_block"].kW_load >> self["kW"]
        self["controller_function_block"].rpm >> self["rpm"]
        self["controller_function_block"].alarm >> self["alarm_status"]
        self["controller_function_block"].alarm % self.alarm_dry_contact
        self["controller_function_block"].drive_running >> self["drive_running"]
        self["controller_function_block"].drive_running % self.drive_running_dry_contact
        self["controller_function_block"].speed_ref_percent >> self["speed_reference"]
        # No controller ... simple causality
        # in fact motor temp is the result of a calculation... but this shows a possibility
        self["motor_temp_effect"].cause_input << self["rpm"]
        self["motor_temp_effect"].effect_output >> self["motor_temp"]
