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
Electricity.AC = Electricity("AC")
Electricity.AC1r73kV_1Ph_60Hz = Electricity.AC("1.73kV-1Ph-60Hz")
Electricity.AC1r91kV_1Ph_60Hz = Electricity.AC("1.91kV-1Ph-60Hz")
Electricity.AC10r0kV_3Ph_60Hz = Electricity.AC("10.0kV-3Ph-60Hz")
Electricity.AC10r0kV_5r77kV_1Ph_60Hz = Electricity.AC("10.0kV-5.77kV-1Ph-60Hz")
Electricity.AC10r0kV_5r77kV_3Ph_60Hz = Electricity.AC("10.0kV-5.77kV-3Ph-60Hz")
Electricity.AC110V_1Ph_50Hz = Electricity.AC("110V-1Ph-50Hz")
Electricity.AC120V_1Ph_60Hz = Electricity.AC("120V-1Ph-60Hz")
Electricity.AC127V_1Ph_50Hz = Electricity.AC("127V-1Ph-50Hz")
Electricity.AC139V_1Ph_50Hz = Electricity.AC("139V-1Ph-50Hz")
Electricity.AC190V_110V_1Ph_50Hz = Electricity.AC("190V-110V-1Ph-50Hz")
Electricity.AC190V_110V_3Ph_50Hz = Electricity.AC("190V-110V-3Ph-50Hz")
Electricity.AC190V_3Ph_50Hz = Electricity.AC("190V-3Ph-50Hz")
Electricity.AC2r4kV_1Ph_60Hz = Electricity.AC("2.4kV-1Ph-60Hz")
Electricity.AC208V_120V_1Ph_60Hz = Electricity.AC("208V-120V-1Ph-60Hz")
Electricity.AC208V_120V_3Ph_60Hz = Electricity.AC("208V-120V-3Ph-60Hz")
Electricity.AC208V_1Ph_60Hz = Electricity.AC("208V-1Ph-60Hz")
Electricity.AC208V_3Ph_60Hz = Electricity.AC("208V-3Ph-60Hz")
Electricity.AC219V_1Ph_60Hz = Electricity.AC("219V-1Ph-60Hz")
Electricity.AC220V_127V_1Ph_50Hz = Electricity.AC("220V-127V-1Ph-50Hz")
Electricity.AC220V_127V_3Ph_50Hz = Electricity.AC("220V-127V-3Ph-50Hz")
Electricity.AC220V_3Ph_50Hz = Electricity.AC("220V-3Ph-50Hz")
Electricity.AC231V_1Ph_50Hz = Electricity.AC("231V-1Ph-50Hz")
Electricity.AC240V_120V_1Ph_60Hz = Electricity.AC("240V-120V_1Ph-60Hz")
Electricity.AC240V_139V_1Ph_50Hz = Electricity.AC("240V-139V-1Ph-50Hz")
Electricity.AC240V_139V_3Ph_50Hz = Electricity.AC("240V-139V-3Ph-50Hz")
Electricity.AC240V_1Ph_50Hz = Electricity.AC("240V-1Ph-50Hz")
Electricity.AC240V_1Ph_60Hz = Electricity.AC("240V-1Ph-60Hz")
Electricity.AC240V_208V_120V_3Ph_60Hz = Electricity.AC("240V-208V-120V-3Ph-60Hz")
Electricity.AC240V_208V_1Ph_60Hz = Electricity.AC("240V-208V-1Ph-60Hz")
Electricity.AC240V_208V_3Ph_60Hz = Electricity.AC("240V-208V-3Ph-60Hz")
Electricity.AC240V_3Ph_50Hz = Electricity.AC("240V-3Ph-50Hz")
Electricity.AC240V_3Ph_60Hz = Electricity.AC("240V-3Ph-60Hz")
Electricity.AC24V_1Ph_60Hz = Electricity.AC("24V-1Ph-60Hz")
Electricity.AC277V_1Ph_60Hz = Electricity.AC("277V-1Ph-60Hz")
Electricity.AC3r0kV_1r73kV_1Ph_60Hz = Electricity.AC("3.0kV-1.73kV-1Ph-60Hz")
Electricity.AC3r0kV_1r73kV_3Ph_60Hz = Electricity.AC("3.0kV-1.73kV-3Ph-60Hz")
Electricity.AC3r0kV_3Ph_60Hz = Electricity.AC("3.0kV-3Ph-60Hz")
Electricity.AC3r3kV_1r91kV_1Ph_60Hz = Electricity.AC("3.3kV-1.91kV-1Ph-60Hz")
Electricity.AC3r3kV_1r91kV_3Ph_60Hz = Electricity.AC("3.3kV-1.91kV-3Ph-60Hz")
Electricity.AC3r3kV_3Ph_60Hz = Electricity.AC("3.3kV-3Ph-60Hz")
Electricity.AC3r46kV_1Ph_60Hz = Electricity.AC("3.46kV-1Ph-60Hz")
Electricity.AC3r81kV_1Ph_60Hz = Electricity.AC("3.81kV-1Ph-60Hz")
Electricity.AC347V_1Ph_60Hz = Electricity.AC("347V-1Ph-60Hz")
Electricity.AC380V_219V_1Ph_60Hz = Electricity.AC("380V-219V-1Ph-60Hz")
Electricity.AC380V_219V_3Ph_60Hz = Electricity.AC("380V-219V-3Ph-60Hz")
Electricity.AC380V_3Ph_60Hz = Electricity.AC("380V-3Ph-60Hz")
Electricity.AC4r16kV_2r4kV_1Ph_60Hz = Electricity.AC("4.16kV-2.4kV-1Ph-60Hz")
Electricity.AC4r16kV_2r4kV_3Ph_60Hz = Electricity.AC("4.16kV-2.4kV-3Ph-60Hz")
Electricity.AC4r16kV_3Ph_60Hz = Electricity.AC("4.16kV-3Ph-60Hz")
Electricity.AC400V_231V_1Ph_50Hz = Electricity.AC("400V-231V-1Ph-50Hz")
Electricity.AC400V_231V_3Ph_50Hz = Electricity.AC("400V-231V-3Ph-50Hz")
Electricity.AC400V_3Ph_50Hz = Electricity.AC("400V-3Ph-50Hz")
Electricity.AC415V_240V_1Ph_50Hz = Electricity.AC("415V-240V-1Ph-50Hz")
Electricity.AC415V_240V_3Ph_50Hz = Electricity.AC("415V-240V-3Ph-50Hz")
Electricity.AC415V_3Ph_50Hz = Electricity.AC("415V-3Ph-50Hz")
Electricity.AC480V_1Ph_60Hz = Electricity.AC("480V-1Ph-60Hz")
Electricity.AC480V_277V_1Ph_60Hz = Electricity.AC("480V-277V-1Ph-60Hz")
Electricity.AC480V_277V_3Ph_60Hz = Electricity.AC("480V-277V-3Ph-60Hz")
Electricity.AC480V_3Ph_60Hz = Electricity.AC("480V-3Ph-60Hz")
Electricity.AC5r77kV_1Ph_60Hz = Electricity.AC("5.77kV-1Ph-60Hz")
Electricity.AC6r0kV_3r46kV_1Ph_60Hz = Electricity.AC("6.0kV-3.46kV-1Ph-60Hz")
Electricity.AC6r0kV_3r46kV_3Ph_60Hz = Electricity.AC("6.0kV-3.46kV-3Ph-60Hz")
Electricity.AC6r0kV_3Ph_60Hz = Electricity.AC("6.0kV-3Ph-60Hz")
Electricity.AC6r6kV_3r81kV_1Ph_60Hz = Electricity.AC("6.6kV-3.81kV-1Ph-60Hz")
Electricity.AC6r6kV_3r81kV_3Ph_60Hz = Electricity.AC("6.6kV-3.81kV-3Ph-60Hz")
Electricity.AC6r6kV_3Ph_60Hz = Electricity.AC("6.6kV-3Ph-60Hz")
Electricity.AC600V_1Ph_60Hz = Electricity.AC("600V-1Ph-60Hz")
Electricity.AC600V_347V_1Ph_60Hz = Electricity.AC("600V-347V-1Ph-60Hz")
Electricity.AC600V_347V_3Ph_60Hz = Electricity.AC("600V-347V-3Ph-60Hz")
Electricity.AC600V_3Ph_60Hz = Electricity.AC("600V-3Ph-60Hz")

