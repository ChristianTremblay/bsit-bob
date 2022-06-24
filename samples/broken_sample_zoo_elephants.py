from pathlib import Path
from typing import Any, Dict

from header import sample_header

from bob.connections.air import *
from bob.connections.electricity import ElectricalInletConnectionPoint
from bob.connections.water import WaterConnection
from bob.core import (
    Device,
    Junction,
    System,
    bind_model_namespace,
    dump,
    get_datagraph,
    UNIT,
)
from bob.devices.architectural import Window
from bob.devices.hvac.chiller import AgnosticChiller
from bob.devices.hvac.coil import ChilledWaterCoil, HotWaterCoil, WaterCoil
from bob.devices.hvac.compressor import AirCompressor
from bob.devices.hvac.damper import (
    Damper,
    ElectricalActuatedOnOffDamper,
    ElectricalActuatedProportionalDamper,
    PneumaticActuatedOnOffDamper,
)
from bob.devices.hvac.fan import Fan
from bob.devices.hvac.filter import Filter
from bob.devices.hvac.geothermal import GeothermalWell
from bob.devices.hvac.heatexchanger import Accumulator, Accumulator4SidesDuct
from bob.devices.hvac.humidifier import Humidifier, SteamPipe
from bob.devices.hvac.pump import Pump
from bob.devices.hvac.valve import TwoWayActuatedProportionalValve, TwoWayValve
from bob.devices.electricity.vfd import VFD
from bob.devices.lighting.light import Luminaire
from bob.sensor.flow import AirFlowSensor
from bob.sensor.gas import CO2Sensor
from bob.sensor.humidity import AirHumiditySensor
from bob.sensor.light import MovementSensor
from bob.sensor.pressure import AirDifferentialStaticPressureSensor
from bob.sensor.temperature import AirTemperatureSensor, WaterTemperatureSensor
from bob.space.hvac import HVACSpace, HVACZone
from bob.space.light import LightingSpace, LightingZone
from bob.space.physical import (
    Bathroom,
    Building,
    Corridor,
    Floor,
    MechanicalRoom,
    Office,
    Roof,
    Room,
)
from bob.systems.hvac.airhandlingunit import AirHandlingUnit
from bob.systems.hvac.vav import VAV

# from bob.externalreference.BACNET import BACnetReference, NiagaraORDReference


model_name = Path(__file__).stem
_namespace = bind_model_namespace("zoo", f"urn:zoo/{model_name}/")

# Physical spaces
building = Building(label="B-1", comment="Pavillon des éléphants")
floor1 = Floor(label="RdC", comment="Rez-de-chaussée")
mezzanine = Floor(label="mezz", comment="Mezzanine")
mechroom = MechanicalRoom(label="MechRoom", comment="Salle mecanique")
mechroom_chiller = MechanicalRoom(
    label="MechRoom", comment="Salle mecanique des refroidisseurs"
)
office = Office(label="Office", comment="Bureau des gardiens")
entrepot = Room(label="Entrepot", comment="Entrepot a foin")
enclos_elephants = Room(label="Box1", comment="Enclos")
enclos_girafes = Room(label="Box2", comment="Enclos des girafes")
building > [floor1, mezzanine]
mezzanine > mechroom
floor1 > [mechroom_chiller, office, entrepot, enclos_elephants, enclos_girafes]


# HVAC Spaces
enclos_elephants_hvac = HVACSpace(label="enclos_elephants_hvac")
enclos_girafe_hvac = HVACSpace(label="enclos_girafe_hvac")

# Outdoor
outdoor = AirConnection(label="Outdoor")

# Worth defining a system to represent the Heat Exhanger
# This process needs to be improved... should be a simple class like custom system
# taking a template for configuration
hx = System(label="ECHANGEUR", comment="The complete heat Exchanger by Trane")
hx_outdoorCP1 = (AirBidirectionalSystemConnectionPoint(hx),)
hx_outdoorCP2 = (AirBidirectionalSystemConnectionPoint(hx),)
hx_returnDuct = (AirInletSystemConnectionPoint(hx),)
hx_supplyDuct = (AirOutletSystemConnectionPoint(hx),)
hx_pneumaticInlet = CompressedAirInletSystemConnectionPoint(hx)


