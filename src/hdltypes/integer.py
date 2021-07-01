import typing

from hdltypes.array import ArrayProto
from hdltypes.logic import Bit
from hdltypes.range import Range


def bit_length(n: int) -> int:
    if n < 0:
        return bit_length(abs(n) - 1) + 1
    return int.bit_length(n)


def int_to_bits(n: int, length: typing.Optional[int] = None) -> str:
    min_length = bit_length(n)
    if length is None:
        length = min_length
    elif length < min_length:
        raise ValueError("Value cannot fit in given length")
    mask = (1 << length) - 1
    n &= mask
    return [Bit(b) for b in format(n, f"0{length}b")]


def bits_to_int(bits: typing.List[Bit], signed: bool) -> int:
    n = int("".join(str(b) for b in bits), 2)


class _IntegerBase(ArrayProto[Bit]):

    _int_value: int
    _int_valid: bool
    _array_value: typing.List[Bit]
    _array_valid: bool
    _range: int

    @property
    def range(self) -> Range:
        return self._range

    @range.setter
    def range(self, range: Range) -> None:
        if len(range) != len(self._range):
            raise ValueError("new range must have the same length as the old range")
        self._range = range

    def value(self) -> typing.Iterator[T]:
        return (Bit(b) for b in int_to_binstr)

    @typing.overload
    def __getitem__(self, item: int) -> T:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> "ArrayProto[Bit]":
        ...

    def __getitem__(self, item):  # type: ignore

    def _set_int(self) -> None:
        if self._int_valid:
            return
        self._int_value = bitstr_to_int(self._array_value)

    def _set_array(self) -> None:
        if self._array_valid:
            return
        self._array_value =


class Unsigned(_IntegerBase):

    @typing.overload
    def __init__(self, value: typing.Iterable[typing.Any], range: Range):
        ...

    @typing.overload
    def __init__(self, value: typing.Iterable[typing.Any]):
        ...

    @typing.overload
    def __init__(self, value: int, range: Range):
        ...

    @typing.overload
    def __init__(self, value: int):
        ...

    @typing.overload
    def __init__(self, *, range: Range):
        ...

    def __init__(self, value=None, range=None)
        if isinstance()
