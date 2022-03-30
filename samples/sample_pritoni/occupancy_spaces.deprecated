from bob.space.occupancy import *

# Occupancy Spaces
openoffice_occ_space = OccupancySpace(
    label="OccupancySpace1", comment="Occupancy space of Open Office"
)
kitchenette_occ_space = OccupancySpace(
    label="OccupancySpace6", comment="Occupancy Space of kitechnette"
)

openoffice_occ_zone = OccupancyZone(
    label="OpenOfficeOccZone", comment="Occupancy Zone for Open Office"
)
kitchenette_occ_zone = OccupancyZone(
    label="KitchenetteOccZone", comment="Occupancy Zone for Kitchenette"
)

openoffice_occ_zone > openoffice_occ_space
kitchenette_occ_zone > kitchenette_occ_space
