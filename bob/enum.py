from rdflib import Graph, URIRef

from .core import (
    G36,
    P223,
    QUANTITYKIND,
    QUDT,
    S223,
    UNIT,
    Constituent,
    Domain,
    EnumerationKind,
    Medium,
    Mix,
    Role,
    Substance,
)

_namespace = S223

# ======================================
# Things that are just Substances
# ======================================
#
Substance.Particle = Particulate = Substance("Particulate")
Particulate.PM1_0 = Particulate.PM1_0 = Particulate(
    "PM1.0"
)  # don't create PM1_0, not clear enough
Particulate.PM2_5 = Particulate.PM2_5 = Particulate("PM2.5")
Particulate.PM10_0 = Particulate.PM10_0 = Particulate("PM10.0")
Substance.Soot = Soot = Substance("Soot")
# ======================================
# Media, Constituents & Mix
# ======================================
#
Constituent.H2O = H2O = Constituent("H2O", label="H2O")
Constituent.Oil = Oil = Constituent("Oil", label="Oil", _alt_namespace=P223)
Constituent.Smoke = Smoke = Constituent("Smoke", label="Smoke", _alt_namespace=P223)
# Gases
Constituent.Ar = Argon = Constituent("Ar", label="Argon", _alt_namespace=P223)
Constituent.CO = CO = Constituent("CO", label="Carbon monoxyde")
Constituent.CO2 = CO2 = Constituent("CO2", label="Carbon dioxyde")
Constituent.NO2 = NO2 = Constituent("NO2", label="NO2", _alt_namespace=P223)
Constituent.CH4 = CH4 = Constituent("CH4", label="CH4", _alt_namespace=P223)
Constituent.NH3 = NH3 = Constituent("NH3", label="NH3", _alt_namespace=P223)
Constituent.H2S = H2S = Constituent("H2S", label="H2S", _alt_namespace=P223)
Constituent.O2 = O2 = Constituent("O2", label="O2", _alt_namespace=P223)
Constituent.O3 = O3 = Constituent("O3", label="O3", _alt_namespace=P223)
Constituent.SO2 = SO2 = Constituent("SO2", label="SO2", _alt_namespace=P223)
Constituent.N = Nitrogen = Constituent("N", label="Nitrogen", _alt_namespace=P223)
Constituent.VOC = VOC = Constituent("VOC", label="VOC", _alt_namespace=P223)
Constituent.Radon = Radon = Constituent("Radon", label="Radon", _alt_namespace=P223)
Constituent.R22 = const_R22 = Constituent("R-22", label="R-22", _alt_namespace=P223)
Constituent.R134A = const_R134A = Constituent(
    "R-134A", label="R-134A", _alt_namespace=P223
)
Constituent.R410A = const_R410A = Constituent(
    "R-410A", label="R-410A", _alt_namespace=P223
)
Constituent.R32 = const_R32 = Constituent("R-32", label="R-32", _alt_namespace=P223)

Constituent.Glycol = Glycol = Constituent("Glycol", label="Glycol")

# Electromagnetic
EM = Constituent("Electro-Magnetic")  # electro-magnetic
EM.Light = Light = EM("Light")
EM.Microwave = Microwave = EM("Microwave")
EM.RF = RF = EM("RF")

Electricity = Constituent("Electricity")
# Electricity
Electricity.AC = Electricity("AC")
Electricity.DC = Electricity("DC")

