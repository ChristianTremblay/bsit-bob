from bob.space.light import *
    
# Light Spaces
openofficeEast_lightspace = LightingSpace(
    label="LightingSpace1", comment="OpenOfficeEast.Light"
)
openofficeWest_lightspace = LightingSpace(
    label="LightingSpace2", comment="OpenOfficeWest.Light"
)
bathroom_lightspace = LightingSpace(
    label="LightingSpace3", comment="Bathroom.Light"
)
corridor_lightspace = LightingSpace(
    label="LightingSpace5", comment="Corridor.Light"
)
privateoffice_lightspace = LightingSpace(
    label="LightingSpace4", comment="PrivateOffice.Light"
)
kitchenette_lightspace = LightingSpace(
    label="LightingSpace6", comment="Kitchenette.Light"
)

# Lighting Zones
lighting_zone_1 = LightingZone(
    label="LightingZone1", comment="Contains OpenOffice Space West"
)
lighting_zone_1 > openofficeWest_lightspace
lighting_zone_2 = LightingZone(
    label="LightingZone2", comment="Contains OpenOffice Space East"
)
lighting_zone_2 > openofficeEast_lightspace

lighting_zone_3 = LightingZone(
    label="LightingZone3", comment="Contains Bathroom Light Space"
)
lighting_zone_3 > bathroom_lightspace

lighting_zone_4 = LightingZone(
    label="LightingZone4", comment="Contains Private Office Light Space"
)
lighting_zone_4 > privateoffice_lightspace

lighting_zone_5 = LightingZone(
    label="LightingZone5", comment="Contains Corridor Light Space"
)
lighting_zone_5 > corridor_lightspace

lighting_zone_6 = LightingZone(
    label="LightingZone6", comment="Contains Kitchenette Light Space"
)
lighting_zone_6 > kitchenette_lightspace