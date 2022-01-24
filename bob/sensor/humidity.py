from __future__ import annotations

from typing import Any
from rdflib import URIRef

from ..core import s223, quantitykind

from .sensor import Sensor

__namespace__ = s223


class HumiditySensor(Sensor):
    node_type: URIRef = s223.HumiditySensor
    hasQuantityKind: quantitykind.RelativeHumidity