Electricity.AC10000VLL_1Ph_60Hz = Electricity.AC("10000VLL-1Ph-60Hz")
Electricity.AC10000VLL_3Ph_60Hz = Electricity.AC("10000VLL-3Ph-60Hz")
Electricity.AC10000VLL_5770VLN_1Ph_60Hz = Electricity.AC("10000VLL-5770VLN-1Ph-60Hz")
Electricity.AC10000VLL_5770VLN_3Ph_60Hz = Electricity.AC("10000VLL-5770VLN-3Ph-60Hz")
Electricity.AC110VLN_1Ph_50Hz = Electricity.AC("110VLN-1Ph-50Hz")
Electricity.AC120VLN_1Ph_60Hz = Electricity.AC("120VLN-1Ph-60Hz")
Electricity.AC127VLN_1Ph_50Hz = Electricity.AC("127VLN-1Ph-50Hz")
Electricity.AC139VLN_1Ph_50Hz = Electricity.AC("139VLN-1Ph-50Hz")
Electricity.AC1730VLN_1Ph_60Hz = Electricity.AC("1730VLN-1Ph-60Hz")
Electricity.AC1900VLN_1Ph_60Hz = Electricity.AC("1900VLN-1Ph-60Hz")
Electricity.AC190VLL_110VLN_1Ph_50Hz = Electricity.AC("190VLL-110VLN-1Ph-50Hz")
Electricity.AC190VLL_110VLN_3Ph_50Hz = Electricity.AC("190VLL-110VLN-3Ph-50Hz")
Electricity.AC190VLL_1Ph_50Hz = Electricity.AC("190VLL-1Ph-50Hz")
Electricity.AC190VLL_3Ph_50Hz = Electricity.AC("190VLL-3Ph-50Hz")
Electricity.AC208VLL_120VLN_1Ph_60Hz = Electricity.AC("208VLL-120VLN-1Ph-60Hz")
Electricity.AC208VLL_120VLN_3Ph_60Hz = Electricity.AC("208VLL-120VLN-3Ph-60Hz")
Electricity.AC208VLL_1Ph_60Hz = Electricity.AC("208VLL-1Ph-60Hz")
Electricity.AC208VLL_3Ph_60Hz = Electricity.AC("208VLL-3Ph-60Hz")
Electricity.AC219VLN_1Ph_60Hz = Electricity.AC("219VLN-1Ph-60Hz")
Electricity.AC220VLL_127VLN_1Ph_50Hz = Electricity.AC("220VLL-127VLN-1Ph-50Hz")
Electricity.AC220VLL_127VLN_3Ph_50Hz = Electricity.AC("220VLL-127VLN-3Ph-50Hz")
Electricity.AC220VLL_1Ph_50Hz = Electricity.AC("220VLL-1Ph-50Hz")
Electricity.AC220VLL_3Ph_50Hz = Electricity.AC("220VLL-3Ph-50Hz")
Electricity.AC231VLN_1Ph_50Hz = Electricity.AC("231VLN-1Ph-50Hz")
Electricity.AC2400VLN_1Ph_60Hz = Electricity.AC("2400VLN-1Ph-60Hz")
Electricity.AC240VLL_120VLN_1Ph_60Hz = Electricity.AC("240VLL-120VLN-1Ph-60Hz")
Electricity.AC240VLL_139VLN_1Ph_50Hz = Electricity.AC("240VLL-139VLN-1Ph-50Hz")
Electricity.AC240VLL_139VLN_3Ph_50Hz = Electricity.AC("240VLL-139VLN-3Ph-50Hz")
Electricity.AC240VLL_1Ph_50Hz = Electricity.AC("240VLL-1Ph-50Hz")
Electricity.AC240VLL_1Ph_60Hz = Electricity.AC("240VLL-1Ph-60Hz")
Electricity.AC240VLL_208VLN_120VLN_1Ph_60Hz = Electricity.AC(
    "240VLL-208VLN-120VLN-1Ph-60Hz"
)
Electricity.AC240VLL_208VLN_120VLN_3Ph_60Hz = Electricity.AC(
    "240VLL-208VLN-120VLN-3Ph-60Hz"
)
Electricity.AC240VLL_3Ph_50Hz = Electricity.AC("240VLL-3Ph-50Hz")
Electricity.AC240VLL_3Ph_60Hz = Electricity.AC("240VLL-3Ph-60Hz")
Electricity.AC240VLN_1Ph_50Hz = Electricity.AC("240VLN-1Ph-50Hz")
Electricity.AC24VLN_1Ph_50Hz = Electricity.AC("24VLN-1Ph-50Hz")
Electricity.AC24VLN_1Ph_60Hz = Electricity.AC("24VLN-1Ph-60Hz")
Electricity.AC277VLN_1Ph_60Hz = Electricity.AC("277VLN-1Ph-60Hz")
Electricity.AC3000VLL_1730VLN_1Ph_60Hz = Electricity.AC("3000VLL-1730VLN-1Ph-60Hz")
Electricity.AC3000VLL_1730VLN_3Ph_60Hz = Electricity.AC("3000VLL-1730VLN-3Ph-60Hz")
Electricity.AC3000VLL_1Ph_60Hz = Electricity.AC("3000VLL-1Ph-60Hz")
Electricity.AC3000VLL_3Ph_60Hz = Electricity.AC("3000VLL-3Ph-60Hz")
Electricity.AC3300VLL_1900VLN_1Ph_60Hz = Electricity.AC("3300VLL-1900VLN-1Ph-60Hz")
Electricity.AC3300VLL_1900VLN_3Ph_60Hz = Electricity.AC("3300VLL-1900VLN-3Ph-60Hz")
Electricity.AC3300VLL_1Ph_60Hz = Electricity.AC("3300VLL-1Ph-60Hz")
Electricity.AC3300VLL_3Ph_60Hz = Electricity.AC("3300VLL-3Ph-60Hz")
Electricity.AC3460VLN_1Ph_60Hz = Electricity.AC("3460VLN-1Ph-60Hz")
Electricity.AC347VLN_1Ph_60Hz = Electricity.AC("347VLN-1Ph-60Hz")
Electricity.AC380VLL_1Ph_60Hz = Electricity.AC("380VLL-1Ph-60Hz")
Electricity.AC380VLL_219VLN_1Ph_60Hz = Electricity.AC("380VLL-219VLN-1Ph-60Hz")
Electricity.AC380VLL_219VLN_3Ph_60Hz = Electricity.AC("380VLL-219VLN-3Ph-60Hz")
Electricity.AC380VLL_3Ph_60Hz = Electricity.AC("380VLL-3Ph-60Hz")
Electricity.AC3810VLN_1Ph_60Hz = Electricity.AC("3810VLN-1Ph-60Hz")
Electricity.AC400VLL_1Ph_50Hz = Electricity.AC("400VLL-1Ph-50Hz")
Electricity.AC400VLL_231VLN_1Ph_50Hz = Electricity.AC("400VLL-231VLN-1Ph-50Hz")
Electricity.AC400VLL_231VLN_3Ph_50Hz = Electricity.AC("400VLL-231VLN-3Ph-50Hz")
Electricity.AC400VLL_3Ph_50Hz = Electricity.AC("400VLL-3Ph-50Hz")
Electricity.AC415VLL_1Ph_50Hz = Electricity.AC("415VLL-1Ph-50Hz")
Electricity.AC415VLL_240VLN_1Ph_50Hz = Electricity.AC("415VLL-240VLN-1Ph-50Hz")
Electricity.AC415VLL_240VLN_3Ph_50Hz = Electricity.AC("415VLL-240VLN-3Ph-50Hz")
Electricity.AC415VLL_3Ph_50Hz = Electricity.AC("415VLL-3Ph-50Hz")
Electricity.AC4160VLL_1Ph_60Hz = Electricity.AC("4160VLL-1Ph-60Hz")
Electricity.AC4160VLL_2400VLN_1Ph_60Hz = Electricity.AC("4160VLL-2400VLN-1Ph-60Hz")
Electricity.AC4160VLL_2400VLN_3Ph_60Hz = Electricity.AC("4160VLL-2400VLN-3Ph-60Hz")
Electricity.AC4160VLL_3Ph_60Hz = Electricity.AC("4160VLL-3Ph-60Hz")
Electricity.AC480VLL_1Ph_60Hz = Electricity.AC("480VLL-1Ph-60Hz")
Electricity.AC480VLL_277VLN_1Ph_60Hz = Electricity.AC("480VLL-277VLN-1Ph-60Hz")
Electricity.AC480VLL_277VLN_3Ph_60Hz = Electricity.AC("480VLL-277VLN-3Ph-60Hz")
Electricity.AC480VLL_3Ph_60Hz = Electricity.AC("480VLL-3Ph-60Hz")
Electricity.AC5770VLN_1Ph_60Hz = Electricity.AC("5770VLN-1Ph-60Hz")
Electricity.AC6000VLL_1Ph_60Hz = Electricity.AC("6000VLL-1Ph-60Hz")
Electricity.AC6000VLL_3460VLN_1Ph_60Hz = Electricity.AC("6000VLL-3460VLN-1Ph-60Hz")
Electricity.AC6000VLL_3460VLN_3Ph_60Hz = Electricity.AC("6000VLL-3460VLN-3Ph-60Hz")
Electricity.AC6000VLL_3Ph_60Hz = Electricity.AC("6000VLL-3Ph-60Hz")
Electricity.AC600VLL_1Ph_60Hz = Electricity.AC("600VLL-1Ph-60Hz")
Electricity.AC600VLL_347VLN_1Ph_60Hz = Electricity.AC("600VLL-347VLN-1Ph-60Hz")
Electricity.AC600VLL_347VLN_3Ph_60Hz = Electricity.AC("600VLL-347VLN-3Ph-60Hz")
Electricity.AC600VLL_3Ph_60Hz = Electricity.AC("600VLL-3Ph-60Hz")
Electricity.AC6600VLL_1Ph_60Hz = Electricity.AC("6600VLL-1Ph-60Hz")
Electricity.AC6600VLL_3810VLN_1Ph_60Hz = Electricity.AC("6600VLL-3810VLN-1Ph-60Hz")
Electricity.AC6600VLL_3810VLN_3Ph_60Hz = Electricity.AC("6600VLL-3810VLN-3Ph-60Hz")
Electricity.AC6600VLL_3Ph_60Hz = Electricity.AC("6600VLL-3Ph-60Hz")
Electricity.DC12V = Electricity.DC("12V")
Electricity.DC24V = Electricity.DC("24V")
Electricity.DC380V = Electricity.DC("380V")
Electricity.DC48V = Electricity.DC("48V")
Electricity.DC5V = Electricity.DC("5V")
Electricity.DC6V = Electricity.DC("6V")

