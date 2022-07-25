from rdflib import Graph, URIRef

from .core import (
    G36,
    P223,
    S223,
    Air,
    Domain,
    Electricity,
    EnumerationKind,
    Light,
    Role,
    Substance,
    Water,
)

_namespace = S223

# ===================
# MEDIA FLAVOURS
# ===================
# Air
Air.CompressedAir = CompressedAir = Air("CompressedAir", _alt_namespace=P223)

# Electricity
Electricity.AC575V_60Hz = Electricity("575V-60Hz")
Electricity.AC480V_60Hz = Electricity("480V-60Hz")
Electricity.AC347V_60Hz = Electricity("347V-60Hz")
Electricity.AC277V_60Hz = Electricity("277V-60Hz")
Electricity.AC208V_60Hz = Electricity("208V-60Hz")
Electricity.AC120V_240V_60Hz = Electricity("120V-240V-60Hz")
Electricity.AC240V_60Hz = Electricity("240V-60Hz")
Electricity.AC120V_60Hz = Electricity("120V-60Hz")
Electricity.AC24V_60Hz = Electricity("24V-60Hz", _alt_namespace=P223)
Electricity.DC48V = Electricity(
    "48V-DC", _alt_namespace=P223
)  # TODO : Create connections
Electricity.DC24V = Electricity(
    "24V-DC", _alt_namespace=P223
)  # TODO : Create connections
Electricity.DC12V = Electricity(
    "12V-DC", _alt_namespace=P223
)  # TODO : Create connections
Electricity.DC5V = Electricity(
    "5V-DC", _alt_namespace=P223
)  # TODO : Create connections
Electricity.OnOffSignal = Electricity("OnOffSignal", _alt_namespace=P223)
Electricity.ModulationSignal = Electricity("ModulationSignal", _alt_namespace=P223)
Electricity.RS485 = Electricity("RS485", _alt_namespace=P223)
Electricity.Ethernet = Electricity("Ethernet", _alt_namespace=P223)

# Water
Water.ChilledWater = ChilledWater = Water("ChilledWater")
Water.PotableWater = PotableWater = Water("PotableWater", _alt_namespace=P223)
Water.HotWater = HotWater = Water("HotWater")
Water.MixedWater = MixedWater = Water("MixedWater", _alt_namespace=P223)
Water.DomesticWater = DomesticWater = Water("DomesticWater", _alt_namespace=P223)
Water.DomesticHotWater = DomesticHotWater = Water(
    "DomesticHotWater", _alt_namespace=P223
)
Water.CondensedWater = CondensedWater = Water("CondensedWater", _alt_namespace=P223)
Water.GlycoledWater = GlycoledWater = Water("GlycoledWater", _alt_namespace=P223)
Water.Steam = Steam = Water("Steam", _alt_namespace=P223)

# Light
Light.Visible = Light("Visible")
Light.Infrared = Light("Infrared")

# ===================
# DOMAINS FLAVOURS
# ===================
Domain.HVAC = HVAC = Domain("HVAC")
Domain.Lighting = Lighting = Domain("Lighting")
Domain.Occupancy = Occupancy = Domain(
    "Occupancy"
)  # TODO : GET RID OF THIS... Occupancy is a function
Domain.Physical = Physical = Domain("Physical")
Domain.ConveyanceSystems = ConveyanceSystems = Domain("ConveyanceSystems")
Domain.Electrical = Electrical = Domain("Electrical")
Domain.Fire = Fire = Domain("Fire")
Domain.Networking = Networking = Domain("Networking")
Domain.Plumbing = Plumbing = Domain("Plumbing")
Domain.Refrigeration = Refrigeration = Domain("Refrigeration")
Domain.Security = Security = Domain("Security")
# ===================
# ROLES FLAVOURS
# ===================
Role.Cooling = Cooling = Role("Cooling")
Role.Discharge = Discharge = Role("Discharge")
Role.Exhaust = Exhaust = Role("Exhaust")
Role.Generator = Generator = Role("Generator")
Role.Heating = Heating = Role("Heating")
Role.Load = Load = Role("Load")
Role.Primary = Primary = Role("Primary")
Role.Return = Return = Role("Return")
Role.Secondary = Secondary = Role("Secondary")
Role.Supply = Supply = Role("Supply")

