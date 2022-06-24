from pathlib import Path

from bob.core import bind_model_namespace, dump
from bob.properties import OccupancyStatus
from bob.space.light import LightingSpace, LightingZone

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


# Light Spaces
openofficeNorth_lightspace = LightingSpace(
    label="LightingSpace1", comment="OpenOffice North.Light"
)
openofficeSouth_lightspace = LightingSpace(
    label="LightingSpace2", comment="OpenOffice South.Light"
)
bathroom_lightspace = LightingSpace(label="LightingSpace3", comment="Bathroom.Light")
corridor_lightspace = LightingSpace(label="LightingSpace5", comment="Corridor.Light")
privateoffice_lightspace = LightingSpace(
    label="LightingSpace4", comment="PrivateOffice.Light"
)
kitchenette_lightspace = LightingSpace(
    label="LightingSpace6", comment="Kitchenette.Light"
)

# Lighting Zones
lighting_zone_1 = LightingZone(
    label="LightingZone1",
    comment="Contains OpenOffice Space North",
    occupancy=OccupancyStatus(),
)
lighting_zone_1 > openofficeNorth_lightspace
lighting_zone_2 = LightingZone(
    label="LightingZone2",
    comment="Contains OpenOffice Space South",
    occupancy=OccupancyStatus(),
)
lighting_zone_2 > openofficeSouth_lightspace

lighting_zone_3 = LightingZone(
    label="LightingZone3",
    comment="Contains Bathroom Light Space",
    occupancy=OccupancyStatus(),
)
lighting_zone_3 > bathroom_lightspace

lighting_zone_4 = LightingZone(
    label="LightingZone4",
    comment="Contains Private Office Light Space",
    occupancy=OccupancyStatus(),
)
lighting_zone_4 > privateoffice_lightspace

lighting_zone_5 = LightingZone(
    label="LightingZone5",
    comment="Contains Corridor Light Space",
    occupancy=OccupancyStatus(),
)
lighting_zone_5 > corridor_lightspace

lighting_zone_6 = LightingZone(
    label="LightingZone6",
    comment="Contains Kitchenette Light Space",
    occupancy=OccupancyStatus(),
)
lighting_zone_6 > kitchenette_lightspace

if __name__ == "__main__":
    dump()
