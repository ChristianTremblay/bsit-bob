import logging
from typing import Any, Dict
from ..sensor import split_kwargs
from ..sensor.flow import FlowSetpoint
from ..sensor.temperature import TemperatureSetpoint
from ..core import (
    G36,
    UNIT,
    Air,
    DomainSpace,
    Node,
    PropertyReference,
    Substance,
    bind_namespace,
    Zone,
    template_update,
)
from ..properties import (
    OccupancyStatus,
    Schedule,
    Temperature,
    Percent,
    Flow,
    OnOffStatus,
    GasConcentration,
)
from ..property import ObservableProperty, QuantifiableObservableProperty
from . import (
    AnalogInput,
    AnalogOutput,
    BinaryInput,
    BinaryOutput,
    FunctionBlock,
    FunctionInput,
    FunctionOutput,
)

_namespace = G36


class G36Sequence(FunctionBlock):
    """
    This function is a subclass of a Function Block kept
    in the namespace of G36.

    In Guideline 36, models present the notion of AI, AO, BI, BO
    and those concept can be modeled using a Function block.
    Function block is then an abstraction of the sequence of
    operation suggested by G36.

    Comment of this block is the description of the sequence.
    """

    _class_iri = G36.FunctionBlock


class G36ZoneTemperatureControl(G36Sequence):
    _class_iri = G36.FunctionBlock


class G36AirFlowControl(G36Sequence):
    _class_iri = G36.FunctionBlock


class G36OccupancyControl(G36Sequence):
    _class_iri = G36.FunctionBlock


class G36VentilationAndCO2Control(G36Sequence):
    _class_iri = G36.FunctionBlock


# g36_4-1_VAV_TerminalUnit_CoolingOnly
class G36VAVCoolingOnly(G36Sequence):
    _class_iri = G36.VAVCoolingOnly
    # From table in section 4.1
    # Defined as Function Input and Output as we will connect
    # to existing properties in the model
    boxDamperPosition: FunctionOutput
    dischargeAirFlow: FunctionInput
    zoneTemperature: FunctionInput
    localOverride: FunctionInput
    zoneOccupancySensor: FunctionInput
    zonewindowSwitch: FunctionInput
    zoneSetpointAdj: FunctionInput
    zoneCO2: FunctionInput
    effectiveOccupancy: FunctionInput
    ahuSupplyAirTemp: FunctionInput

    ### PROPERTIES
    # Airflow setpoints
    zoneMaximumCoolingAirflowSetpoint: FlowSetpoint
    zoneMaximumHeatingAirflowSetpoint: FlowSetpoint

    # Temperature setpoint
    occupiedHtgSetpoint: TemperatureSetpoint
    occupiedClgSetpoint: TemperatureSetpoint
    unoccupiedHtgSetpoint: TemperatureSetpoint
    unoccupiedClgSetpoint: TemperatureSetpoint

    def __init__(self, config: Dict = None, **kwargs):
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        logging.debug(f"Fan.__init__ {_config} {kwargs}")

        super().__init__(_config, **kwargs)


class G36Figure_A_3(G36VAVCoolingOnly):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36Figure_A_2(G36VAVCoolingOnly):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)


class G36VAVCoolingOnly0(G36Sequence):
    def __init__(self, comment=None, **kwargs):
        super().__init__(comment=comment, **kwargs)

    _class_iri = G36.FunctionBlock


class G36ZoneGroup(Zone):
    _class_iri = G36.ZoneGroup


class G36ZoneFromZone(Zone):
    _class_iri = G36.Zone


class G36ZoneFromDomainSpace(DomainSpace):
    _class_iri = G36.Zone


VAV_CoolingOnly_template = {
    "cp": {
        "boxDamperPosition": FunctionOutput,
        "dischargeAirFlow": FunctionInput,
        "zoneTemperature": FunctionInput,
        "localOverride": FunctionInput,
        "zoneOccupancySensor": FunctionInput,
        "zonewindowSwitch": FunctionInput,
        "zoneSetpointAdj": FunctionInput,
        "zoneCO2": FunctionInput,
        "effectiveOccupancy": FunctionInput,
        "ahuSupplyAirTemp": FunctionInput,
    },
    "functions": {
        ("zoneTemperatureControl", G36ZoneTemperatureControl): {},
        ("airFlowControl", G36AirFlowControl): {},
        ("occupancyControl", G36OccupancyControl): {},
        ("ventilationAndCO2Control", G36VentilationAndCO2Control): {},
    },
}
