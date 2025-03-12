import os
import logging

print(f"{os.getenv('BOB_LOG') = }")

logging.basicConfig(level=logging.WARNING)
print(f"{logging.root} level={logging.root.level} handlers={logging.root.handlers}")

x = logging.getLogger("bob")
print(f"{x} level={x.level} handlers={x.handlers}")

y = logging.getLogger("bob.core")
print(f"{y} level={y.level} handlers={y.handlers}")
print()


print(f"{x} level={x.level} handlers={x.handlers}")
print(f"{y} level={y.level} handlers={y.handlers}")
print("----------")

from bob.equipment.hvac.valve import TwoWayActuatedOnOffValve

valve = TwoWayActuatedOnOffValve(label="valve")
print(f"{valve = }")
