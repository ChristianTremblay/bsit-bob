# multimethods
#
# This is a re-work of multimethods from Eli Bendersky
# [http://eli.thegreenplace.net] who placed it the public domain.  This
# derivative is also in the public domain.
#

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple, Union, get_origin

import itertools
import inspect

__all__ = ["multimethod"]


# Maps function.__name__ -> _MultiMethod object.
_multi_registry: Dict[str, _MultiMethod] = {}


def all_subclasses(cls: type) -> List[type]:
    """Returns a list of *all* subclasses of cls, recursively."""
    if not hasattr(cls, "__subclasses__"):
        return []

    subclasses: List[type] = cls.__subclasses__()
    for subcls in cls.__subclasses__():
        subclasses.extend(all_subclasses(subcls))
    return subclasses


class _MultiMethod:
    """Maps tuples of argument types to function to call for these types."""

    name: str
    argc: int
    typemap: Dict[Tuple[type, ...], Callable[..., Any]]
    funcs: List[Callable[..., Any]]

    def __init__(self, name: str) -> None:
        self.name = name
        self.typemap = {}
        self.funcs = []
        self.argc = -1

    def __call__(self, *args: Any) -> Any:
        # if the typemap is empty it hasn't been populated yet
        if not self.typemap:
            self.populate_typemap()

        types = list(arg.__class__ for arg in args)

        # pad the list of types with None if there aren't enough
        if len(types) > self.argc:
            raise RuntimeError(f"too many parameters, expecting {self.argc}")
        elif len(types) < self.argc:
            types.extend([type(None)] * (self.argc - len(types)))

        if list in types:
            for i, arg_type in enumerate(types):
                if arg_type is list:
                    parm_subtypes = set(elem.__class__ for elem in args[i])

                    # make an ordered dict of the first subtype __mro__
                    top_mro = {s: None for s in parm_subtypes.pop().__mro__}

                    # keep the classes in the top_mro that are in each of
                    # the other parm_subtypes __mro__
                    for cls in parm_subtypes:
                        top_mro = {s: None for s in top_mro if s in cls.__mro__}

                    types[i] = List[next(iter(top_mro))]  # type: ignore[index,misc]

        method = self.typemap.get(tuple(types), None)
        if not method:
            raise TypeError("no match %r: %s" % (self.name, types))

        return method(*args)

    def register_function(self, func: Callable[..., Any]) -> None:
        # if the typemap is populated you cannot add more patterns (which
        # is testable here) and you cannot subclass existing classes (which
        # would mean setting every class used to "final")
        if self.typemap:
            raise RuntimeError("type map already populated")

        func_sig = inspect.signature(func)
        argc = len(func_sig.parameters)
        if self.argc < 0:
            self.argc = argc
        elif argc != self.argc:
            raise RuntimeError(f"expecting {self.argc} parameters, got {argc}")

        # add the function for the population step
        self.funcs.append(func)

    def populate_typemap(self):
        # map each function in the order it was registered
        for func in self.funcs:
            types_with_subclasses = []

            func_sig = inspect.signature(func)
            for parameter in func_sig.parameters.values():
                parm_type = parameter.annotation
                if isinstance(parm_type, str):
                    parm_type = eval(parm_type, func.__globals__)
                parm_origin = get_origin(parm_type)

                if inspect.isclass(parm_type):
                    types_with_subclasses.append(
                        [parm_type] + all_subclasses(parm_type)
                    )

                elif parm_origin is Union:
                    parm_types = set()
                    for parm_subtype in parm_type.__args__:
                        if not inspect.isclass(parm_subtype):
                            raise TypeError(
                                f"parameter {parameter.name} subtype: {parm_subtype!r}"
                            )
                        parm_types.add(parm_subtype)
                        parm_types.update(all_subclasses(parm_subtype))

                    types_with_subclasses.append(parm_types)

                elif parm_origin is list:
                    parm_subtype = parm_type.__args__[0]
                    if not inspect.isclass(parm_subtype):
                        raise TypeError(
                            f"parameter {parameter.name} subtype: {parm_subtype!r}"
                        )

                    parm_types = set([List[parm_subtype]])
                    for more_subtypes in all_subclasses(parm_subtype):
                        parm_types.add(List[more_subtypes])

                    types_with_subclasses.append(parm_types)

                else:
                    raise TypeError(
                        f"parameter {parameter.name}: {parm_type!r} {parm_origin!r}"
                    )

            for type_tuple in itertools.product(*types_with_subclasses):
                # Here we explicitly support overriding the registration, so that
                # more specific dispatches can override earlier-defined generic
                # dispatches.
                self.typemap[type_tuple] = func


def multimethod(func: Callable[..., Any]) -> _MultiMethod:
    name = func.__name__
    mm = _multi_registry.get(name)
    if mm is None:
        mm = _multi_registry[name] = _MultiMethod(name)
    mm.register_function(func)
    return mm