Electricity.DC = Electricity("DC")
Electricity.DC12V = Electricity.DC("12V")
Electricity.DC24V = Electricity.DC("24V")
Electricity.DC380V = Electricity.DC("380V")
Electricity.DC48V = Electricity.DC("48V")
Electricity.DC5V = Electricity.DC("5V")

Electricity.Signal = Electricity("Signal")
# Electricity.Control = Electricity.Signal("Control", _alt_namespace=P223)
Electricity.OnOffSignal = Electricity.Signal("OnOffSignal", _alt_namespace=P223)
Electricity.ModulatedSignal = Electricity.Signal("Modulated")
Electricity.USB = Electricity.Signal("USB")
Electricity.DC0_10 = Electricity.ModulatedSignal("0-10VDC")
Electricity.MA4_20 = Electricity.ModulatedSignal("4-20mA")
Electricity.Communication = Electricity.Signal("Communication", _alt_namespace=P223)
Electricity.RS485 = Electricity.Communication("EIA-485")
Electricity.Ethernet = Electricity.Communication("Ethernet")
Electricity.IEC14908 = Electricity.Communication("IEC14908")

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
AnalogSignalTypeEnum = EnumerationKind("Analog", _alt_namespace=P223)
BinarySignalTypeEnum = EnumerationKind("Binary", _alt_namespace=P223)
Effectiveness = EnumerationKind("Effectiveness")
G36AlarmLevel = EnumerationKind("G36AlarmLevels", _alt_namespace=G36)
HandOffAutoEnum = EnumerationKind("HandOffAuto", _alt_namespace=P223)
HVACOperatingMode = EnumerationKind("HVACOperatingMode")
HVACOperatingStatus = EnumerationKind("HVACOperatingStatus")
LeftRightEnum = EnumerationKind("LeftRight", _alt_namespace=P223)
ManualAutoEnum = EnumerationKind("ManualAuto", _alt_namespace=P223)
MotionNoMotionEnum = EnumerationKind("MotionNoMotion", _alt_namespace=P223)
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
AnalogSignalTypeEnum.Unknown = AnalogSignalTypeEnum("Unknown", _alt_namespace=P223)
AnalogSignalTypeEnum.RTD = AnalogSignalTypeEnum("RTD", _alt_namespace=P223)
AnalogSignalTypeEnum.Nickel1kRTD = AnalogSignalTypeEnum(
    "Nickel1kRTD", _alt_namespace=P223
)
AnalogSignalTypeEnum.Platinum1kRTD = AnalogSignalTypeEnum(
    "Platinum1kRTD", _alt_namespace=P223
)
AnalogSignalTypeEnum.VDC_0_10 = AnalogSignalTypeEnum("0-10VDC", _alt_namespace=P223)
AnalogSignalTypeEnum.mA_4_20 = AnalogSignalTypeEnum("4-20mA", _alt_namespace=P223)
AnalogSignalTypeEnum.NTC10kType3 = AnalogSignalTypeEnum(
    "NTC10kType3", _alt_namespace=P223
)
AnalogSignalTypeEnum.NTC10kType2 = AnalogSignalTypeEnum(
    "NTC10kType2", _alt_namespace=P223
)
AnalogSignalTypeEnum.NTC2250Type2 = AnalogSignalTypeEnum(
    "NTC2250Type2", _alt_namespace=P223
)
AnalogSignalTypeEnum.Resistive = AnalogSignalTypeEnum("Resistive", _alt_namespace=P223)

