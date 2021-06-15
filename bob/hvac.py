"""
HVAC Domain
"""

from __future__ import annotations

from typing import Any

from .core import (
    s223,
    Connection,
    ConnectionPoint,
    Device,
    InletConnectionPoint,
    InletSystemConnectionPoint,
    InletZoneConnectionPoint,
    OutletConnectionPoint,
    OutletSystemConnectionPoint,
    OutletZoneConnectionPoint,
    DomainSpace,
    Substance,
    System,
    SystemConnectionPoint,
    Zone,
    ZoneConnectionPoint,
)
from .signal import AnalogIn, AnalogOut

__namespace__ = s223


#
#  Air
#

Air = Substance(node_iri=s223.Air)


class AirConnection(Connection):
    hasSubstance = Air
    node_type = None


class AirConnectionPoint(ConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletConnectionPoint(AirConnectionPoint, InletConnectionPoint):
    node_type = None


class AirOutletConnectionPoint(AirConnectionPoint, OutletConnectionPoint):
    node_type = None


class AirSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletSystemConnectionPoint(
    AirSystemConnectionPoint, InletSystemConnectionPoint
):
    node_type = None


class AirOutletSystemConnectionPoint(
    AirSystemConnectionPoint, OutletSystemConnectionPoint
):
    node_type = None


class AirZoneConnectionPoint(ZoneConnectionPoint):
    hasSubstance = Air
    node_type = None


class AirInletZoneConnectionPoint(AirZoneConnectionPoint, InletZoneConnectionPoint):
    node_type = None


class AirOutletZoneConnectionPoint(AirZoneConnectionPoint, OutletZoneConnectionPoint):
    node_type = None


#
#   ChilledWater
#

ChilledWater = Substance(node_iri=s223.ChilledWater)


class ChilledWaterConnection(Connection):
    hasSubstance = ChilledWater
    node_type = None


class ChilledWaterConnectionPoint(ConnectionPoint):
    hasSubstance = ChilledWater
    node_type = None


class ChilledWaterInletConnectionPoint(
    InletConnectionPoint, ChilledWaterConnectionPoint
):
    node_type = None


class ChilledWaterOutletConnectionPoint(
    OutletConnectionPoint, ChilledWaterConnectionPoint
):
    node_type = None


class ChilledWaterSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = ChilledWater
    node_type = None


class ChilledWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


class ChilledWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, ChilledWaterSystemConnectionPoint
):
    node_type = None


#
#   HotWater
#

HotWater = Substance(node_iri=s223.HotWater)


class HotWaterConnection(Connection):
    hasSubstance = HotWater
    node_type = None


class HotWaterConnectionPoint(ConnectionPoint):
    hasSubstance = HotWater
    node_type = None


