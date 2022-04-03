from pathlib import Path

from bob.core import bind_model_namespace, dump

import lighting_devices as ld
import lighting_spaces as ls
import physical_spaces as ps
import hvac_devices as hd

model_name = Path(__file__).stem
__namespace__ = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


ld.kitchenette_luminaire_11.lightOutlet >> ld.kitch_light_conn
ld.kitchenette_luminaire_12.lightOutlet >> ld.kitch_light_conn
ld.kitch_light_conn >> ls.kitchenette_lightspace.lightInlet

# There is a occupancy space for Kitchenette... go figure
ld.kitchenette_movement.hasMeasurementLocation = ls.kitchenette_lightspace
ld.kitchenette_movement.hasPhysicalLocation = ps.kitchenette

ld.privateoffice_luminaire_7.lightOutlet >> ld.privateoffice_light_conn
ld.privateoffice_luminaire_8.lightOutlet >> ld.privateoffice_light_conn
ld.privateoffice_light_conn >> ls.privateoffice_lightspace.lightInlet

ld.corridor_luminaire_9.lightOutlet >> ld.corridor_light_conn
ld.corridor_luminaire_10.lightOutlet >> ld.corridor_light_conn
ld.corridor_light_conn >> ls.corridor_lightspace.lightInlet

ld.corridor_movement.hasMeasurementLocation = ls.corridor_lightspace
ld.corridor_movement.hasPhysicalLocation = ps.corridor

ld.bathroom_luminaire_5.lightOutlet >> ld.bathroom_light_conn
ld.bathroom_luminaire_6.lightOutlet >> ld.bathroom_light_conn
ld.bathroom_light_conn >> ls.bathroom_lightspace.lightInlet
ld.bathroom_movement.hasMeasurementLocation = ls.bathroom_lightspace
ld.bathroom_movement.hasPhysicalLocation = ps.bathroom


ld.openofficeEast_luminaire_1.lightOutlet >> ld.openofficeEast_light_conn
ld.openofficeEast_luminaire_2.lightOutlet >> ld.openofficeEast_light_conn
ld.openofficeEast_light_conn >> ls.openofficeEast_lightspace.lightInlet

ld.openofficeWest_luminaire_3.lightOutlet >> ld.openofficeWest_light_conn
ld.openofficeWest_luminaire_4.lightOutlet >> ld.openofficeWest_light_conn
ld.openofficeWest_light_conn >> ls.openofficeWest_lightspace.lightInlet

ld.openoffice_movement.hasMeasurementLocation = ls.openofficeWest_lightspace
ld.openoffice_movement.hasPhysicalLocation = ps.openoffice

hd.window1.naturalLight >> ld.natural_ligth_conn
hd.window2.naturalLight >> ld.natural_ligth_conn
ld.natural_ligth_conn >> ls.openofficeEast_lightspace.naturalLightInlet
ld.natural_ligth_conn >> ls.openofficeWest_lightspace.naturalLightInlet

if __name__ == "__main__":
    dump()
