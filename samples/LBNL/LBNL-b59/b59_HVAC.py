from pathlib import Path
from typing import Any

# from bob.domain import *
import pandas as pd
from header import lbnl_header

from bob.connections.air import *
from bob.connections.water import *
from bob.core import *
from bob.equipment.archives.coolingcoil import ChilledWaterCoil, ChilledWaterCoil2
from bob.equipment.archives.heatingcoil import HotWaterCoil2
from bob.equipment.hvac.airflowstation import AirFlowMonitor
from bob.equipment.hvac.damper import Damper
from bob.equipment.hvac.fan import Fan
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.vfd import VFD
from bob.properties.electricity import ElectricPowerkW
from bob.properties.flow import Flow
from bob.properties.ratio import Percent
from bob.properties.states import OnOffCommand, OnOffStatus
from bob.properties.temperature import Temperature
from bob.property import *
from bob.role import Exhaust, Return, Supply

# from bob.properties.force import Pressure
from bob.sensor import DifferentialSensor
from bob.sensor.pressure import AirStaticPressureSensor
from bob.sensor.temperature import (
    AirTemperatureSensor,
    TemperatureSetpoint,
    WaterTemperatureSensor,
)

# from bob.signal import(
#     AnalogOut,
#     AnalogIn,
#     )


# model_name = Path(__file__).stem
model_name = "b59"
__namespace__ = ex = bind_model_namespace("ex", f"urn:ex/{model_name}/")
_namespace = ex


class OutdoorAir(DomainSpace):
    # something to connect exhaust air too
    hasDomain = HVAC

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class Pressure(QuantifiableObservableProperty):
    hasQuantityKind: URIRef = quantitykind.PRESSURE
    unit: URIRef = qudt.PSI


class SpeedSetpoint(QuantifiableActuatableProperty):
    hasQuantityKind: URIRef = quantitykind.Speed
    unit: URIRef = qudt.PERCENT


class RTUFan(Fan):
    speedSetpoint = SpeedSetpoint
    # not sure if it should be qudt.Speed AngularFrequency, something else?
    power = ElectricPowerkW
    speedFeedback = Percent
    vfd_start_stop = OnOffCommand
    airFlow = Flow

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.airFlow.unit = unit.FT3_PER_MIN


class RTUDamper(Damper):
    node_type = None
    # position = Analog Out from hvac.py. Exhaust Air Damper doesn't have a position command in the Haystack model. Here I am adding it
    positionFeedback = Percent


class RTUChilledWaterCoil(ChilledWaterCoil):
    node_type = None
    compressor1Status: ObservableProperty
    compressor2Status: ObservableProperty
    Compressor1Cooling: ActuatableProperty  # not sure what more information the cooling commands should have
    Compressor2Cooling: ActuatableProperty

    # diagram has sensors, but this is not in haystack... Not sure if I want to do the below. Sensors are shown in the diagram so I am including them, like the other Equipment
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        ts1 = WaterTemperatureSensor(label=self.label + ".in_temperature_sensor")
        ts2 = WaterTemperatureSensor(label=self.label + ".out_temperature_sensor")

        ts1 % self.chilledWaterInlet
        ts2 % self.chilledWaterOutlet


