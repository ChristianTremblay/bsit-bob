from rdflib import Graph, URIRef

from .core import (
    OccupancyEnum,
    Role,
    Substance,
    YesNoEnum,
    s223,
    OnOffEnum,
    PositionStatusEnum,
    NormalAlarmEnum,
    OpenCloseEnum,
)

_namespace = s223


#
Exhaust = Role("Exhaust")
Primary = Role("Primary")
Secondary = Role("Secondary")
Supply = Role("Supply")
Return = Role("Return")

#
Smoke = Substance("Smoke")

#
OnOff_On = OnOffEnum("On")
OnOff_Off = OnOffEnum("Off")
OnOff_Unknown = OnOffEnum("Unknown")

#
PositionStatus_Close = PositionStatusEnum("Closed")
PositionStatus_Open = PositionStatusEnum("Open")
PositionStatus_Moving = PositionStatusEnum("Moving")
PositionStatus_Unknown = PositionStatusEnum("Unknown")

#
OccupancyStatus_Unknown = OccupancyEnum("Unknown")
OccupancyStatus_Occupied = OccupancyEnum("Occupied")
OccupancyStatus_Unoccupied = OccupancyEnum("Unoccupied")
OccupancyStatus_Standby = OccupancyEnum("Standby")
OccupancyStatus_Bypass = OccupancyEnum("Bypass")

#
Yes = YesNoEnum("Yes")
No = YesNoEnum("No")

#
Normal = NormalAlarmEnum("Normal")
Alarm = NormalAlarmEnum("Alarm")

#
Open = OpenCloseEnum("Open")
Close = OpenCloseEnum("Close")

"""
s223:EnumerationKind-Direction
    s223:Direction-Inlet
    s223:Direction-Outlet
    s223:Direction-Bidirectional

s223:EnumerationKind-Domain
    s223:Domain-ConveyanceSystems
    s223:Domain-Electrical
    s223:Domain-Fire
    s223:Domain-HVAC
    s223:Domain-Lighting
    s223:Domain-Networking
    s223:Domain-Occupancy
    s223:Domain-Physical
    s223:Domain-Plumbing
    s223:Domain-Refrigeration
    s223:Domain-Security

s223:EnumerationKind-Effectiveness
    s223:Effectiveness-Active

s223:EnumerationKind-HVACOperatingMode
    s223:HVACOperatingMode-Auto
    s223:HVACOperatingMode-CoolOnly
    s223:HVACOperatingMode-FanOnly
    s223:HVACOperatingMode-HeatOnly
    s223:HVACOperatingMode-Off

s223:EnumerationKind-HVACOperatingStatus
    s223:HVACOperatingStatus-Cooling
    s223:HVACOperatingStatus-Dehumidifying
    s223:HVACOperatingStatus-Heating
    s223:HVACOperatingStatus-Off
    s223:HVACOperatingStatus-Ventilating

s223:EnumerationKind-Medium
    s223:Medium-Air
    s223:Medium-Electricity
    s223:Medium-Glycol
    s223:Medium-Light
        s223:Light-Infrared
        s223:Light-Visible
    s223:Medium-Water
        s223:Water-ChilledWater
        s223:Water-HotWater

s223:EnumerationKind-OccupancyStatus
    s223:OccupancyStatus-Occupied
    s223:OccupancyStatus-Unknown
    s223:OccupancyStatus-Unoccupied

s223:EnumerationKind-PositionStatus
    s223:PositionStatus-Closed
    s223:PositionStatus-Open
    s223:PositionStatus-Unknown

s223:EnumerationKind-Role
    s223:Role-Cooling
    s223:Role-Discharge
    s223:Role-Exhaust
    s223:Role-Generator
    s223:Role-Heating
    s223:Role-Load
    s223:Role-Primary
    s223:Role-Recirculating
    s223:Role-Return
    s223:Role-Secondary
    s223:Role-Supply

s223:EnumerationKind-RunStatus
    s223:RunStatus-Off
    s223:RunStatus-On
    s223:RunStatus-Unknown

s223:EnumerationKind-Substance
    s223:Substance-CO
    s223:Substance-Particulate
    s223:Substance-Soot

s223:EnumerationKind-ThreeSpeedSetting
    s223:ThreeSpeedSetting-High
    s223:ThreeSpeedSetting-Low
    s223:ThreeSpeedSetting-Medium
    s223:ThreeSpeedSetting-Off
"""