Electricity.Signal = Electricity("Signal")
# Electricity.Control = Electricity.Signal("Control", _alt_namespace=P223)
Electricity.OnOffSignal = Electricity.Signal("OnOffSignal", _alt_namespace=P223)
Electricity.ModulatedSignal = Electricity.Signal("Modulated")
Electricity.DC0_10 = Electricity.ModulatedSignal("0-10VDC")
Electricity.MA4_20 = Electricity.ModulatedSignal("4-20mA")
# Electricity.Communication = Electricity.Signal("Communication", _alt_namespace=P223)
Electricity.RS485 = Electricity.Signal("EIA485")
Electricity.Ethernet = Electricity.Signal("Ethernet")
Electricity.IEC14908 = Electricity.Signal("IEC14908")

Mix.PowerAndSignal = PowerAndSignal = Mix("PowerAndSignal", _alt_namespace=P223)
PowerAndSignal.PoE = PowerAndSignal("PoE", _alt_namespace=P223)
PowerAndSignal.PoE.add_constituent(Electricity.DC48V)
PowerAndSignal.PoE.add_constituent(Electricity.Ethernet)
PowerAndSignal.USB = PowerAndSignal("USB", _alt_namespace=P223)
PowerAndSignal.USB.add_constituent(Electricity.DC5V)
# PowerAndSignal.USB.add_constituent(Electricity.Ethernet)

