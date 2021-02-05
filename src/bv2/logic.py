from typing import Optional, List, Any


class Logic:

    _repr_map = {
        # 0 and weak 0
        False: 0,
        0: 0,
        "0": 0,
        "L": 0,
        "l": 0,
        # 1 and weak 1
        True: 1,
        1: 1,
        "1": 1,
        "H": 1,
        "h": 1,
        # unknown, unassigned, and weak unknown
        None: 2,
        "X": 2,
        "x": 2,
        "U": 2,
        "u": 2,
        "W": 2,
        "w": 2,
        # high impedance
        "Z": 3,
        "z": 3,
    }

    _and_table: List[List["Logic"]]
    _or_table: List[List["Logic"]]
    _xor_table: List[List["Logic"]]
    _not_table: List["Logic"]

    def __init__(self, value: Optional[Any] = None):
        try:
            self._repr = self._repr_map[value]
        except KeyError:
            raise ValueError(
                "{value!r} is not a {self_type}".format(
                    value=value, self_type=type(self).__name__
                )
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


Logic._repr_map.update(
    {
        Logic("0"): 0,
        Logic("1"): 1,
        Logic("X"): 2,
        Logic("Z"): 3,
    }
)

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
