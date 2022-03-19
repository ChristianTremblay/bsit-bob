from bob.connections.electricity import *

import electrical_devices as ed
import lighting_devices as ld

# Make Electrical connections
ed.dist_panel_cb1 >> [
    ld.openofficeEast_luminaire_1,
    ld.openofficeEast_luminaire_2,
    ld.openofficeWest_luminaire_3,
    ld.openofficeWest_luminaire_4,
]
ed.dist_panel_cb3 >> [
    ld.kitchenette_luminaire_11,
    ld.kitchenette_luminaire_12,
]

ed.dist_panel_cb4 >> [
    ld.bathroom_luminaire_5,
    ld.bathroom_luminaire_6,
    ld.corridor_luminaire_9,
    ld.corridor_luminaire_10,
]

ed.dist_panel_cb5 >> [
    ld.privateoffice_luminaire_7,
    ld.privateoffice_luminaire_8,
]