# class AirStaticPressureSensor(Equipment):
# should have just made a sensor class probs #WILL NEED TO HANDLE DIFFERENTIAL PRESSURE DIFFERENTLY
#     node_type: URIRef = s223.Sensor
#     pressure = QuantifiableObservableProperty  #AnalogIn This results in the turtle file having temperature listed as a property and listed plainly.
#     pressure.hasQuantityKind = quantitykind.StaticPressure #QUDT doesn't seem to have differential pressure quantity kind
#     pressure.unit = qudt.IN_H2O
#     #check what unit
#     hasObservationLocation: Node # FOR DIFFERENTIAL PRESSURE, should probably maybe make a new sensor that measures connection points around Equipment
class RooftopUnit(System):
    node_type = None  # missing some of the points in the haystack model that are not attached to equipment or shown in the diagram. (duct heat gain, outside air flow, economizer enable status, outside air temperature)
    returnAirInlet: AirInletSystemConnectionPoint
    outsideAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    exhaustAirOutlet: AirOutletSystemConnectionPoint

    # should I put the basic command and feedback in the class here?

    # deciding not to use self, if I need ot access the RTU outside of this class it'd probably be good to have, but will I?
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        mixed_air_damper = RTUDamper(label=self.label + ".mixed_air_damper")
        self > mixed_air_damper
        mixed_air = AirConnection(label=self.label + ".mixed_air")

        self.sensor = AirTemperatureSensor(label=self.label + ".MA_temp_sensor")
        self > self.sensor
        self.sensor % mixed_air  # This seems weird, but I kind of like it. You're measuring the mixed air connection

        return_fan = RTUFan(label=self.label + ".return_fan")
        self > return_fan
        return_fan.hasRole = Return
        self.returnAirInlet.mapsTo = return_fan.airInlet
        return_air = AirConnection(label=self.label + ".return_air")
        return_fan >> return_air
        ra_temp = AirTemperatureSensor(label=self.label + ".RA_temp_sensor")
        self > ra_temp
        ra_temp % return_air

        ra_pres = AirStaticPressureSensor(
            label=self.label + ".RA_static_pressure", unit=qudt.PA
        )
        self > ra_pres
        ra_pres % return_air

        # making backdraft damper (exhaust damper) and connecting it
        ea_damper = RTUDamper(label=self.label + ".exhaust_air_damper")
        self > ea_damper
        ea_damper.hasRole = Exhaust
        return_air >> ea_damper
        return_air >> mixed_air_damper
        self.exhaustAirOutlet.mapsTo = ea_damper.airOutlet

        oa_damper = RTUDamper(label=self.label + ".outside_air_damper")
        self > oa_damper
        self.outsideAirInlet.mapsTo = oa_damper.airInlet
        # connecting damper directly to flow station, not indicating OA air
        oa_flow_station = AirFlowMonitor(label=self.label + ".outside_air_flow_station")
        self > oa_flow_station
        oa_damper >> oa_flow_station >> mixed_air
        mixed_air_damper >> mixed_air

        pre_filter = Filter(label=self.label + ".pre_filter")
        self > pre_filter
        pf_press = AirStaticPressureSensor(
            label=self.label + "PF_differential_pressure", unit=qudt.PA
        )  # Do I need a different pressure sensor
        self > pf_press
        pf_press % pre_filter

        # filter has one connection, making new air to connect to bypass and coil
        pre_filtered_air = AirConnection(label=self.label + ".pre_filtered_air")
        mixed_air >> pre_filter >> pre_filtered_air

        bp_damper = RTUDamper(label=self.label + ".bypass_damper")
        self > bp_damper
        # schematic has an iso valve but I don't think that's what chilledWaterCoil2 is talking about
        cwc = RTUChilledWaterCoil(label=self.label + ".chilled_water_coil")
        self > cwc
        # both the damper and air need to go into a filter, air as a medium?
        chilled_air = AirConnection(label=self.label + ".chilled_air")
        pre_filtered_air >> bp_damper >> chilled_air
        pre_filtered_air >> cwc >> chilled_air

        # connect via air connections or create junctions/segments: Why create junctions when I can make multiple things connect too or from an AirConnection?

        final_filter = Filter(label=self.label + ".final_filter")
        self > final_filter
        ff_press = AirStaticPressureSensor(
            label=self.label + ".FF_differential_pressure", unit=qudt.PA
        )
        self > ff_press
        ff_press % final_filter

        supply_fan = RTUFan(label=self.label + ".supply_fan")
        self > supply_fan
        supply_fan.hasRole = Supply
        chilled_air >> final_filter >> supply_fan

        supply_air = AirConnection(label=self.label + ".supply_air")
        sa_press = AirStaticPressureSensor(
            label=self.label + ".SA_static_pressure", unit=qudt.PA
        )
        self > sa_press
        sa_press % supply_air
        sa_temp = AirTemperatureSensor(label=self.label + ".SA_temperature")
        self > sa_temp
        sa_temp % supply_air

        self.iso_damper = Damper(label=self.label + ".iso_damper")
        self > self.iso_damper
        supply_fan >> self.iso_damper

        self.supplyAirOutlet.mapsTo = self.iso_damper.airOutlet


# Should a plenum be a segment or is system correct??
class UFPlenum(DomainSpace):
    node_type = (
        s223.Plenum
    )  # line 717 making sure that the connection doesn't already exist uses the substance. This means I can't make a new subclass with the same substance but different points.
    staticPressure = Pressure
    hasDomain = HVAC

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    # HAVE TO DO SOMETHING WITH MEDIUM

    # SupplyInlet: AirInletConnectionPoint
    # SupplyOutlet: AirOutletConnectionPoint
    # ReturnInlet: AirInletConnectionPoint
    # ReturnOutlet: AirOutletConnectionPoint

    # Underfloor plenum, making it a space even though it could be many things
    # hasDomain = HVAC
    # hasSubstance = Air