# System - Air Handling Unit
accumulator1 = Accumulator(label="Acc1", comment="Accumulator #1")
accumulator2 = Accumulator(label="Acc2", comment="Accumulator #2")
acc1_damper_a = Damper(label="ACC1_DPR-A", comment="Accumulator #1 Damper A")
acc1_damper_b = Damper(label="ACC1_DPR-B", comment="Accumulator #1 Damper B")
acc1_damper_c = Damper(label="ACC1_DPR-C", comment="Accumulator #1 Damper C")
acc1_damper_d = Damper(label="ACC1_DPR-D", comment="Accumulator #1 Damper D")
acc2_damper_a = Damper(label="ACC2_DPR-A", comment="Accumulator #2 Damper A")
acc2_damper_b = Damper(label="ACC2_DPR-B", comment="Accumulator #2 Damper B")
acc2_damper_c = Damper(label="ACC2_DPR-C", comment="Accumulator #2 Damper C")
acc2_damper_d = Damper(label="ACC2_DPR-D", comment="Accumulator #2 Damper D")

acc_4sides_duct = Accumulator4SidesDuct(
    label="Accumulator 4 sides duct",
    comment="It contains a Air Connection to connect 4 sides and a pneumatic damper",
)
acc_4sides_damper = PneumaticActuatedOnOffDamper(
    label="Accumulator 4 sides damper",
    comment="This damper switch the side of the airflow going in accumulator 1 & 2",
)

hx > [
    accumulator1,
    accumulator2,
    acc1_damper_a,
    acc1_damper_b,
    acc1_damper_c,
    acc1_damper_d,
    acc2_damper_a,
    acc2_damper_b,
    acc2_damper_c,
    acc2_damper_d,
    acc_4sides_damper,
    acc_4sides_duct,
]

filters = Filter(label="FLT")

coil = WaterCoil(
    label="SE-1",
    comment="This coil acts as a cooling coil in summer, heating coil in winter",
)
sf = Fan(
    label="UV-1", comment="Supply Fan", electricalInlet=ElectricalInletConnectionPoint
)
supply_duct = AirConnection(
    label="SupplyDuct",
    comment="This is where 3 duct are connected going to Girafes, Elephants and UV-3 (Manège)",
)
return_duct = AirConnection(
    label="ReturnDuct",
    comment="This is where 2 ducts are connected coming from Girafes and Elephants",
)
av2 = Damper(label="AV-2", comment="Damper going to Girafe")
av4 = Damper(label="AV-4", comment="Damper going to Éléphants")
av1 = Damper(label="AV-1", comment="Damper Coming from Girafe (return)")
av3 = Damper(label="AV-3", comment="Damper coming from Éléphants (return)")
rf = Fan(
    label="VR-1", comment="Return Fan", electricalInlet=ElectricalInletConnectionPoint
)

vfd_sf = VFD(
    label="VFD-1",
    comment="VFD for Supply Fan",
    electricalInlet=ElectricalInletConnectionPoint,
    electricalOutlet=ElectricalInletConnectionPoint,
)
vfd_rf = VFD(
    label="VFD-2",
    comment="VFD for return fan",
    electricalInlet=ElectricalInletConnectionPoint,
    electricalOutlet=ElectricalInletConnectionPoint,
)

hum = Humidifier(label="HUM-1", comment="Humidifier")
hum_pipe = SteamPipe(
    label="HUM-1_Buse",
    comment="The pipe connected in the duct to provide humidity in air",
)
# hum.steamOutlet >> hum_pipe.steamInlet

aircomp = AirCompressor(label="ACOMP-1", comment="Air Compressor")
aircomp.compressedAirOutlet >> acc_4sides_damper["actuator"].compressedAirInlet


# Sensors
te1 = AirTemperatureSensor(
    label="TE-1",
    comment="Outdoor air preheated by exhanger",
    unit=UNIT.DEG_C,
    # hasExternalReference=BACnetReference("bacnet://345/analog-value/1/present-value"),
)
ha1 = AirHumiditySensor(label="HA-1")
tpd1 = AirDifferentialStaticPressureSensor(
    label="TPD-1", comment="Filters differential pressure", unit=UNIT.PA
)
taec1 = WaterTemperatureSensor(
    label="TAEC-1", comment="Water temperature feeding coil", unit=UNIT.DEG_C
)
tbl1 = Device(label="TBL-1", comment="Freeze Thermostat")
ta1 = AirTemperatureSensor(
    label="TA-1",
    comment="Discharge Air Temperature Sensor",
    unit=UNIT.DEG_C,
)
fs1 = Device(label="FS-1", comment="Air flow switch for humidifier")
hlh1 = Device(label="HLH-1", comment="Humidity High Level Stat")
tpd2 = AirDifferentialStaticPressureSensor(
    label="TPD-2", comment="Static Discharge Air Pressure Sensor", unit=UNIT.PA
)
co2_1 = CO2Sensor(label="CO2-1", comment="Return Air CO2 Sensor (Elephants)")
co2_2 = CO2Sensor(label="CO2-2", comment="Return Air CO2 Sensor (Girafes)")
hr1 = AirHumiditySensor(label="HR-1", comment="Return Air Humidity Sensor")
tr1 = AirTemperatureSensor(
    label="TR-1",
    comment="Return Air Temperature Sensor",
    unit=UNIT.DEG_C,
)

