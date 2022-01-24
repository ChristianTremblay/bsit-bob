from .core import bind_namespace
from .node import Property

__namespace__ = bind_namespace(
    "g36", "http://data.ashrae.org/standard223/1.0/extension/g36#"
)


class AnalogIn(Property):
    pass


class AnalogOut(Property):
    pass


class BinaryIn(Property):
    pass


class BinaryOut(Property):
    pass
