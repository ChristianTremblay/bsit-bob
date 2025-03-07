import logging
from typing import Dict

from bob.connections.air import AirConnection
from bob.connections.electricity import Electricity_600VLL_3Ph_60HzInletConnectionPoint
from bob.core import S223, SCRATCH, UNIT, BoundaryConnectionPoint, Role
from bob import application
from bob.equipment.hvac.coil import ChilledWaterCoil, HotWaterCoil
from bob.equipment.hvac.filter import Filter
from bob.equipment.hvac.stats import AirDifferentialStaticPressureSensor

# Prototypes
from bob.scratch.electricity.starter import MotorStarter_600VLL_3Ph_60Hz as MotorStarter
from bob.scratch.electricity.vfd import VFD
from bob.scratch.hvac.damper import ElectricalActuatedProportionalDamper
from bob.scratch.hvac.fan import Fan
from bob.sensor.temperature import AirTemperatureSensor
from bob.template import SystemFromTemplate, template_update

# logging
_log = logging.getLogger(__name__)

_namespace = SCRATCH

ahu_template = {
    "params": {"label": "AHU", "comment": "AHU delivering air to 2 VAV boxes"},
    "sensors": {},
    "equipment": {
        ("RF", Fan): {
            "comment": "Return Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Return,
        },
        ("RF_VFD", VFD): {
            "comment": "Return Air Fan VFD",
        },
        ("SF", Fan): {
            "comment": "Supply Air Fan",
            "electricalInlet": Electricity_600VLL_3Ph_60HzInletConnectionPoint,
            "hasRole": Role.Supply,
        },
        ("SF_Starter", MotorStarter): {
            "comment": "Supply Air Fan Starter",
        },
        ("CLGCOIL", ChilledWaterCoil): {"comment": "Cooling Coil"},
        ("HTGCOIL", HotWaterCoil): {"comment": "Heating coil"},
        ("FILTER", Filter): {"comment": "Filter"},
        ("OADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Outdoor air damper"
        },
        ("MADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Mixed Air Damper"
        },
        ("EADPR", ElectricalActuatedProportionalDamper): {
            "comment": "Exhaust Air Damper"
        },
    },
    "relations": [
        ("self['SF_Starter'].electricalOutlet", ">>", "self['SF'].electricalInlet"),
        ("self['RF_VFD'].electricalOutlet", ">>", "self['RF'].electricalInlet"),
        ('self["OADPR"].airOutlet', ">>", "self.mixedAir"),
        ('self["MADPR"].airOutlet', ">>", "self.mixedAir"),
        ("self.mixedAir", ">>", 'self["FILTER"].airInlet'),
        ('self["FILTER"].airOutlet', ">>", 'self["CLGCOIL"].airInlet'),
        ('self["CLGCOIL"].airOutlet', ">>", 'self["SF"].airInlet'),
        ('self["SF"].airOutlet', ">>", 'self["HTGCOIL"].airInlet'),
        ('self["HTGCOIL"].airOutlet', ">>", "self.supplyAir"),
        ("self.returnAir", ">>", 'self["RF"].airInlet'),
        ('self["RF"].airOutlet', ">>", "self.returnExhaust"),
        ("self.returnExhaust", ">>", 'self["EADPR"].airInlet'),
        ("self.returnExhaust", ">>", 'self["MADPR"].airInlet'),
    ],
}


class AirHandlingUnit(SystemFromTemplate, application.AirHandlingUnit):
    _class_iri = SCRATCH.AirHandlingUnit
    airInlet: BoundaryConnectionPoint
    airOutlet: BoundaryConnectionPoint

    def __init__(self, config: Dict = ahu_template, **kwargs) -> None:
        """
        Air Handling Unit (AHU) is a system that delivers conditioned air to a space or zones

        """
        self.mixedAir = AirConnection(
            label="MixedAirDuct",
            comment="Mix between return air and outdoor air",
        )
        self.returnExhaust = AirConnection(
            label="Return / Exhaust",
            comment="Paths for return or exhaust",
        )
        self.supplyAir = AirConnection(
            label="SUPPLY-DUCT", comment="Supply Air Duct that feed VAV Boxes 1 & 2"
        )
        self.returnAir = AirConnection(
            label="RETURN-DUCT",
            comment="Return Air Duct extracting air from open office",
        )
        _config = template_update({}, config=config)
        kwargs = {**_config.pop("params", {}), **kwargs}
        _log.debug(f"AHU.__init__ {_config} {kwargs}")
        super().__init__(_config, **kwargs)