class UFT_Fan(Fan):
    node_type = None
    speed_ctrl = SpeedSetpoint  # WHAT additional detail should I add to these points??
    # fan_amps = AnalogIn


class HotWaterCoilUFT(HotWaterCoil2):
    node_type: URIRef = s223.HeatingCoil
    pass  # HotWaterCoil2 has everything I need


class UFT(System):  # Underfloor Fan Terminal Unit
    node_type = None
    supplyAirInlet: AirInletSystemConnectionPoint
    supplyAirOutlet: AirOutletSystemConnectionPoint
    staticPressure = Pressure
    airFlow = Flow
    # reheat valve command in hotWaterCoil2 in hvac.py. It is analog in there
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.airFlow.unit = qudt.FT3_PER_MIN
        supply_fan = UFT_Fan(label=self.label + ".supply_fan")
        self > supply_fan
        supply_fan.hasRole = Supply
        self.supplyAirInlet.mapsTo = supply_fan.airInlet
        hw_coil = HotWaterCoilUFT(
            label=self.label + ".hw_coil"
        )  # problem using HotWaterCoil2, mapping a system connection point to a system connection point that maps to a Equipment connection point
        supply_fan >> hw_coil
        self > hw_coil
        self.supplyAirOutlet.mapsTo = (
            hw_coil.hot_water_coil.airOutlet
        )  # have to map system to the Equipment connection point in the subsystem, does this make sense?


class UFTZone(
    Zone
):  # adding CO2 point in instantiation #Could use HVACZone1 but space is not declared as self.space. What is the more streamlined way of doing this?
    node_type = None
    # supplyAir: AirInletZoneConnectionPoint
    # heating_setpoint = HeatingSetpoint
    # cooling_setpoint = CoolingSetpoint
    temperature = Temperature
    hasDomain = HVAC

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.temperature.unit = qudt.DEG_F
        # temperature_sensor = TemperatureSensor(label = self.label + '.temperature_sensor') #this will be for cerc temploggers.
        # temperature_sensor % self  #not sure if I even wan't it to measure zone or space
        # print(self)
        # self.space = DomainSpace(label=self.label + ".space")
        # self.space.hasDomain = HVAC

        # self.supplyAir.mapsTo = AirInletConnectionPoint(
        #     self.space, label=self.label + ".space.supplyAir"
        # )
        # self.returnAir.mapsTo = AirOutletConnectionPoint(
        #     self.space, label=self.label + ".space.returnAir"
        # )
        # self>self.space


class CO2Concentration(QuantifiableObservableProperty):
    node_type = None
    unit = qudt.PPM
    hasQuantityKind = quantitykind.Concentration


# attempt to add water, all from diagram, needs checks/incomplete
class HeatExchanger(Equipment):
    node_type = None
    coolingInlet: ChilledWaterInletConnectionPoint
    coolingOutlet: ChilledWaterOutletConnectionPoint
    heatingInlet: ChilledWaterInletConnectionPoint
    heatingOutlet: ChilledWaterOutletConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


class LoopPressureSensor(DifferentialSensor):
    node_type = None  # should have just made a sensor class probs
    node_type: URIRef = s223.Sensor
    pressure = Pressure
    # check what unit
    hasObservationLocationReturn: Node
    hasObservationLocationSupply: Node

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in ["hasObservationLocationReturn", "hasObservationLocationSupply"]:
            self._data_graph.add((self.node, S223.hasObservationLocation, value.node))
        else:
            super().__setattr__(attr, value)


class CoolingPump(Equipment):
    node_type = None  # need to check points in Haystack
    waterInlet: ChilledWaterInletConnectionPoint
    waterOutlet: ChilledWaterOutletConnectionPoint

    speedSetpoint = SpeedSetpoint
    power = ElectricPowerkW
    speedFeedback = Percent
    vfd_start_stop = OnOffCommand
    airFlow = Flow

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.airFlow.unit = unit.FT3_PER_MIN


