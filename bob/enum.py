from rdflib import Graph, URIRef

from .core import (
    Air,
    Domain,
    Electricity,
    EnumerationKind,
    Light,
    Role,
    Substance,
    Water,
    p223,
    s223,
)

_alt_namespace = s223

# ===================
# MEDIA FLAVOURS
# ===================
# Air
Air.CompressedAir = CompressedAir = Air("CompressedAir", _alt_namespace=p223)

# Electricity
Electricity.AC575V_60Hz = Electricity("575V-60Hz")
Electricity.AC480V_60Hz = Electricity("480V-60Hz")
Electricity.AC347V_60Hz = Electricity("347V-60Hz")
Electricity.AC277V_60Hz = Electricity("277V-60Hz")
Electricity.AC208V_60Hz = Electricity("208V-60Hz")
Electricity.AC120V_240V_60Hz = Electricity("120V-240V-60Hz")
Electricity.AC240V_60Hz = Electricity("240V-60Hz")
Electricity.AC120V_60Hz = Electricity("120V-60Hz")
Electricity.AC24V_60Hz = Electricity("24V-60Hz", _alt_namespace=p223)
Electricity.DC48V = Electricity(
    "48V-DC", _alt_namespace=p223
)  # TODO : Create connections
Electricity.DC24V = Electricity(
    "24V-DC", _alt_namespace=p223
)  # TODO : Create connections
Electricity.DC12V = Electricity(
    "12V-DC", _alt_namespace=p223
)  # TODO : Create connections
Electricity.DC5V = Electricity(
    "5V-DC", _alt_namespace=p223
)  # TODO : Create connections
Electricity.OnOffSignal = Electricity("OnOffSignal", _alt_namespace=p223)
Electricity.ModulationSignal = Electricity("ModulationSignal", _alt_namespace=p223)
Electricity.RS485 = Electricity("RS485", _alt_namespace=p223)
Electricity.Ethernet = Electricity("Ethernet", _alt_namespace=p223)

# Water
Water.ChilledWater = ChilledWater = Water("ChilledWater")
Water.PotableWater = PotableWater = Water("PotableWater")
Water.HotWater = HotWater = Water("HotWater")
Water.MixedWater = MixedWater = Water("MixedWater")
Water.DomesticWater = DomesticWater = Water("DomesticWater")
Water.DomesticHotWater = DomesticHotWater = Water("DomesticHotWater")
Water.CondensedWater = CondensedWater = Water("CondensedWater")
Water.GlycoledWater = GlycoledWater = Water("GlycoledWater")
Water.Steam = Steam = Water("Steam")

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
Substance.Smoke = Smoke = Substance("Smoke")
Substance.Particle = Particulate = Substance("Particulate")
Substance.PM1_0 = Particulate.PM1_0 = Particulate(
    "PM1.0"
)  # don't create PM1_0, not clear enough
Substance.PM2_5 = Particulate.PM2_5 = Particulate("PM2.5")
Substance.PM10_0 = Particulate.PM10_0 = Particulate("PM10.0")
Substance.CO = CO = Substance("CO")
Substance.CO2 = CO2 = Substance("CO2")
Substance.NO2 = NO2 = Substance("NO2")
Substance.CH4 = CH4 = Substance("CH4")
Substance.Soot = Soot = Substance("Soot")

# ===================
# Values Enumeration
# ===================
# Enumeration kinds to create hasValue
ActiveInactiveEnum = EnumerationKind("ActiveInactive", _alt_namespace=p223)
Effectiveness = EnumerationKind("Effectiveness")
HandOffAutoEnum = EnumerationKind("HandOffAuto", _alt_namespace=p223)
HVACOperatingMode = EnumerationKind("HVACOperatingMode")
HVACOperatingStatus = EnumerationKind("HVACOperatingStatus")
LeftRightEnum = EnumerationKind("LeftRight", _alt_namespace=p223)
ManualAutoEnum = EnumerationKind("ManualAuto", _alt_namespace=p223)
NiagaraStatusEnum = EnumerationKind("NiagaraStatus", _alt_namespace=p223)  # SEE BELOW
NormalAlarmEnum = EnumerationKind("NormalAlarm", _alt_namespace=p223)
NormalFaultEnum = EnumerationKind("NormalFault", _alt_namespace=p223)
OccupancyEnum = EnumerationKind("Occupancy", _alt_namespace=p223)
OnOffEnum = EnumerationKind("OnOff")
OpenCloseEnum = EnumerationKind("OpenClose", _alt_namespace=p223)
OverriddenAuto = EnumerationKind("OverriddenAuto", _alt_namespace=p223)
PositionEnum = EnumerationKind("Position", _alt_namespace=p223)
RunningNotRunningEnum = EnumerationKind("RunningNotRunning", _alt_namespace=p223)
ThreeSpeedSetting = EnumerationKind("ThreeSpeedSetting")
TopBottomEnum = EnumerationKind("TopBottom", _alt_namespace=p223)
TrueFalseEnum = EnumerationKind("TrueFalse", _alt_namespace=p223)
YesNoEnum = EnumerationKind("YesNo", _alt_namespace=p223)

# Enumerated Values
#
ActiveInactiveEnum.Active = ActiveInactiveEnum("Active", _alt_namespace=p223)
ActiveInactiveEnum.Inactive = ActiveInactiveEnum("Inactive", _alt_namespace=p223)
ActiveInactiveEnum.Unknown = ActiveInactiveEnum("Unknown", _alt_namespace=p223)

#
Effectiveness.Active = Effectiveness("Active", _alt_namespace=p223)
Effectiveness.Inactive = Effectiveness("Inactive", _alt_namespace=p223)
Effectiveness.Unknown = Effectiveness("Unknown", _alt_namespace=p223)

