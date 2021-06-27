import typing

from hdltypes.array import _ArrayBase
from hdltypes.logic import Bit, Logic, StdLogic

T = typing.TypeVar("T")


class _LogicArrayBase(_ArrayBase[T]):
    __slots__ = ("_value", "_range")

    def __str__(self) -> str:
        return "".join(str(v) for v in self)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(value={str(self)!r}, range={self._range!r}"


class StdLogicArray(_LogicArrayBase[StdLogic]):
    __slots__ = ()

    _constructor = StdLogic


class LogicArray(_LogicArrayBase[Logic]):
    __slots__ = ()

    _constructor = Logic


class BitArray(_LogicArrayBase[Bit]):
    __slots__ = ()

    _constructor = Bit