#
BinarySignalTypeEnum.DryContact = BinarySignalTypeEnum(
    "DryContact", _alt_namespace=P223
)
BinarySignalTypeEnum.Pulse = BinarySignalTypeEnum("Pulse", _alt_namespace=P223)
BinarySignalTypeEnum.StartStop = BinarySignalTypeEnum("StartStop", _alt_namespace=P223)
BinarySignalTypeEnum.Incremental = BinarySignalTypeEnum(
    "Incremental", _alt_namespace=P223
)

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

#
MotionNoMotionEnum.Motion = MotionNoMotionEnum("Motion", _alt_namespace=P223)
MotionNoMotionEnum.NoMotion = MotionNoMotionEnum("NoMotion", _alt_namespace=P223)

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
# ===================
# Aspects
# ===================
# Enumeration kinds that add context to properties
Context = EnumerationKind("Context")
CtxAttribute = Context("Attribute")
Dimensioned = Context("Dimensioned")
Dimensionless = Context("Dimensionless")

Dimensioned.LineLineVoltage = Dimensioned("LineLineVoltage", _alt_namespace=P223)
Dimensioned.ABLineLineVoltage = Dimensioned("ABLineLineVoltage", _alt_namespace=P223)
Dimensioned.BCLineLineVoltage = Dimensioned("BCLineLineVoltage", _alt_namespace=P223)
Dimensioned.CALineLineVoltage = Dimensioned("CALineLineVoltage", _alt_namespace=P223)
Dimensioned.LineNeutralVoltage = Dimensioned("LineNeutralVoltage", _alt_namespace=P223)
Dimensioned.ANLineNeutralVoltage = Dimensioned(
    "ANLineNeutralVoltage", _alt_namespace=P223
)
Dimensioned.BNLineNeutralVoltage = Dimensioned(
    "BNLineNeutralVoltage", _alt_namespace=P223
)
Dimensioned.CNLineNeutralVoltage = Dimensioned(
    "CNLineNeutralVoltage", _alt_namespace=P223
)
Dimensioned.NominalFrequency = Dimensioned("NominalFrequency", _alt_namespace=P223)