#
HandOffAutoEnum.Hand = HandOffAutoEnum("Hand", _alt_namespace=p223)
HandOffAutoEnum.Off = HandOffAutoEnum("Off", _alt_namespace=p223)
HandOffAutoEnum.Auto = HandOffAutoEnum("Auto", _alt_namespace=p223)

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
LeftRightEnum.Left = LeftRightEnum("Left", _alt_namespace=p223)
LeftRightEnum.Right = LeftRightEnum("Right", _alt_namespace=p223)

#
ManualAutoEnum.Manual = ManualAutoEnum("Manual", _alt_namespace=p223)
ManualAutoEnum.Auto = ManualAutoEnum("Auto", _alt_namespace=p223)

# This is a test example... do we want to fill 223 with
# that kind of enums ?
# Or do we provide a way for people to define their own ?
# Niagara is widely used though....
# Same apply to BACnet....
# Alignment ?
NiagaraStatusEnum.ok = NiagaraStatusEnum("ok", _alt_namespace=p223)
NiagaraStatusEnum.unackedAlarm = NiagaraStatusEnum("unackedAlarm", _alt_namespace=p223)
NiagaraStatusEnum.null = NiagaraStatusEnum("null", _alt_namespace=p223)
NiagaraStatusEnum.overridden = NiagaraStatusEnum("overridden", _alt_namespace=p223)
NiagaraStatusEnum.stale = NiagaraStatusEnum("stale", _alt_namespace=p223)
NiagaraStatusEnum.down = NiagaraStatusEnum("down", _alt_namespace=p223)
NiagaraStatusEnum.fault = NiagaraStatusEnum("fault", _alt_namespace=p223)
NiagaraStatusEnum.disabled = NiagaraStatusEnum("disabled", _alt_namespace=p223)
NiagaraStatusEnum.alarm = NiagaraStatusEnum("alarm", _alt_namespace=p223)

#
NormalAlarmEnum.Normal = NormalAlarmEnum("Normal", _alt_namespace=p223)
NormalAlarmEnum.Alarm = NormalAlarmEnum("Alarm", _alt_namespace=p223)

#
NormalFaultEnum.Normal = NormalFaultEnum("Normal", _alt_namespace=p223)
NormalFaultEnum.Fault = NormalFaultEnum("Fault", _alt_namespace=p223)

#
OccupancyEnum.Unknown = OccupancyEnum("Unknown", _alt_namespace=p223)
OccupancyEnum.Occupied = OccupancyEnum("Occupied", _alt_namespace=p223)
OccupancyEnum.Unoccupied = OccupancyEnum("Unoccupied", _alt_namespace=p223)
OccupancyEnum.Standby = OccupancyEnum("Standby", _alt_namespace=p223)
OccupancyEnum.Bypass = OccupancyEnum("Bypass", _alt_namespace=p223)

#
OnOffEnum.On = OnOffEnum("On")
OnOffEnum.Off = OnOffEnum("Off")
OnOffEnum.Unknown = OnOffEnum("Unknown")

#
OpenCloseEnum.Open = OpenCloseEnum("Open", _alt_namespace=p223)
OpenCloseEnum.Close = OpenCloseEnum("Close", _alt_namespace=p223)

#
OverriddenAuto.Auto = OverriddenAuto("Auto", _alt_namespace=p223)
OverriddenAuto.Overridden = OverriddenAuto("Overridden", _alt_namespace=p223)

#
PositionEnum.Close = PositionEnum("Close", _alt_namespace=p223)
PositionEnum.Open = PositionEnum("Open", _alt_namespace=p223)
PositionEnum.Moving = PositionEnum("Moving", _alt_namespace=p223)
PositionEnum.Unknown = PositionEnum("Unknown", _alt_namespace=p223)

#
RunningNotRunningEnum.Running = RunningNotRunningEnum("Running", _alt_namespace=p223)
RunningNotRunningEnum.NotRunning = RunningNotRunningEnum(
    "NotRunning", _alt_namespace=p223
)
RunningNotRunningEnum.Unknown = RunningNotRunningEnum("Unknown", _alt_namespace=p223)

#
ThreeSpeedSetting.High = ThreeSpeedSetting("High")
ThreeSpeedSetting.Low = ThreeSpeedSetting("Low")
ThreeSpeedSetting.Medium = ThreeSpeedSetting("Medium")
ThreeSpeedSetting.Off = ThreeSpeedSetting("Off")

#
TopBottomEnum.Top = TopBottomEnum("Top", _alt_namespace=p223)
TopBottomEnum.Bottom = TopBottomEnum("Bottom", _alt_namespace=p223)

# lowercase so we don't clash with internal booleans
TrueFalseEnum.true = TrueFalseEnum("True", _alt_namespace=p223)
TrueFalseEnum.false = TrueFalseEnum("False", _alt_namespace=p223)

#
YesNoEnum.Yes = YesNoEnum("Yes", _alt_namespace=p223)
YesNoEnum.No = YesNoEnum("No", _alt_namespace=p223)

"""
Those are relatively central....let's keep them in core...
s223:EnumerationKind-Direction
    s223:Direction-Inlet
    s223:Direction-Outlet
    s223:Direction-Bidirectional

I created ActiveInactive.... still needed ?
s223:EnumerationKind-Effectiveness
    s223:Effectiveness-Active

RunningNotRunning ?
s223:EnumerationKind-RunStatus
    s223:RunStatus-Off
    s223:RunStatus-On
    s223:RunStatus-Unknown

"""
