import typing
from functools import lru_cache

Self = typing.TypeVar("Self", bound="StdLogic")


_U = 0
_X = 1
_0 = 2
_1 = 3
_Z = 4
_L = 5
_H = 6
_W = 7
__ = 8


_repr_table = {
    # unassigned
    "U": _U,
    "u": _U,
    # unknown
    "X": _X,
    "x": _X,
    # 0
    "0": _0,
    0: _0,
    False: _0,
    # 1
    "1": _1,
    1: _1,
    True: _1,
    # high impedance
    "Z": _Z,
    "z": _Z,
    # weak 0
    "L": _L,
    "l": _L,
    # weak 1
    "H": _H,
    "h": _H,
    # weak unknown
    "W": _W,
    "w": _W,
    # don't care
    "-": __,
}


_str_table = ("U", "X", "0", "1", "Z", "L", "H", "W", "-")


_bool_table = (None, None, False, True, None, None, None, None, None)


_int_table = (None, None, 0, 1, None, None, None, None, None)


_and_table = (
    (_U, _U, _0, _U, _U, _U, _0, _U, _U),  # U
    (_U, _X, _0, _X, _X, _X, _0, _X, _X),  # X
    (_0, _0, _0, _0, _0, _0, _0, _0, _0),  # 0
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # 1
    (_U, _X, _0, _X, _X, _X, _0, _X, _X),  # Z
    (_U, _X, _0, _X, _X, _X, _0, _X, _X),  # W
    (_0, _0, _0, _0, _0, _0, _0, _0, _0),  # L
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # H
    (_U, _X, _0, _X, _X, _X, _0, _X, _X),  # -
)  #  U   X   0   1   Z   W   L   H   -


_or_table = (
    (_U, _U, _U, _1, _U, _U, _U, _1, _U),  # U
    (_U, _X, _X, _1, _X, _X, _X, _1, _X),  # X
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # 0
    (_1, _1, _1, _1, _1, _1, _1, _1, _1),  # 1
    (_U, _X, _X, _1, _X, _X, _X, _1, _X),  # Z
    (_U, _X, _X, _1, _X, _X, _X, _1, _X),  # W
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # L
    (_1, _1, _1, _1, _1, _1, _1, _1, _1),  # H
    (_U, _X, _X, _1, _X, _X, _X, _1, _X),  # -
)  #  U   X   0   1   Z   W   L   H   -


_xor_table = (
    (_U, _U, _U, _U, _U, _U, _U, _U, _U),  # U
    (_U, _X, _X, _X, _X, _X, _X, _X, _X),  # X
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # 0
    (_U, _X, _1, _0, _X, _X, _1, _0, _X),  # 1
    (_U, _X, _X, _X, _X, _X, _X, _X, _X),  # Z
    (_U, _X, _X, _X, _X, _X, _X, _X, _X),  # W
    (_U, _X, _0, _1, _X, _X, _0, _1, _X),  # L
    (_U, _X, _1, _0, _X, _X, _1, _0, _X),  # H
    (_U, _X, _X, _X, _X, _X, _X, _X, _X),  # -
)  #  U   X   0   1   Z   W   L   H   -


_not_table = (_U, _X, _1, _0, _X, _X, _1, _0, _X)
#              U   X   0   1   Z   W   L   H   -


class StdLogic:
    __slots__ = ("_repr",)
    _repr: int

    @classmethod
    @lru_cache(maxsize=None)
    def _make(cls: typing.Type[Self], repr: typing.Optional[int]) -> Self:
        self = super().__new__(cls)
        self._repr = repr
        return self

    @lru_cache(maxsize=None)
    def __new__(cls: typing.Type[Self], value: typing.Any = "U") -> Self:
        repr = _repr_table.get(value)
        if repr is None:
            raise ValueError(f"{value!r} is not a valid {cls.__qualname__}")
        return cls._make(repr)

    def __str__(self) -> str:
        return _str_table[self._repr]

    def __int__(self) -> int:
        res = _int_table[self._repr]
        if res is None:
            raise ValueError(f"{self!r} is not convertible to int")
        return res

    def __bool__(self) -> bool:
        res = _bool_table[self._repr]
        if res is None:
            raise ValueError(f"{self!r} is not convertible to bool")
        return res

    def __hash__(self) -> int:
        return self._repr

    def __eq__(self, other: typing.Any) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return self._repr == other._repr

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({str(self)!r})"

    @typing.overload
    def __and__(self: Self, other: Self) -> Self:
        ...

    @typing.overload
    def __and__(self, other: Self) -> Self:  # type: ignore
        ...

    def __and__(self, other):  # type: ignore
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)._make(_and_table[self._repr][other._repr])

    def __rand__(self, other):  # type: ignore
        return self & other

    @typing.overload
    def __or__(self: Self, other: Self) -> Self:
        ...

    @typing.overload
    def __or__(self, other: Self) -> Self:  # type: ignore
        ...

    def __or__(self, other):  # type: ignore
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)._make(_or_table[self._repr][other._repr])

    def __ror__(self, other):  # type: ignore
        return self | other

    @typing.overload
    def __xor__(self: Self, other: Self) -> Self:
        ...

    @typing.overload
    def __xor__(self, other: Self) -> Self:  # type: ignore
        ...

    def __xor__(self, other):  # type: ignore
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)._make(_xor_table[self._repr][other._repr])

    def __rxor__(self, other):  # type: ignore
        return self ^ other

    def __invert__(self: Self) -> Self:
        return type(self)._make(_not_table[self._repr])


_repr_table.update(
    {
        StdLogic("U"): _U,
        StdLogic("X"): _X,
        StdLogic("0"): _0,
        StdLogic("1"): _1,
        StdLogic("Z"): _Z,
        StdLogic("L"): _L,
        StdLogic("H"): _H,
        StdLogic("W"): _W,
        StdLogic("-"): __,
    }
)


class Logic(StdLogic):
    __slots__ = ()

    @lru_cache(maxsize=None)
    def __new__(cls: typing.Type[Self], value: typing.Any = "X") -> Self:
        self = super().__new__(cls, value=value)  # type: ignore
        if self._repr not in {_X, _0, _1, _Z}:
            raise ValueError(f"{value!r} is not a valid {cls.__qualname__}")
        return self


_repr_table.update(
    {
        Logic("X"): _X,
        Logic("0"): _0,
        Logic("1"): _1,
        Logic("Z"): _Z,
    }
)


class Bit(Logic):
    __slots__ = ()

    @lru_cache(maxsize=None)
    def __new__(cls: typing.Type[Self], value: typing.Any = "0") -> Self:
        self = super().__new__(cls, value=value)  # type: ignore
        if self._repr not in {_0, _1}:
            raise ValueError(f"{value!r} is not a valid {cls.__qualname__}")
        return self


_repr_table.update(
    {
        Bit("0"): _0,
        Bit("1"): _1,
    }
)


if typing.TYPE_CHECKING:
    reveal_type(StdLogic(0) & StdLogic(1))
    reveal_type(StdLogic(0) & Logic(1))
    reveal_type(StdLogic(0) & Bit(1))
    reveal_type(Logic(0) & StdLogic(1))
    reveal_type(Logic(0) & Logic(1))
    reveal_type(Logic(0) & Bit(1))
    reveal_type(Bit(0) & StdLogic(1))
    reveal_type(Bit(0) & Logic(1))
    reveal_type(Bit(0) & Bit(1))
