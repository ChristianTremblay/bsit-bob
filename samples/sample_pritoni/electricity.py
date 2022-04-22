from pathlib import Path

import electrical_devices as ed
import hvac_devices as hd
import lighting_devices as ld

from bob.connections.electricity import *
from bob.core import bind_model_namespace, dump

model_name = Path(__file__).stem
_namespace = bind_model_namespace(model_name, f"urn:ex/{model_name}/")


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

ed.main_panel["CB#2"] >> hd.ahu["SF-STARTER"] >> hd.ahu["SF"]
ed.main_panel["CB#4"] >> hd.ahu["RF-VFD"] >> hd.ahu["RF"]

if __name__ == "__main__":
    dump()
