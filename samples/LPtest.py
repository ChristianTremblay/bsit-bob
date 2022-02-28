from pathlib import Path

from typing import Any

from bob.core import (
    bind_model_namespace,
    DomainSpace,
    PhysicalSpace,
    Device,
    System,
    Zone,
    Node,
    s223,
    ConnectionPoint,
    Connection,
    Segment,
    Junction,
    dump,
)
from bob.devices.hvac.damper import (
    Damper,
)
from bob.devices.hvac import (
    Fan,
)
from bob.connections.air import (
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
    AirOutletZoneConnectionPoint,
)
from bob.devices.hvac.coil import (
    ChilledWaterCoil,
)
from bob.space.hvac import (
    HVACZone,
)
from bob.devices.hvac.airflowstation import (
    AirFlowMonitor,
)
from bob.devices.hvac.filter import (
    Filter,
)
from bob.role import (
    Exhaust,
    Supply,
)
from bob.signal import (
    AnalogOut,
    AnalogIn,
)

# from header import g36_header


model_name = Path(__file__).stem
__namespace__ = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")


class TemperatureSensor(Device):
    connection: AirInletConnectionPoint
    temperature = AnalogIn

    # not sure about this at all, should be air inlet outlet, something else? If I make it one of the directional connections, which?
    # Should a temperature output be its own property?


class RooftopUnit(System):
    returnAirInlet: AirInletSystemConnectionPoint
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    # should I put the basic command and feedback in the class here?

    # not doing sensors yet
    # deciding not to use self, if I need ot access the RTU outside of this class it'd probably be good to have, but will I?
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        return_fan = Fan(label=self.label + ".return_fan")
        # return_fan.hasRole = Return
        self.returnAirInlet.mapsTo = return_fan.airInlet
        return_air = AirConnection(label=self.label + ".return_air")
        return_fan >> return_air

        # making backdraft damper (exhaust damper) and connecting it
        ea_damper = Damper(label=self.label + ".exhaust_air_damper")
        return_air >> ea_damper
        self.exhaustAirOutlet.mapsTo = ea_damper.airOutlet

        mixed_air_damper = Damper(label=self.label + ".mixed_air_damper")
        mixed_air = AirConnection(label=self.label + ".mixed_air")

        oa_damper = Damper(label=self.label + ".outside_air_damper")
        self.outsideAirInlet.mapsTo = oa_damper.airInlet
        # connecting damper directly to flow station, not indicating OA air
        oa_flow_station = AirFlowMonitor(label=self.label + ".outside_air_flow_station")
        oa_damper >> oa_flow_station >> mixed_air

        pre_filter = Filter(label=self.label + ".pre_filter")
        # filter has one connection, making new air to connect to bypass and coil
        pre_filtered_air = AirConnection(label=self.label + ".pre_filtered_air")
        mixed_air >> pre_filter >> pre_filtered_air

        bp_damper = Damper(label=self.label + ".bypass_damper")
        # schematic has an iso valve but I don't think that's what chilledWaterCoil2 is talking about
        cwc = ChilledWaterCoil(label=self.label + ".chilled_water_coil")
        # both the damper and air need to go into a filter, air as a medium?
        chilled_air = AirConnection(label=self.label + ".chilled_air")
        pre_filtered_air >> bp_damper >> chilled_air
        pre_filtered_air >> cwc >> chilled_air

        # connect via air connections or create junctions/segments in the ducts?

        final_filter = Filter(label=self.label + ".final_filter")
        supply_fan = Fan(label=self.label + ".supply_fan")
        supply_fan.hasRole = Supply
        chilled_air >> final_filter >> supply_fan

        iso_damper = Damper(label=self.label + ".iso_damper")
        supply_fan >> iso_damper

        self.supplyAirOutlet.mapsTo = iso_damper.airOutlet

        # ALTERNATIVELY
        pre_filtered = Segment()
        sensor = TemperatureSensor(label=self.label + ".MA_sensor")
        pre_filtered.link_to(sensor.connection)


# make an instance

r = RooftopUnit(node_iri=ex.rtu, label="rtu")
# g36_header(model_name)
dump()