class CoolingWaterSystem(
    System
):  # my Equipment using cool water will be connected to a junction at CWSupply
    node_type = None
    CWSupply: ChilledWaterOutletSystemConnectionPoint
    # not including BTU meters
    from_twgps: ChilledWaterInletSystemConnectionPoint
    to_cooling_towers: ChilledWaterOutletSystemConnectionPoint
    CWReturn: ChilledWaterInletSystemConnectionPoint
    makeUpInlet: ChilledWaterInletSystemConnectionPoint

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        tws_ts = WaterTemperatureSensor(label=self.label + ".TWS_Temp")
        # lets make this connection points
        ex1 = HeatExchanger(label=self.label + ".EX_1")
        self.from_twgps.mapsTo = ex1.coolingInlet
        self > ex1
        cwsupply = Junction(label="Chilled Water Supply")
        cwsupply << ex1.coolingOutlet
        self.CWSupply.mapsTo = cwsupply
        tws_ts % ex1.coolingInlet
        # cws = ChilledWaterConnection(label = self.label + '.CWS')
        # ex1.coolingOutlet>>cws
        cws_ts = WaterTemperatureSensor(label=self.label + ".CWS_Temp")
        self > cws_ts
        # cws_ts % cws
        cws_ts % ex1.coolingOutlet
        # have to use segments and junctions here, this shows different modeling decision between right and left side of Cooling Water Control Schematic
        cwr = Segment(label=self.label + ".CWR")
        makeup = Segment(label=self.label + ".MakeUp")
        j = Junction()  # if I should label, I'm not sure what I should do.
        # cwr.link_to(j) #connect to or link to?
        j.link_to(cwr)
        j.link_to(makeup)
        # makeup.link_to(j) #worried I'm doing this wrong
        mkin = Junction(label=self.label + "MakeUp_Inlet")
        mkin.link_to(makeup)
        self.makeUpInlet.mapsTo = mkin
        cwgp1 = CoolingPump(label=self.label + ".Pump_1")
        cwgp2 = CoolingPump(label=self.label + ".Pump_2")
        self > cwgp1
        self > cwgp2
        j.connect_to(cwgp1.waterInlet)
        j.connect_to(cwgp2.waterInlet)
        pump_out = ChilledWaterConnection(label=self.label + ".Pump_Outputs")
        cwgp1.waterOutlet >> pump_out
        cwgp2.waterOutlet >> pump_out
        EX1_cwr_ts = WaterTemperatureSensor(label=self.label + ".EX-1_CWR_Temp")
        EX1_cwr_ts % pump_out
        self > EX1_cwr_ts
        ps = LoopPressureSensor(label=self.label + ".CW_Loop_Diff_Pressure")
        ps.hasObservationLocationSupply = ex1.coolingInlet
        ps.hasObservationLocationReturn = cwr
        # not sure how to do loop differential pressure, two measurement locations?
        pump_out >> ex1.heatingInlet
        EX1_TWR_ts = WaterTemperatureSensor(label=self.label + ".EX-1_TWR_Temp")
        EX1_TWR_ts % ex1.heatingOutlet
        self.to_cooling_towers.mapsTo = ex1.heatingOutlet
        jret = Junction(label=self.label + ".CWR_Inlet")
        jret.link_to(cwr)
        self.CWReturn.mapsTo = jret


class CoolingTower(
    Equipment
):  # should I try to specify type of cooling tower (counterflow I think)
    node_type = None
    waterInlet: ChilledWaterInletConnectionPoint
    waterOutlet: ChilledWaterOutletConnectionPoint
    ssfInlet: ChilledWaterInletConnectionPoint  # side stream filter Inlet
    ssfOutlet: ChilledWaterOutletConnectionPoint  # side stream filter outlet
    vaporOutlet: AirOutletConnectionPoint  # not sure if this is right
    vibrationSwitch = OnOffCommand  # not sure what this is


class SSFValve(Equipment):
    node_type = None
    waterInlet: ChilledWaterInletConnectionPoint
    waterOutlet: ChilledWaterOutletConnectionPoint
    status = OnOffStatus
    openValve = OnOffCommand


class SSFilter(Equipment):  # I need more information on this Filter
    node_type = None
    waterInlet: ChilledWaterInletConnectionPoint
    waterOutlet: ChilledWaterOutletConnectionPoint


class CoolingTowerFan(
    RTUFan
):  # has the same points as RTU fan, just different geometry
    node_type = None