# Connections
outdoor >> accumulator1.outdoorSide
outdoor >> accumulator2.outdoorSide
after_accumulator1 = AirConnection(
    label="AfterAcc1",
    comment="After Accumulator 1, there are 4 dampers to control air flow, need a connection to connect those 4 dampers",
)
after_accumulator2 = AirConnection(
    label="AfterAcc2",
    comment="After Accumulator 2, there are 4 dampers to control air flow, need a connection to connect those 4 dampers",
)

after_dampers1 = AirConnection(
    label="AfterDpr1", comment="4 dampers are feeding the 4 sided duct of the exchanger"
)
after_dampers2 = AirConnection(
    label="AfterDpr2", comment="4 dampers are feeding the 4 sided duct of the exchanger"
)

accumulator1.indoorSide >> after_accumulator1 >> acc1_damper_a >> after_dampers1
after_accumulator1 >> acc1_damper_b >> after_dampers1
after_accumulator1 >> acc1_damper_c >> after_dampers1
after_accumulator1 >> acc1_damper_d >> after_dampers1
accumulator2.indoorSide >> after_accumulator2 >> acc2_damper_a >> after_dampers2
after_accumulator2 >> acc2_damper_b >> after_dampers2
after_accumulator2 >> acc2_damper_c >> after_dampers2
after_accumulator2 >> acc2_damper_d >> after_dampers2

after_dampers1 >> acc_4sides_duct.accumulator1Connection
after_dampers2 >> acc_4sides_duct.accumulator2Connection

acc_4sides_duct.supplyDuctOutlet >> filters.airInlet
filters.airOutlet >> coil.airInlet
coil.airOutlet >> sf.airInlet
sf.airOutlet >> hum_pipe.airInlet
hum_pipe.airOutlet >> supply_duct
supply_duct >> av2.airInlet
supply_duct >> av4.airInlet

av2.airOutlet >> enclos_girafe_hvac.ductAirInlet
av4.airOutlet >> enclos_elephants_hvac.ductAirInlet

enclos_girafe_hvac.ductAirOutlet >> av1.airInlet
av1.airOutlet >> return_duct
enclos_elephants_hvac.ductAirOutlet >> av3.airInlet
av3.airOutlet >> return_duct
return_duct >> rf.airInlet
rf.airOutlet >> acc_4sides_duct.returnDuctInlet

# Localise sensors
te1.hasMeasurementLocation = acc_4sides_duct.supplyDuctOutlet
te1.hasPhysicalLocation = mechroom
ha1.hasMeasurementLocation = acc_4sides_duct.supplyDuctOutlet
ha1.hasPhysicalLocation = mechroom
ta1.hasMeasurementLocation = supply_duct
ta1.hasPhysicalLocation = mechroom
tpd1.hasMeasurementLocationHigh = filters.airInlet
tpd1.hasMeasurementLocationLow = filters.airOutlet
tpd1.hasPhysicalLocation = mechroom
tpd2.hasMeasurementLocationHigh = supply_duct
tpd2.hasMeasurementLocationLow = enclos_elephants_hvac
tpd2.hasPhysicalLocation = mechroom
co2_1.hasMeasurementLocation = enclos_girafe_hvac.ductAirOutlet
co2_1.hasPhysicalLocation = enclos_elephants
co2_2.hasMeasurementLocation = enclos_elephants_hvac.ductAirOutlet
co2_2.hasPhysicalLocation = enclos_elephants
hr1.hasMeasurementLocation = return_duct
hr1.hasPhysicalLocation = mechroom
tr1.hasMeasurementLocation = return_duct
tr1.hasPhysicalLocation = mechroom


