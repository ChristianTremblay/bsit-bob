from .core import ConnectionType, register_connection_type, Connection, Inlet, Outlet


class AnalogSignal(ConnectionType):
    connection_type: str = "AnalogSignal"


@register_connection_type
class AnalogSignalConnection(AnalogSignal, Connection):
    pass


class AnalogIn(Inlet, AnalogSignal):
    pass


class AnalogOut(Outlet, AnalogSignal):
    pass


class BinarySignal(ConnectionType):
    connection_type: str = "BinarySignal"


@register_connection_type
class BinarySignalConnection(BinarySignal, Connection):
    pass


class BinaryIn(Inlet, BinarySignal):
    pass


class BinaryOut(Outlet, BinarySignal):
    pass