# ===================
# SUBSTANCES FLAVOURS
# ===================
Substance.Smoke = Smoke = Substance("Smoke", _alt_namespace=P223)
Substance.Particle = Particulate = Substance("Particulate")
Substance.PM1_0 = Particulate.PM1_0 = Particulate(
    "PM1.0"
)  # don't create PM1_0, not clear enough
Substance.PM2_5 = Particulate.PM2_5 = Particulate("PM2.5")
Substance.PM10_0 = Particulate.PM10_0 = Particulate("PM10.0")
Substance.CO = CO = Substance("CO")
Substance.CO2 = CO2 = Substance("CO2")
Substance.NO2 = NO2 = Substance("NO2", _alt_namespace=P223)
Substance.CH4 = CH4 = Substance("CH4", _alt_namespace=P223)
Substance.Soot = Soot = Substance("Soot")

# ===================
# Values Enumeration
# ===================
# Enumeration kinds to create hasValue
ActiveInactiveEnum = EnumerationKind("ActiveInactive", _alt_namespace=P223)
AITypeEnum = EnumerationKind("AIType", _alt_namespace=P223)
AOTypeEnum = EnumerationKind("AOType", _alt_namespace=P223)
BITypeEnum = EnumerationKind("BIType", _alt_namespace=P223)
BOTypeEnum = EnumerationKind("BOType", _alt_namespace=P223)
Effectiveness = EnumerationKind("Effectiveness")
G36AlarmLevel = EnumerationKind("G36AlarmLevels", _alt_namespace=G36)
HandOffAutoEnum = EnumerationKind("HandOffAuto", _alt_namespace=P223)
HVACOperatingMode = EnumerationKind("HVACOperatingMode")
HVACOperatingStatus = EnumerationKind("HVACOperatingStatus")
LeftRightEnum = EnumerationKind("LeftRight", _alt_namespace=P223)
ManualAutoEnum = EnumerationKind("ManualAuto", _alt_namespace=P223)
NiagaraStatusEnum = EnumerationKind("NiagaraStatus", _alt_namespace=P223)  # SEE BELOW
NormalAlarmEnum = EnumerationKind("NormalAlarm", _alt_namespace=P223)
NormalFaultEnum = EnumerationKind("NormalFault", _alt_namespace=P223)
OccupancyStatus = EnumerationKind("OccupancyStatus")
OnOffEnum = EnumerationKind("OnOff")
OpenCloseEnum = EnumerationKind("OpenClose", _alt_namespace=P223)
OverriddenAuto = EnumerationKind("OverriddenAuto", _alt_namespace=P223)
ProtocolEnum = EnumerationKind("Protocol", _alt_namespace=P223)
PositionEnum = EnumerationKind("Position", _alt_namespace=P223)
RunningNotRunningEnum = EnumerationKind("RunningNotRunning", _alt_namespace=P223)
ThreeSpeedSetting = EnumerationKind("ThreeSpeedSetting")
TopBottomEnum = EnumerationKind("TopBottom", _alt_namespace=P223)
TrueFalseEnum = EnumerationKind("TrueFalse", _alt_namespace=P223)
YesNoEnum = EnumerationKind("YesNo", _alt_namespace=P223)

# Enumerated Values
#
ActiveInactiveEnum.Active = ActiveInactiveEnum("Active", _alt_namespace=P223)
ActiveInactiveEnum.Inactive = ActiveInactiveEnum("Inactive", _alt_namespace=P223)
ActiveInactiveEnum.Unknown = ActiveInactiveEnum("Unknown", _alt_namespace=P223)

#
AITypeEnum.Unknown = AITypeEnum("Unknown", _alt_namespace=P223)
AITypeEnum.RTD = AITypeEnum("RTD", _alt_namespace=P223)
AITypeEnum.Nickel1kRTD = AITypeEnum("Nickel1kRTD", _alt_namespace=P223)
AITypeEnum.Platinum1kRTD = AITypeEnum("Platinum1kRTD", _alt_namespace=P223)
AITypeEnum.VDC_0_10 = AITypeEnum("0-10VDC", _alt_namespace=P223)
AITypeEnum.mA_4_20 = AITypeEnum("4-20mA", _alt_namespace=P223)
AITypeEnum.NTC10kType3 = AITypeEnum("NTC10kType3", _alt_namespace=P223)
AITypeEnum.NTC10kType2 = AITypeEnum("NTC10kType2", _alt_namespace=P223)
AITypeEnum.NTC2250Type2 = AITypeEnum("NTC2250Type2", _alt_namespace=P223)
AITypeEnum.Resistive = AITypeEnum("Resistive", _alt_namespace=P223)

