from .core import ConnectionType, register_connection_type, Connection, In, Out


class AnalogSignal(ConnectionType):
    __brick__: "Point"
    connection_type: str = "AnalogSignal"


@register_connection_type
class AnalogSignalConnection(AnalogSignal, Connection):
    pass


class AnalogIn(In, AnalogSignal):
    pass


class AnalogOut(Out, AnalogSignal):
    pass


class BinarySignal(ConnectionType):
    __brick__: "Point"
    connection_type: str = "BinarySignal"


@register_connection_type
class BinarySignalConnection(BinarySignal, Connection):
    pass


class BinaryIn(In, BinarySignal):
    pass


class BinaryOut(Out, BinarySignal):
    pass