# Geothermal water network
well = GeothermalWell(label="GeothermalWells")
pc1 = AgnosticChiller(label="PC-1", comment="Chiller #1")
pc2 = AgnosticChiller(label="PC-2", comment="Chiller #2")
p1 = Pump(
    label="P-1",
    comment="Pump P-1, Condensed Water loop to heat UV-1 and Radiant Floors",
)
p2 = Pump(
    label="P-2",
    comment="Pump P-2, Condensed Water loop to heat UV-1 and Radiant Floors",
)
p3 = Pump(label="P-3", comment="Pump P-3, Geothermal Well pumps")
p4 = Pump(label="P-4", comment="Pump P-4, Geothermal Well pumps")
v1A_no = TwoWayActuatedProportionalValve(
    label="V-1A_NO", comment="Butterfly Valve NO to Well of pair V-1A"
)
v1A_nc = TwoWayActuatedProportionalValve(
    label="V-1A_NC", comment="Butterfly Valve NC to Coil of pair V-1A"
)
v1B_no = TwoWayActuatedProportionalValve(
    label="V-1B_NO", comment="Butterfly Valve NO to Well of pair V-1B"
)
v1B_nc = TwoWayActuatedProportionalValve(
    label="V-1B_NC", comment="Butterfly Valve NC to Coil of pair V-1B"
)
v2 = TwoWayActuatedProportionalValve(label="V-2", comment="PC-1 Isolation valve")
v3 = TwoWayActuatedProportionalValve(label="V-3", comment="PC-2 Isolation valve")
v4 = TwoWayActuatedProportionalValve(label="V-4", comment="Loop pressure control Valve")

leaving_chilledWater_pipe = WaterConnection(
    label="CHWL_Pipe", comment="Chilled Water Leaving Pipe from both chillers"
)

# This one leads to Connection - Connection link
# Also be better as a System Conneciton Point
entering_chilledWater_pipe = WaterConnection(
    label="CHWE_Pipe", comment="Chilled Water Entering Pipe for both chillers"
)

leaving_condensedWater_pipe = WaterConnection(
    label="CWL_Pipe", comment="Condensed Water Leaving Pipe from both chillers"
)
entering_condensedWater_pipe = WaterConnection(
    label="CWE_Pipe", comment="Condensed Water Entering Pipe for both chillers"
)

p1_p2_leaving = WaterConnection(label="P1P2WL")

# This will lead to connecting 2 connections together
# = problem
# this connection could be abstracted by a System Connection Point instead
# using p1_p2_leaving as the connection for all radiant floor valves

# radiant_floor_collector_supply = Junction(label="RFC-SUPPLY")
# radiant_floor_collector_return = Junction(label="RFC-RETURN")

coil_supply_pipe = WaterConnection(
    label="COIL-SUPPLY",
    comment="At this point, water can be hot or cold, depending on the valve V-1A,B position",
)
coil_return_pipe = WaterConnection(
    label="COIL-RETURN",
    comment="This is the connection where UV-3 coil, and UV-1 coil returns",
)

bypass_pipe = WaterConnection(label="BYPASS")

p3_p4_leaving = WaterConnection(label="P3P4WL")
p3_p4_entering = WaterConnection(label="P3P4WE")

pc1.chilledWaterLeaving >> leaving_chilledWater_pipe
pc2.chilledWaterLeaving >> leaving_chilledWater_pipe
leaving_chilledWater_pipe >> p1.waterInlet
p1.waterOutlet >> p1_p2_leaving
leaving_chilledWater_pipe >> p2.waterInlet
p2.waterOutlet >> p1_p2_leaving

# p1_p2_leaving >> radiant_floor_collector_supply
p1_p2_leaving >> v1B_nc.waterInlet
v1B_nc.waterOutlet >> coil_supply_pipe
v1B_no.waterOutlet >> coil_supply_pipe

coil_supply_pipe >> coil.waterInlet
coil.waterOutlet >> coil_return_pipe

coil_return_pipe >> v1A_no.waterInlet
coil_return_pipe >> v1A_nc.waterInlet

v1A_nc.waterOutlet >> entering_condensedWater_pipe
v1A_no.waterOutlet >> leaving_chilledWater_pipe
# radiant_floor_collector_return >> entering_condensedWater_pipe

entering_condensedWater_pipe >> pc1.condensedWaterEntering
entering_condensedWater_pipe >> pc2.condensedWaterEntering

p3_p4_leaving >> v2.waterInlet
v2.waterOutlet >> pc1.chilledWaterEntering

p3_p4_leaving >> v3.waterInlet
v3.waterOutlet >> pc2.chilledWaterEntering

leaving_chilledWater_pipe >> well.waterInlet
leaving_chilledWater_pipe >> v4.waterInlet
v4.waterOutlet >> p3_p4_entering

well.waterOutlet >> p3_p4_entering >> p3.waterInlet
p3_p4_entering >> p4.waterInlet
p3.waterOutlet >> p3_p4_leaving
p4.waterOutlet >> p3_p4_leaving
# p3_p4_leaving >> entering_chilledWater_pipe


result = dump(
    filename=f"samples/ttl/{model_name}.ttl", header=sample_header(model_name)
)