#
AOTypeEnum.VDC_0_10 = AOTypeEnum("0-10VDC", _alt_namespace=P223)
AOTypeEnum.mA_4_20 = AOTypeEnum("4-20mA", _alt_namespace=P223)

#
BITypeEnum.DryContact = BITypeEnum("DryContact", _alt_namespace=P223)
BITypeEnum.PulseCounter = BITypeEnum("PulseCounter", _alt_namespace=P223)

#
BOTypeEnum.Maintained = AOTypeEnum("Maintained", _alt_namespace=P223)
BOTypeEnum.Pulse = AOTypeEnum("Pulse", _alt_namespace=P223)
BOTypeEnum.StartStop = AOTypeEnum("StartStop", _alt_namespace=P223)
BOTypeEnum.Incremental = AOTypeEnum("Incremental", _alt_namespace=P223)

#
Effectiveness.Active = Effectiveness("Active", _alt_namespace=P223)
Effectiveness.Inactive = Effectiveness("Inactive", _alt_namespace=P223)
Effectiveness.Unknown = Effectiveness("Unknown", _alt_namespace=P223)

#
G36AlarmLevel.Level1 = EnumerationKind(
    "Level1", comment="Life Safetey Message", _alt_namespace=G36
)
G36AlarmLevel.Level2 = EnumerationKind(
    "Level2", comment="Critical Equipment Message", _alt_namespace=G36
)
G36AlarmLevel.Level3 = EnumerationKind(
    "Level3", comment="Urgent Message", _alt_namespace=G36
)
G36AlarmLevel.Level4 = EnumerationKind(
    "Level4", comment="Normal Message", _alt_namespace=G36
)

#
HandOffAutoEnum.Hand = HandOffAutoEnum("Hand", _alt_namespace=P223)
HandOffAutoEnum.Off = HandOffAutoEnum("Off", _alt_namespace=P223)
HandOffAutoEnum.Auto = HandOffAutoEnum("Auto", _alt_namespace=P223)

#
HVACOperatingMode.Auto = HVACOperatingMode("Auto")
HVACOperatingMode.CoolOnly = HVACOperatingMode("CoolOnly")
HVACOperatingMode.FanOnly = HVACOperatingMode("FanOnly")
HVACOperatingMode.HeatOnly = HVACOperatingMode("HeatOnly")
HVACOperatingMode.Off = HVACOperatingMode("Off")

#
HVACOperatingStatus.Off = HVACOperatingStatus("Off")
HVACOperatingStatus.Cooling = HVACOperatingStatus("Cooling")
HVACOperatingStatus.Dehumidifying = HVACOperatingStatus("Dehumidifying")
HVACOperatingStatus.Heating = HVACOperatingStatus("Heating")
HVACOperatingStatus.Ventilating = HVACOperatingStatus("Ventilating")

#
LeftRightEnum.Left = LeftRightEnum("Left", _alt_namespace=P223)
LeftRightEnum.Right = LeftRightEnum("Right", _alt_namespace=P223)

#
ManualAutoEnum.Manual = ManualAutoEnum("Manual", _alt_namespace=P223)
ManualAutoEnum.Auto = ManualAutoEnum("Auto", _alt_namespace=P223)

# This is a test example... do we want to fill 223 with
# that kind of enums ?
# Or do we provide a way for people to define their own ?
# Niagara is widely used though....
# Same apply to BACnet....
# Alignment ?
NiagaraStatusEnum.ok = NiagaraStatusEnum("ok", _alt_namespace=P223)
NiagaraStatusEnum.unackedAlarm = NiagaraStatusEnum("unackedAlarm", _alt_namespace=P223)
NiagaraStatusEnum.null = NiagaraStatusEnum("null", _alt_namespace=P223)
NiagaraStatusEnum.overridden = NiagaraStatusEnum("overridden", _alt_namespace=P223)
NiagaraStatusEnum.stale = NiagaraStatusEnum("stale", _alt_namespace=P223)
NiagaraStatusEnum.down = NiagaraStatusEnum("down", _alt_namespace=P223)
NiagaraStatusEnum.fault = NiagaraStatusEnum("fault", _alt_namespace=P223)
NiagaraStatusEnum.disabled = NiagaraStatusEnum("disabled", _alt_namespace=P223)
NiagaraStatusEnum.alarm = NiagaraStatusEnum("alarm", _alt_namespace=P223)

