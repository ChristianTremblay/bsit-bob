from pathlib import Path

from typing import Any

from bob import bind_model_namespace, dump
from bob.core import (
    DomainSpace,
    PhysicalSpace,
    System,
    Zone,
    Node,
    s223,
    ConnectionPoint,
    Connection,
    Segment,
    Junction,
    QuantifiableObservableProperty,
    bind_namespace,
    Substance,
)
from bob.hvac import (
    Damper,
    Fan,
    AirConnection,
    AirInletConnectionPoint,
    AirInletSystemConnectionPoint,
    AirInletZoneConnectionPoint,
    AirOutletConnectionPoint,
    AirOutletSystemConnectionPoint,
    AirOutletZoneConnectionPoint,
    ChilledWaterCoil,
    HVACZone1,
    HVACZone,
    AirFlowStation,
    Device,
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
from rdflib import Namespace, URIRef, BNode, Literal, RDF, RDFS, XSD

# from header import g36_header


model_name = Path(__file__).stem
__namespace__ = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")

qudt = bind_namespace("qudt", "http://qudt.org/schema/qudt/")
quantitykind = bind_namespace("quantitykind", "http://qudt.org/vocab/quantitykind/")

Air = Substance(node_iri=s223.Air)


class TemperatureSensor(Device):
    node_type: URIRef = s223.sensor
    temperature = QuantifiableObservableProperty  # Should this be an AnalogIn???
    temperature.hasQuantityKind = quantitykind.Temperature

    hasMeasurementLocation: Connection  # this is a questionable choice


class RooftopUnit(System):
    returnAirInlet: AirInletSystemConnectionPoint
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    # should I put the basic command and feedback in the class here?

    # deciding not to use self, if I need ot access the RTU outside of this class it'd probably be good to have, but will I?
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.outsideAirInlet.mapsTo = Junction()
        mixed_air_damper = Damper(label=self.label + ".mixed_air_damper")
        mixed_air = AirConnection(label=self.label + ".mixed_air")

        iso_damper = Damper(label=self.label + ".iso_damper")
        # supply_fan >> iso_damper

        # self.supplyAirOutlet.mapsTo = iso_damper.airOutlet
        j = Junction(label=self.label + ".RTU_supply_outlet")
        j << (iso_damper.airOutlet)
        self.supplyAirOutlet.mapsTo = (
            j  # if I don't map it to a junction, then it doesn't connect to the plenum
        )

        sensor = TemperatureSensor(label=self.label + ".MA_sensor")
        sensor.hasMeasurementLocation = mixed_air  # This seems weird, but I kind of like it. You're measuring the mixed air connection

        # return_fan = Fan(label=self.label + ".return_fan")
        # #return_fan.hasRole = Return
        # self.returnAirInlet.mapsTo = return_fan.airInlet
        # return_air = AirConnection(label=self.label + ".return_air")
        # return_fan >> return_air

        # #making backdraft damper (exhaust damper) and connecting it
        # ea_damper= Damper(label=self.label + ".exhaust_air_damper")
        # return_air>>ea_damper
        # self.exhaustAirOutlet.mapsTo = ea_damper.airOutlet

        # oa_damper = Damper(label=self.label + ".outside_air_damper")
        # self.outsideAirInlet.mapsTo = oa_damper.airInlet
        # #connecting damper directly to flow station, not indicating OA air
        # oa_flow_station = AirFlowStation(label=self.label + ".outside_air_flow_station")
        # oa_damper >> oa_flow_station >> mixed_air

        # pre_filter = Filter(label=self.label + '.pre_filter')
        # #filter has one connection, making new air to connect to bypass and coil
        # pre_filtered_air = AirConnection(label=self.label + ".pre_filtered_air")
        # mixed_air >> pre_filter >> pre_filtered_air

        # bp_damper = Damper(label=self.label + ".bypass_damper")
        # #schematic has an iso valve but I don't think that's what chilledWaterCoil2 is talking about
        # cwc = ChilledWaterCoil(label=self.label + ".chilled_water_coil")
        # #both the damper and air need to go into a filter, air as a medium?
        # chilled_air = AirConnection(label=self.label+".chilled_air")
        # pre_filtered_air>>bp_damper>>chilled_air
        # pre_filtered_air>>cwc>>chilled_air

        # #connect via air connections or create junctions/segments: Why create junctions when I can make multiple things connect too or from an AirConnection?

        # final_filter = Filter(label=self.label + '.final_filter')
        # supply_fan = Fan(label=self.label + '.supply_fan')
        # supply_fan.hasRole = Supply
        # chilled_air>>final_filter>>supply_fan


# Should a plenum be a segment or is system correct??
class Plenum(System):
    AirInlet: AirInletSystemConnectionPoint  # would the outlet be a junction, or just connection points??
    AirOutlet: AirOutletSystemConnectionPoint
    hasSubstance = Air

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        j = Junction(label=self.label + ".inlet")
        # j.hasSubstance = Air
        j2 = Junction(label=self.label + ".outlet")
        # j2.hasSubstance = Air #If the junction has a substance, then it doesn't connect. Am I just doing this wrong??
        self.AirInlet.mapsTo = j
        self.AirOutlet.mapsTo = j2


# make an instance
class HVACZone2(HVACZone):
    node_type = None  # Does this just mean that this isn't something in 223p yet?
    temperature_setpoint: AnalogOut

    def __init__(self, label: str) -> None:
        super().__init__(label=label)
        # I need a junction to be the system inlet and outlet if I want to connect to another junction.
        j = Junction()
        self.supplyAir.mapsTo = j


r = RooftopUnit(node_iri=ex.rtu, label="rtu")
p = Plenum(label="plenum")
z = HVACZone2(label="zone")
# can't seem to connect system connection points to junctions
r.supplyAirOutlet >> p.AirInlet

# p.AirOutlet.link_to(z.supplyAir) #getting no common connection types, because supply Air isn't a junction
p.AirOutlet >> (z.supplyAir)


# g36_header(model_name)
dump()