# ===================
# MEDIA FLAVOURS
# ===================
# Air and gases
Mix.Fluid = Fluid = Mix("Fluid")
Fluid.Air = Air = Fluid("Air")
Air.CompressedAir = CompressedAir = Air("CompressedAir")

Fluid.NaturalGas = NaturalGas = Fluid("NaturalGas")
Fluid.Refrigerant = Refrigerant = Fluid("Refrigerant")
Refrigerant.R410A = R410a = Refrigerant("R-410A")
R410a.add_constituent(
    const_R410A, hasQuantityKind=QUANTITYKIND.VolumeFraction, hasUnit=UNIT.PERCENT
)
Refrigerant.R32 = R32 = Refrigerant("R-32", _alt_namespace=P223)
R32.add_constituent(
    const_R32, hasQuantityKind=QUANTITYKIND.VolumeFraction, hasUnit=UNIT.PERCENT
)
Refrigerant.R22 = R22 = Refrigerant("R-22")
R22.add_constituent(
    const_R22, hasQuantityKind=QUANTITYKIND.VolumeFraction, hasUnit=UNIT.PERCENT
)

# Water
Fluid.Water = Water = Fluid("Water")  # constituent in S223 already

Water.ChilledWater = ChilledWater = Water("ChilledWater")

Water.PotableWater = PotableWater = Water("PotableWater", _alt_namespace=P223)