#
NormalAlarmEnum.Normal = NormalAlarmEnum("Normal", _alt_namespace=P223)
NormalAlarmEnum.Alarm = NormalAlarmEnum("Alarm", _alt_namespace=P223)

#
NormalFaultEnum.Normal = NormalFaultEnum("Normal", _alt_namespace=P223)
NormalFaultEnum.Fault = NormalFaultEnum("Fault", _alt_namespace=P223)

#
OccupancyStatus.Unknown = OccupancyStatus("Unknown")
OccupancyStatus.Occupied = OccupancyStatus("Occupied")
OccupancyStatus.Unoccupied = OccupancyStatus("Unoccupied")
OccupancyStatus.Standby = OccupancyStatus("Standby")
OccupancyStatus.Bypass = OccupancyStatus("Bypass")

#
OnOffEnum.On = OnOffEnum("On")
OnOffEnum.Off = OnOffEnum("Off")
OnOffEnum.Unknown = OnOffEnum("Unknown")

#
OpenCloseEnum.Open = OpenCloseEnum("Open", _alt_namespace=P223)
OpenCloseEnum.Close = OpenCloseEnum("Close", _alt_namespace=P223)

#
OverriddenAuto.Auto = OverriddenAuto("Auto", _alt_namespace=P223)
OverriddenAuto.Overridden = OverriddenAuto("Overridden", _alt_namespace=P223)

#
ProtocolEnum.BACnet = ProtocolEnum("BACnet", _alt_namespace=P223)
ProtocolEnum.BACnet_MSTP = ProtocolEnum("BACnet_MSTP", _alt_namespace=P223)
ProtocolEnum.BACnet_IP = ProtocolEnum("BACnet_IP", _alt_namespace=P223)
ProtocolEnum.BACnet_SC = ProtocolEnum("BACnet_SC", _alt_namespace=P223)
ProtocolEnum.Modbus = ProtocolEnum("Modbus", _alt_namespace=P223)
ProtocolEnum.Modbus_RTU = ProtocolEnum("Modbus_RTU", _alt_namespace=P223)
ProtocolEnum.Modbus_TCP = ProtocolEnum("Modbus_TCP", _alt_namespace=P223)
ProtocolEnum.Lonworks = ProtocolEnum("Lonworks", _alt_namespace=P223)

#
PositionEnum.Close = PositionEnum("Close", _alt_namespace=P223)
PositionEnum.Open = PositionEnum("Open", _alt_namespace=P223)
PositionEnum.Moving = PositionEnum("Moving", _alt_namespace=P223)
PositionEnum.Unknown = PositionEnum("Unknown", _alt_namespace=P223)

#
RunningNotRunningEnum.Running = RunningNotRunningEnum("Running", _alt_namespace=P223)
RunningNotRunningEnum.NotRunning = RunningNotRunningEnum(
    "NotRunning", _alt_namespace=P223
)
RunningNotRunningEnum.Unknown = RunningNotRunningEnum("Unknown", _alt_namespace=P223)

#
ThreeSpeedSetting.High = ThreeSpeedSetting("High")
ThreeSpeedSetting.Low = ThreeSpeedSetting("Low")
ThreeSpeedSetting.Medium = ThreeSpeedSetting("Medium")
ThreeSpeedSetting.Off = ThreeSpeedSetting("Off")

#
TopBottomEnum.Top = TopBottomEnum("Top", _alt_namespace=P223)
TopBottomEnum.Bottom = TopBottomEnum("Bottom", _alt_namespace=P223)

# lowercase so we don't clash with internal booleans
TrueFalseEnum.true = TrueFalseEnum("True", _alt_namespace=P223)
TrueFalseEnum.false = TrueFalseEnum("False", _alt_namespace=P223)

#
YesNoEnum.Yes = YesNoEnum("Yes", _alt_namespace=P223)
YesNoEnum.No = YesNoEnum("No", _alt_namespace=P223)

"""
Those are relatively central....let's keep them in core...
S223:EnumerationKind-Direction
    S223:Direction-Inlet
    S223:Direction-Outlet
    S223:Direction-Bidirectional

I created ActiveInactive.... still needed ?
S223:EnumerationKind-Effectiveness
    S223:Effectiveness-Active

RunningNotRunning ?
S223:EnumerationKind-RunStatus
    S223:RunStatus-Off
    S223:RunStatus-On
    S223:RunStatus-Unknown

"""
