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
    s223,
)

_namespace = s223

# ===================
# MEDIA FLAVOURS
# ===================
# Air
Air.CompressedAir = CompressedAir = Air("CompressedAir")

# Electricity
Electricity.AC575V_60Hz = Electricity("575V-60Hz")
Electricity.AC480V_60Hz = Electricity("480V-60Hz")
Electricity.AC347V_60Hz = Electricity("347V-60Hz")
Electricity.AC277V_60Hz = Electricity("277V-60Hz")
Electricity.AC208V_60Hz = Electricity("208V-60Hz")
Electricity.AC120V_240V_60Hz = Electricity("120V-240V-60Hz")
Electricity.AC240V_60Hz = Electricity("240V-60Hz")
Electricity.AC120V_60Hz = Electricity("120V-60Hz")
Electricity.AC24V_60Hz = Electricity("24V-60Hz")
Electricity.DC48V = Electricity("48V-DC")  # TODO : Create connections
Electricity.DC24V = Electricity("24V-DC")  # TODO : Create connections
Electricity.DC12V = Electricity("12V-DC")  # TODO : Create connections
Electricity.DC5V = Electricity("5V-DC")  # TODO : Create connections
Electricity.OnOffSignal = Electricity("OnOffSignal")
Electricity.ModulationSignal = Electricity("ModulationSignal")
Electricity.RS485 = Electricity("RS485")
Electricity.Ethernet = Electricity("Ethernet")

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
Role.Recirculating = Recirculating = Role("Recirculating")
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
ActiveInactiveEnum = EnumerationKind("ActiveInactive")
Effectiveness = EnumerationKind("Effectiveness")
HandOffAutoEnum = EnumerationKind("HandOffAuto")
HVACOperatingMode = EnumerationKind("HVACOperatingMode")
HVACOperatingStatus = EnumerationKind("HVACOperatingStatus")
LeftRightEnum = EnumerationKind("LeftRight")
ManualAutoEnum = EnumerationKind("ManualAuto")
NiagaraStatusEnum = EnumerationKind("NiagaraStatus")  # SEE BELOW
NormalAlarmEnum = EnumerationKind("NormalAlarm")
NormalFaultEnum = EnumerationKind("NormalFault")
OccupancyEnum = EnumerationKind("Occupancy")
OnOffEnum = EnumerationKind("OnOff")
OpenCloseEnum = EnumerationKind("OpenClose")
OverriddenAuto = EnumerationKind("OverriddenAuto")
PositionEnum = EnumerationKind("Position")
RunningNotRunningEnum = EnumerationKind("RunningNotRunning")
ThreeSpeedSetting = EnumerationKind("ThreeSpeedSetting")
TopBottomEnum = EnumerationKind("TopBottom")
TrueFalseEnum = EnumerationKind("TrueFalse")
YesNoEnum = EnumerationKind("YesNo")

# Enumerated Values
#
ActiveInactiveEnum.Active = ActiveInactiveEnum("Active")
ActiveInactiveEnum.Inactive = ActiveInactiveEnum("Inactive")
ActiveInactiveEnum.Unknown = ActiveInactiveEnum("Unknown")

#
Effectiveness.Active = Effectiveness("Active")
Effectiveness.Inactive = Effectiveness("Inactive")
Effectiveness.Unknown = Effectiveness("Unknown")

#
HandOffAutoEnum.Hand = HandOffAutoEnum("Hand")
HandOffAutoEnum.Off = HandOffAutoEnum("Off")
HandOffAutoEnum.Auto = HandOffAutoEnum("Auto")

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
LeftRightEnum.Left = LeftRightEnum("Left")
LeftRightEnum.Right = LeftRightEnum("Right")

#
ManualAutoEnum.Manual = ManualAutoEnum("Manual")
ManualAutoEnum.Auto = ManualAutoEnum("Auto")

# This is a test example... do we want to fill 223 with
# that kind of enums ?
# Or do we provide a way for people to define their own ?
# Niagara is widely used though....
# Same apply to BACnet....
# Alignment ?
NiagaraStatusEnum.ok = NiagaraStatusEnum("ok")
NiagaraStatusEnum.unackedAlarm = NiagaraStatusEnum("unackedAlarm")
NiagaraStatusEnum.null = NiagaraStatusEnum("null")
NiagaraStatusEnum.overridden = NiagaraStatusEnum("overridden")
NiagaraStatusEnum.stale = NiagaraStatusEnum("stale")
NiagaraStatusEnum.down = NiagaraStatusEnum("down")
NiagaraStatusEnum.fault = NiagaraStatusEnum("fault")
NiagaraStatusEnum.disabled = NiagaraStatusEnum("disabled")
NiagaraStatusEnum.alarm = NiagaraStatusEnum("alarm")

#
NormalAlarmEnum.Normal = NormalAlarmEnum("Normal")
NormalAlarmEnum.Alarm = NormalAlarmEnum("Alarm")

#
NormalFaultEnum.Normal = NormalFaultEnum("Normal")
NormalFaultEnum.Fault = NormalFaultEnum("Fault")

#
OccupancyEnum.Unknown = OccupancyEnum("Unknown")
OccupancyEnum.Occupied = OccupancyEnum("Occupied")
OccupancyEnum.Unoccupied = OccupancyEnum("Unoccupied")
OccupancyEnum.Standby = OccupancyEnum("Standby")
OccupancyEnum.Bypass = OccupancyEnum("Bypass")

#
OnOffEnum.On = OnOffEnum("On")
OnOffEnum.Off = OnOffEnum("Off")
OnOffEnum.Unknown = OnOffEnum("Unknown")

#
OpenCloseEnum.Open = OpenCloseEnum("Open")
OpenCloseEnum.Close = OpenCloseEnum("Close")

#
OverriddenAuto.Auto = OverriddenAuto("Auto")
OverriddenAuto.Overridden = OverriddenAuto("Overridden")

#
PositionEnum.Close = PositionEnum("Close")
PositionEnum.Open = PositionEnum("Open")
PositionEnum.Moving = PositionEnum("Moving")
PositionEnum.Unknown = PositionEnum("Unknown")

#
RunningNotRunningEnum.Running = RunningNotRunningEnum("Running")
RunningNotRunningEnum.NotRunning = RunningNotRunningEnum("NotRunning")
RunningNotRunningEnum.Unknown = RunningNotRunningEnum("Unknown")

#
ThreeSpeedSetting.High = ThreeSpeedSetting("High")
ThreeSpeedSetting.Low = ThreeSpeedSetting("Low")
ThreeSpeedSetting.Medium = ThreeSpeedSetting("Medium")
ThreeSpeedSetting.Off = ThreeSpeedSetting("Off")

#
TopBottomEnum.Top = TopBottomEnum("Top")
TopBottomEnum.Bottom = TopBottomEnum("Bottom")

# lowercase so we don't clash with internal booleans
TrueFalseEnum.true = TrueFalseEnum("True")
TrueFalseEnum.false = TrueFalseEnum("False")

#
YesNoEnum.Yes = YesNoEnum("Yes")
YesNoEnum.No = YesNoEnum("No")

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