Water.HotWater = HotWater = Water("HotWater")

Water.MixedWater = MixedWater = Water("MixedWater", _alt_namespace=P223)

Water.DomesticWater = DomesticWater = Water("DomesticWater", _alt_namespace=P223)

Water.DomesticHotWater = DomesticHotWater = Water(
    "DomesticHotWater", _alt_namespace=P223
)

Water.CondensedWater = CondensedWater = Water("CondensedWater")

Water.GlycolSolution = GlycolSolution = Water(
    "GlycolSolution"
)  # constituent in S223 already

GlycolSolution.GlycolSolution_15Percent = GlycolSolution_15Percent = GlycolSolution(
    "GlycolSolution-15Percent"
)  # constituent in S223 already
GlycolSolution.GlycolSolution_30Percent = GlycolSolution_30Percent = GlycolSolution(
    "GlycolSolution-30Percent"
)  # constituent in S223 already

Water.Steam = Steam = Water("Steam")

# Light
Light.Visible = Light("Visible")
Light.Infrared = Light("Infrared")

Occupant = Medium("Occupant")

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
Role.Controller = Controller = Role("Controller")
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
Role.Condenser = Condenser = Role("Condenser")
Role.Evaporator = Evaporator = Role("Evaporator")
Role.Storage = Storage = Role("Storage", _alt_namespace=P223)
Role.RunStatus = RunStatus = Role("RunStatus", _alt_namespace=P223)

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
# MotionNoMotionEnum = EnumerationKind("MotionNoMotion", _alt_namespace=P223)
NiagaraStatusEnum = EnumerationKind("NiagaraStatus", _alt_namespace=P223)  # SEE BELOW
NormalAlarmEnum = EnumerationKind("NormalAlarm", _alt_namespace=P223)
NormalFaultEnum = EnumerationKind("NormalFault", _alt_namespace=P223)
OccupancyStatus = EnumerationKind("OccupancyStatus")
OnOffEnum = EnumerationKind("OnOff")
OpenCloseEnum = EnumerationKind("OpenClose", _alt_namespace=P223)
OverriddenAuto = EnumerationKind("OverriddenAuto", _alt_namespace=P223)
ProtocolEnum = EnumerationKind("Protocol", _alt_namespace=P223)
PositionEnum = EnumerationKind("Position", _alt_namespace=P223)
RunStatusEnum = EnumerationKind("RunStatus")
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
MotionEnum = Occupancy("Motion")
MotionTrue = MotionEnum("Motion-True")
MotionFalse = MotionEnum("Motion-False")

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
RunStatusEnum.On = RunStatusEnum("On")
RunStatusEnum.Off = RunStatusEnum("Off")
RunStatusEnum.Unknown = RunStatusEnum("Unknown")

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

