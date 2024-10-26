from pathlib import Path

from bob.core import bind_model_namespace, dump, Setpoint
from bob.space.hvac import HVACSpace, HVACZone, OccupancyStatus

model_name = Path(__file__).stem
global_ns = Path(__file__).parent.stem
_namespace = bind_model_namespace(model_name, f"urn:{global_ns}:{model_name}/")

# HVAC Spaces
zone1_hvac = HVACSpace(
    label="HVACSpace1",
    comment="OpenOffice.HVAC",
    occupancy=OccupancyStatus(),
    temperature_setpoint=Setpoint(),
)
zone2_hvac = HVACSpace(
    label="HVACSpace2", comment="Bathroom.HVAC", occupancy=OccupancyStatus()
)
zone3_hvac = HVACSpace(
    label="HVACSpace4", comment="CorridorNorth.HVAC", occupancy=OccupancyStatus()
)
zone4_hvac = HVACSpace(
    label="HVACSpace5", comment="CorridorSouth.HVAC", occupancy=OccupancyStatus()
)

# HVAC Zones
hvac_zone_1 = HVACZone(
    label="HVACZone1",
    comment="HVAC Zone 1 contains open office, bathroom, private office and corridor north",
    occupancy=OccupancyStatus(),
)
hvac_zone_1 > zone1_hvac
hvac_zone_1 > zone2_hvac
hvac_zone_1 > zone3_hvac
hvac_zone_1 > zone4_hvac

# hvac_zone_2.airInlet.mapsTo = kitchenette_hvac.ductAirInlet
# hvac_zone_2.airOutlet.mapsTo = corridorSouth_hvac.ductAirOutlet

if __name__ == "__main__":
    dump()
