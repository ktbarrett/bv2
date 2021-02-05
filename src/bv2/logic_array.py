from bv2.logic import Logic
from bv2.array import Array, _length

from typing import Callable
import itertools
from functools import reduce, lru_cache
import operator


class LogicArray(Array):

    _conversion = Logic

    def __str__(self) -> str:
        return "".join(map(str, self._value))

    def _bitwise_op(self, other: object, operator: Callable[[Logic, Logic], Logic]):
        if not isinstance(other, type(self)):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("Arrays must be the same length for bitwise operations")
        return type(self)(
            left=1, right=len(self), value=(operator(v, w) for v, w in zip(self, other))
        )

    def __and__(self, other: object) -> "LogicArray":
        """Bitwise logical 'and'"""
        return self._bitwise_op(other, operator.and_)

    def __rand__(self, other: object):
        return self & other

    def __or__(self, other: object) -> "LogicArray":
        """Bitwise logical 'or'"""
        return self._bitwise_op(other, operator.or_)

    def __ror__(self, other: object) -> "LogicArray":
        return self | other

    def __xor__(self, other: object) -> "LogicArray":
        """Bitwise logical 'xor'"""
        return self._bitwise_op(other, operator.xor)

    def __rxor__(self, other: object) -> "LogicArray":
        return self ^ other

    def __invert__(self) -> "LogicArray":
        """Bitwise inversion"""
        return type(self)(left=1, right=len(self), value=(~v for v in self))

    def concat(self, other: "LogicArray"):
        """Concatenate two arrays into one"""
        return type(self)(
            left=1, right=(len(self) + len(other)), value=itertools.chain(self, other)
        )

    def and_reduce(self) -> Logic:
        """Logically 'and's all elements of the array together"""
        return reduce(operator.and_, self)

    def or_reduce(self) -> Logic:
        """Logically 'or's all elements of the array together"""
        return reduce(operator.or_, self)

    def xor_reduce(self) -> Logic:
        """Logically 'xor's all elements of the array together"""
        return reduce(operator.xor, self)

    @property
    def resolvable(self) -> bool:
        """Returns ``True`` if all values in an array are 0 or 1"""
        resolved = (Logic(0), Logic(1))
        return all(v in resolved for v in self)

    @classmethod
    def from_twos_complement(cls, left: int, right: int, value: int) -> "LogicArray":
        """Converts an integer into a logic array using two's complementation representation"""
        length = _length(left, right)
        if value < _min_value_signed(length):
            raise ValueError(
                "Signed integer {value} too small to fit in bounds ({left}, {right})".format(
                    value=value, left=left, right=right
                )
            )
        elif value > _max_value_signed(length):
            raise ValueError(
                "Signed integer {value} too big to fit in bounds ({left}, {right})".format(
                    value=value, left=left, right=right
                )
            )
        if value < 0:
            value &= (1 << length) - 1
        value_binstr = format(value, f"0{length}b")
        return cls(left=left, right=right, value=value_binstr)

    @classmethod
    def from_unsigned(cls, left: int, right: int, value: int) -> "LogicArray":
        """Converts an integer into a logic array using unsigned represetation"""
        length = _length(left, right)
        if value < _min_value_unsigned(length):
            raise ValueError(
                "Unsigned integer {value} too small to fit in bounds ({left}, {right})".format(
                    value=value, left=left, right=right
                )
            )
        elif value > _max_value_unsigned(length):
            raise ValueError(
                "Unsigned integer {value} too big to fit in bounds ({left}, {right})".format(
                    value=value, left=left, right=right
                )
            )
        value_binstr = format(value, f"0{length}b")
        return cls(left=left, right=right, value=value_binstr)

    def to_twos_complement(self) -> int:
        """Converts a logic array into an integer using two's complement representation"""
        if not self.resolvable:
            raise ValueError(
                "{self_type} contains non-0/1 values".format(
                    self_type=type(self).__name__
                )
            )
        unsigned = int(str(self), 2)
        max_value = _max_value_signed(len(self))
        if unsigned > max_value:
            return unsigned - (max_value + 1)
        else:
            return unsigned

    def to_unsigned(self) -> int:
        """Converts a logic array into an integer using unsigned representation"""
        if not self.resolvable:
            raise ValueError(
                "{self_type} contains non-0/1 values".format(
                    self_type=type(self).__name__
                )
            )
        return int(str(self), 2)


@lru_cache
def _min_value_signed(bitwidth: int) -> int:
    return -(2 ** (bitwidth - 1))


@lru_cache
def _max_value_signed(bitwidth: int) -> int:
    return (2 ** (bitwidth - 1)) - 1


def _min_value_unsigned(bitwidth: int) -> int:
    return 0


@lru_cache
def _max_value_unsigned(bitwidth: int) -> int:
    return (2 ** bitwidth) - 1