class CoolingTowerSystem(System):
    node_type = None  # page 56 on visio bill of materials, I am making interesting modeling decisions around the connections and such
    waterInlet: ChilledWaterInletSystemConnectionPoint
    waterOutlet: ChilledWaterOutletSystemConnectionPoint

    def __init__(
        self, **kwargs: Any
    ) -> None:  # Might be misunderstanding schematic, do I need to add more pumps or are those already represented in the cooling watersystem?
        super().__init__(**kwargs)
        ct_dict = {}
        ct_dict[1] = self.ct1 = CoolingTower(label=self.label + ".Cooling_Tower_1")
        ct_dict[2] = self.ct2 = CoolingTower(label=self.label + ".Cooling_Tower_2")
        ct_dict[3] = self.ct3 = CoolingTower(label=self.label + ".Cooling_Tower_3")
        ct_dict[4] = self.ct4 = CoolingTower(label=self.label + ".Cooling_Tower_4")
        jin = Junction(
            label=self.label + ".CTS_Inlet"
        )  # I'm not sure these junction/connections are working right
        jout = Junction(label=self.label + ".CTS_Outlet")
        self.waterInlet.mapsTo = jin
        self.waterOutlet.mapsTo = jout
        for ct in ct_dict:
            fan = CoolingTowerFan(label=ct_dict[ct].label + ".CT_Fan")
            ct_dict[
                ct
            ].vaporOutlet >> fan.airInlet  # do I need to indicate that this system has an outlet point for this vapor
            jout << ct_dict[ct].waterOutlet
            jin >> ct_dict[ct].waterInlet
            ts = AirTemperatureSensor(label=ct_dict[ct].label + ".TWS_Temp")
            ts % ct_dict[ct].waterOutlet


class SSFSystem(System):
    node_type = None  # going to be a subsystem, missing overflow. Where does side stream water come from? This system seems to be closed except for cooling towers as middlemen
    SSFEnable = OnOffCommand  # these will be enumerated properties
    SSFPowerStatus: ElectricPowerkW
    SSFModeStatus: OnOffStatus  # placeholder

    def __init__(
        self, cts: CoolingTowerSystem, **kwargs: Any
    ) -> None:  # not sure it should be allowed
        super().__init__(**kwargs)
        to_ssf = ChilledWaterConnection(label=self.label + ".to_ssf")
        from_ssf = ChilledWaterConnection(label=self.label + ".from_ssf")
        ssf = SSFilter(label=self.label + ".Side_Stream_Filter")
        to_ssf >> ssf.waterInlet
        ssf.waterOutlet >> from_ssf
        ct_dict = {1: cts.ct1, 2: cts.ct2, 3: cts.ct3, 4: cts.ct4}
        for ct in ct_dict:
            vo = SSFValve(
                label=ct_dict[ct].label + ".SSFValve_to_filter"
            )  # if I need to access these valves again this will have to change
            vi = SSFValve(label=ct_dict[ct].label + ".SSFValve_from_filter")
            ct_dict[ct].ssfInlet << vi.waterOutlet
            ct_dict[ct].ssfOutlet >> vo.waterInlet
            vi.waterInlet << from_ssf
            vo.waterOutlet >> to_ssf


class ReturnZone(
    Zone
):  # adding CO2 point in instantiation #Could use HVACZone1 but space is not declared as self.space. What is the more streamlined way of doing this?
    node_type = None
    returnAirInlet: AirInletZoneConnectionPoint
    hasDomain = HVAC


class Lighting_Zone(Zone):
    node_type = None
    hasDomain = Lighting


class Area(QuantifiableObservableProperty):
    node_type = None
    unit = qudt.FT2
    hasQuantityKind = quantitykind.Area

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Wattage(QuantifiableObservableProperty):
    node_type = None
    hasQuantityKind = (
        quantitykind.ElectricPower
    )  # QUDT doesn't seem to have differential pressure quantity kind
    unit = qudt.W

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Light_Fixtures(Equipment):
    node_type = None
    FixtureWattage = Wattage
    FixtureQty = ObservableProperty  # This is the type and quantity it seems, can separate this out into more properties later
    LoadType = ObservableProperty


class Zone_Lighting(System):
    node_type = None
    TotalWattage = Wattage

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Illuminance(QuantifiableObservableProperty):
    node_type = None
    hasQuantityKind = (
        quantitykind.Illuminance
    )  # QUDT doesn't seem to have differential pressure quantity kind
    unit = qudt.FC

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)


class Daylight_Sensor(Equipment):
    node_type: URIRef = s223.Sensor
    illuminance = Illuminance
    hasObservationLocation: Node