class HotWaterInletConnectionPoint(InletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterOutletConnectionPoint(OutletConnectionPoint, HotWaterConnectionPoint):
    node_type = None


class HotWaterSystemConnectionPoint(SystemConnectionPoint):
    hasSubstance = HotWater
    node_type = None


class HotWaterInletSystemConnectionPoint(
    InletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


class HotWaterOutletSystemConnectionPoint(
    OutletSystemConnectionPoint, HotWaterSystemConnectionPoint
):
    node_type = None


#
#   Spaces and Zones
#


class HVACZone(Zone):
    """
    An HVAC Zone with and supply and return air connection points.
    """

    supplyAir: AirInletZoneConnectionPoint
    returnAir: AirOutletZoneConnectionPoint


class HVACZone1(HVACZone):
    """
    HVAC Zone Type 1

    A simple HVAC Zone with a single space.
    """

    node_type = None

    def __init__(self, label: str) -> None:
        super().__init__(label=label)

        # there is a space that is the destination of the air
        space = DomainSpace(label=label + ".space")

        self.supplyAir.mapsTo = AirInletConnectionPoint(
            space, label=label + ".space.supplyAir"
        )
        self.returnAir.mapsTo = AirOutletConnectionPoint(
            space, label=label + ".space.returnAir"
        )


#
#   Devices and Systems
#


class Fan(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint


class Damper(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    position = AnalogOut


class Filter(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    dp = AnalogIn


class AirFlowStation(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    flow = AnalogIn


class ChilledWaterValve(Device):
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint
    position = AnalogOut


class ChilledWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    chilledWaterInlet: ChilledWaterInletConnectionPoint
    chilledWaterOutlet: ChilledWaterOutletConnectionPoint


class ChilledWaterCoil2(System):
    """
    Chilled Water Coil Type 2

    This is an example of a chilled water coil as a system that contains a
    chilled water valve device and makes the valve position available as its
    own analog output signal.
    """

    node_type = None

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    chilledWaterSupply: ChilledWaterInletSystemConnectionPoint
    chilledWaterReturn: ChilledWaterOutletSystemConnectionPoint
    chilledWaterValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a chilled water coil
        self.chilled_water_coil = ChilledWaterCoil(label=self.label + ".cw_coil")
        self.airInlet.mapsTo = self.chilled_water_coil.airInlet
        self.airOutlet.mapsTo = self.chilled_water_coil.airOutlet

        # create a chilled water valve
        self.chilled_water_valve = ChilledWaterValve(label=self.label + ".cw_valve")
        self.chilledWaterSupply.mapsTo = self.chilled_water_valve.chilledWaterInlet
        self.chilledWaterReturn.mapsTo = self.chilled_water_coil.chilledWaterOutlet

        # connect the valve to the coil
        self.chilled_water_valve >> self.chilled_water_coil

        # reference the valve position
        self.chilledWaterValvePosition = self.chilled_water_valve.position


class HotWaterValve(Device):
    hotWaterInlet: HotWaterInletConnectionPoint
    hotWaterOutlet: HotWaterOutletConnectionPoint
    position = AnalogOut


class HotWaterCoil(Device):
    airInlet: AirInletConnectionPoint
    airOutlet: AirOutletConnectionPoint
    hotWaterSupply: HotWaterInletConnectionPoint
    hotWaterReturn: HotWaterOutletConnectionPoint


class HotWaterBoiler(Device):
    hotWaterSupply: HotWaterOutletConnectionPoint
    hotWaterReturn: HotWaterInletConnectionPoint


class HotWaterCoil2(System):
    """
    This is an example of a hot water coil that contains a hot water valve
    device and makes the valve position available as its own analog output
    signal.
    """

    node_type = None

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    hotWaterSupply: HotWaterInletSystemConnectionPoint
    hotWaterReturn: HotWaterOutletSystemConnectionPoint
    hotWaterValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self.airInlet.mapsTo = self.hot_water_coil.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self.hotWaterSupply.mapsTo = self.hot_water_valve.hotWaterInlet
        self.hot_water_valve >> self.hot_water_coil
        self.hotWaterReturn.mapsTo = self.hot_water_coil.hotWaterReturn

        # reference the valve position
        self.hotWaterValvePosition = self.hot_water_valve.position


class VAV(System):
    """
    Variable Air Volume Terminal Unit
    """

    pass


class VAV1(VAV):
    """
    VAV Type 1

    This system contains an air flow station upstream of a damper.
    """

    node_type = None

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # link the air pieces together
        self.air_flow_station >> self.damper

        # reference the connections
        self.airInlet.mapsTo = self.air_flow_station.airInlet
        self.airOutlet.mapsTo = self.damper.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position


class VAV2(VAV):
    """
    VAV Type 2

    This system contains an air flow station, damper, and a reheat hot water
    coil.
    """

    node_type = None

    airInlet: AirInletSystemConnectionPoint
    airOutlet: AirOutletSystemConnectionPoint
    airFlow: AnalogIn
    damperPosition: AnalogOut
    hotWaterValvePosition: AnalogOut

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # create an air flow station
        self.air_flow_station = AirFlowStation(label=self.label + ".air_flow_station")
        self > self.air_flow_station

        # create a damper
        self.damper = Damper(label=self.label + ".damper")
        self > self.damper

        # create a hot water coil
        self.hot_water_coil = HotWaterCoil(label=self.label + ".hw_coil")
        self > self.hot_water_coil

        # create a hot water valve
        self.hot_water_valve = HotWaterValve(label=self.label + ".hw_valve")
        self > self.hot_water_valve

        # link them together
        self.air_flow_station.airOutlet >> self.damper.airInlet
        self.damper >> self.hot_water_coil

        # link the hot water pieces together
        self.hot_water_valve >> self.hot_water_coil

        # reference the connections
        self.airInlet.mapsTo = self.air_flow_station.airInlet
        self.airOutlet.mapsTo = self.hot_water_coil.airOutlet
        self.airFlow = self.air_flow_station.flow
        self.damperPosition = self.damper.position
        self.hotWaterValvePosition = self.hot_water_valve.position