Dimensioned.Delta = Dimensioned("Delta")
Dimensioned.DryBulb = Dimensioned("DryBulb")
Dimensioned.Latent = Dimensioned("Latent")
Dimensioned.Loss = Dimensioned("Loss")
Dimensioned.Maximum = Dimensioned("Maximum")
Dimensioned.Minimum = Dimensioned("Minimum")
Dimensioned.Nominal = Dimensioned("Nominal")
Dimensioned.Rated = Dimensioned("Rated")
Dimensioned.Sensible = Dimensioned("Sensible")
Dimensioned.StandardConditions = Dimensioned("StandardConditions")
Dimensioned.Standby = Dimensioned("Standby")
Dimensioned.Startup = Dimensioned("Startup")
Dimensioned.Threshold = Dimensioned("Threshold")
Dimensioned.Total = Dimensioned("Total")
Dimensioned.Weight = Dimensioned("Weight")
Dimensioned.WetBulb = Dimensioned("WetBulb")
Dimensionless.Efficiency = Dimensioned("Efficiency")
Dimensionless.NumberOfElectricalPhases = Dimensioned("NumberOfElectricalPhases")
Dimensionless.PhaseAngle = Dimensioned("PhaseAngle")
Dimensionless.PowerFactor = Dimensioned("PowerFactor")
Dimensionless.ServiceFactor = Dimensioned("ServiceFactor")

CtxAttribute.CatalogNumber = CtxAttribute("CatalogNumber")
CtxAttribute.DayOfWeek = CtxAttribute("DayOfWeek")
CtxAttribute.Effectiveness = CtxAttribute("Effectiveness")
ElectricalPhaseIdentifier = CtxAttribute("ElectricalPhaseIdentifier")
ElectricalPhaseIdentifier.A = ElectricalPhaseIdentifier("A")
ElectricalPhaseIdentifier.B = ElectricalPhaseIdentifier("B")
ElectricalPhaseIdentifier.C = ElectricalPhaseIdentifier("C")
ElectricalPhaseIdentifier.AB = ElectricalPhaseIdentifier("AB")
ElectricalPhaseIdentifier.BC = ElectricalPhaseIdentifier("BC")
ElectricalPhaseIdentifier.CA = ElectricalPhaseIdentifier("CA")
ElectricalPhaseIdentifier.ABC = ElectricalPhaseIdentifier("ABC")
CtxAttribute.Face = CtxAttribute("Face")
CtxAttribute.Manufacturer = CtxAttribute("Manufacturer")
CtxAttribute.Model = CtxAttribute("Model")
CtxAttribute.SerialNumber = CtxAttribute("SerialNumber")
CtxAttribute.Year = CtxAttribute("Year")
