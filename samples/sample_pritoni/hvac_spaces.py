from bob.space.hvac import *
    
# HVAC Spaces
openoffice_hvac = HVACSpace(label="HVACSpace1", comment="OpenOffice.HVAC")
bathroom_hvac = HVACSpace(label="HVACSpace2", comment="Bathroom.HVAC")
corridorNorth_hvac = HVACSpace(label="HVACSpace4", comment="CorridorNorth.HVAC")
corridorSouth_hvac = HVACSpace(label="HVACSpace5", comment="CorridorSouth.HVAC")
privateoffice_hvac = HVACSpace(label="HVACSpace3", comment="PrivateOffice.HVAC")
kitchenette_hvac = HVACSpace(label="HVACSpace6", comment="Kitchenette.HVAC")

# HVAC Zones
hvac_zone_1 = HVACZone(
    label="HVACZone1",
    comment="HVAC Zone 1 contains open office, bathroom, private office and corridor north",
)
hvac_zone_1 > openoffice_hvac
hvac_zone_1 > bathroom_hvac
hvac_zone_1 > corridorNorth_hvac
hvac_zone_1 > privateoffice_hvac

hvac_zone_2 = HVACZone(
    label="HVACZone2", comment="HVAC Zone 2 contains Kitchenette and Corridor South"
)
hvac_zone_2 > kitchenette_hvac
hvac_zone_2 > corridorSouth_hvac