# ===================
# Aspects
# ===================
# Enumeration kinds that add context to properties
Aspect = EnumerationKind("Aspect")
Numerical = EnumerationKind("Numerical")
ElectricalVoltagePhases = Aspect("ElectricalVoltagePhases")

Numerical.LineLineVoltage = Numerical("LineLineVoltage")
Numerical.LineNeutralVoltage = Numerical("LineNeutralVoltage")
Numerical.Frequency = Numerical("Frequency")

ElectricalVoltagePhases.ABLineLineVoltage = ElectricalVoltagePhases("ABLineLineVoltage")
ElectricalVoltagePhases.BCLineLineVoltage = ElectricalVoltagePhases("BCLineLineVoltage")
ElectricalVoltagePhases.CALineLineVoltage = ElectricalVoltagePhases("CALineLineVoltage")

ElectricalVoltagePhases.ANLineNeutralVoltage = ElectricalVoltagePhases(
    "ANLineNeutralVoltage"
)
ElectricalVoltagePhases.BNLineNeutralVoltage = ElectricalVoltagePhases(
    "BNLineNeutralVoltage"
)
ElectricalVoltagePhases.CNLineNeutralVoltage = ElectricalVoltagePhases(
    "CNLineNeutralVoltage"
)


Numerical.Delta = Numerical("Delta")
Numerical.DryBulb = Numerical("DryBulb")
Numerical.Latent = Numerical("Latent")
Numerical.Loss = Numerical("Loss")
Numerical.Maximum = Numerical("Maximum")
Numerical.Minimum = Numerical("Minimum")
Aspect.Nominal = Aspect("Nominal")
Numerical.Rated = Numerical("Rated")
Numerical.Sensible = Numerical("Sensible")
Numerical.StandardConditions = Numerical("StandardConditions")
Numerical.Standby = Numerical("Standby")
Numerical.Startup = Numerical("Startup")
Numerical.Threshold = Numerical("Threshold")
Numerical.Total = Numerical("Total")
Numerical.Weight = Numerical("Weight")
Numerical.WetBulb = Numerical("WetBulb")
Aspect.Efficiency = Numerical("Efficiency")

Aspect.PhaseAngle = Numerical("PhaseAngle")
Aspect.PowerFactor = Numerical("PowerFactor")
Aspect.ServiceFactor = Numerical("ServiceFactor")

Aspect.CatalogNumber = Aspect("CatalogNumber")
Aspect.DayOfWeek = Aspect("DayOfWeek")
Aspect.Effectiveness = Aspect("Effectiveness")

Aspect.ElectricalVoltagePhases = Aspect("ElectricalVoltagePhases")
ElectricalPhaseIdentifier = Aspect("ElectricalPhaseIdentifier")
ElectricalPhaseIdentifier.A = ElectricalPhaseIdentifier("A")
ElectricalPhaseIdentifier.B = ElectricalPhaseIdentifier("B")
ElectricalPhaseIdentifier.C = ElectricalPhaseIdentifier("C")
ElectricalPhaseIdentifier.AB = ElectricalPhaseIdentifier("AB")
ElectricalPhaseIdentifier.BC = ElectricalPhaseIdentifier("BC")
ElectricalPhaseIdentifier.CA = ElectricalPhaseIdentifier("CA")
ElectricalPhaseIdentifier.ABC = ElectricalPhaseIdentifier("ABC")
Aspect.Face = Aspect("Face")
Aspect.Manufacturer = Aspect("Manufacturer")
Aspect.Model = Aspect("Model")
Aspect.SerialNumber = Aspect("SerialNumber")
Aspect.Year = Aspect("Year")
