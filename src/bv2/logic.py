from typing import Optional, List, Any, Dict


class Logic:

    # class tables
    _constructor_table: Dict[Any, "Logic"]
    _and_table: List[List["Logic"]]
    _or_table: List[List["Logic"]]
    _xor_table: List[List["Logic"]]
    _not_table: List["Logic"]

    # attributes
    _repr: int

    def __new__(cls, value: Optional[Any] = None) -> "Logic":
        try:
            return cls._constructor_table[value]
        except KeyError:
            raise ValueError(
                "{value!r} is not a {cls}".format(value=value, cls=cls.__name__)
            ) from None

    def __and__(self, other: object) -> "Logic":
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._and_table[self._repr][other._repr]

    def __rand__(self, other: object) -> "Logic":
        return self & other

    def __or__(self, other: object) -> "Logic":
        if not isinstance(other, type(self)):
            return NotImplemented
        return Logic(self._or_table[self._repr][other._repr])

    def __ror__(self, other: object) -> "Logic":
        return self | other

    def __xor__(self, other: object) -> "Logic":
        if not isinstance(other, type(self)):
            return NotImplemented
        return Logic(self._xor_table[self._repr][other._repr])

    def __rxor__(self, other: object) -> "Logic":
        return self ^ other

    def __invert__(self) -> "Logic":
        return Logic(self._not_table[self._repr])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._repr == other._repr

    def __repr__(self) -> str:
        return "{}({!r})".format(type(self).__name__, str(self))

    def __str__(self) -> str:
        return "01XZ"[self._repr]

    def __bool__(self) -> bool:
        if self._repr < 2:
            return bool(self._repr)
        raise ValueError("Cannot convert non-0/1 value to bool")

    def __int__(self) -> int:
        if self._repr < 2:
            return self._repr
        raise ValueError("Cannot convert non-0/1 value to int")

    def __hash__(self) -> int:
        return self._repr


_0 = object.__new__(Logic)
_0._repr = 0
_1 = object.__new__(Logic)
_1._repr = 1
_X = object.__new__(Logic)
_X._repr = 2
_Z = object.__new__(Logic)
_Z._repr = 3

Logic._constructor_table = {
    # 0 and weak 0
    False: _0,
    0: _0,
    "0": _0,
    "L": _0,
    "l": _0,
    _0: _0,
    # 1 and weak 1
    True: _1,
    1: _1,
    "1": _1,
    "H": _1,
    "h": _1,
    _1: _1,
    # unknown, unassigned, and weak unknown
    None: _X,
    "X": _X,
    "x": _X,
    "U": _X,
    "u": _X,
    "W": _X,
    "w": _X,
    _X: _X,
    # high impedance
    "Z": _Z,
    "z": _Z,
    _Z: _Z,
}

Logic._and_table = [
    [Logic(v) for v in "0000"],
    [Logic(v) for v in "01XX"],
    [Logic(v) for v in "0XXX"],
    [Logic(v) for v in "0XXX"],
]

Logic._or_table = [
    [Logic(v) for v in "01XX"],
    [Logic(v) for v in "1111"],
    [Logic(v) for v in "X1XX"],
    [Logic(v) for v in "X1XX"],
]

Logic._xor_table = [
    [Logic(v) for v in "01XX"],
    [Logic(v) for v in "10XX"],
    [Logic(v) for v in "XXXX"],
    [Logic(v) for v in "XXXX"],
]

Logic._not_table = [Logic(v) for v in "10XX"]
