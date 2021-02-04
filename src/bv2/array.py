from typing import Optional, Any, Iterable, Iterator, overload
from functools import cached_property, reduce
import operator


class Array:
    """
    Fixed-size, arbitrarily-indexed, heterogenous array type

    Arrays are similar, but different from Python :class:`list`_s.
    An array can store values of any type or multiple types at a time, just like a :class:`list`.
    Unlike :class:`list`_s, an array's size cannot change.
    An array's indexes can start or end at any integer value, they are not limited to 0-based indexing.
    The left and right arguments, known as `bounds`, are used to describe the indexing.
    The bounds are used to determine the size of the array, which is the number of indexes between the two bounds.
    Bounds can be ascending (-3, 4), or descending (7, 2).

    Args
        left: Left-most index of the array (inclusive).
        right: Right-most index of the array (inclusive).
        value: Initial value for the array. Must be the same size as the array.
    """

    @staticmethod
    def _conversion(value: Any = None) -> Any:
        """
        Takes a value and converts it to the element type of the Array

        Meant to be overriden by subclasses.
        All override should be able to take 0 or 1 arguments.
        """
        return value

    def __init__(self, left: int, right: int, *, value: Optional[Iterable[Any]] = None):
        self._left = left
        self._right = right
        conversion = self._conversion
        if value is None:
            self._value = [conversion() for _ in range(len(self))]
        else:
            self._value = [conversion(v) for v in value]
            if len(self._value) != len(self):
                raise ValueError(
                    "Init value of length '{}'' does not fit in given bounds {}".format(
                        len(self._value), (left, right)
                    )
                )

    @property
    def left(self) -> int:
        """Left bound"""
        return self._left

    @property
    def right(self) -> int:
        """Right bound"""
        return self._right

    @cached_property
    def ascending(self) -> bool:
        """:class`True` if array has ascending bounds"""
        return _ascending(self.left, self.right)

    @cached_property
    def length(self) -> int:
        """Number of elements the array can store"""
        return _length(self.left, self.right)

    def __len__(self) -> int:
        """Number of elements the array can store"""
        return self.length

    def indexes(self) -> Iterable[int]:
        """Returns :class:`range` iterable of indexes from left to right"""
        if self.ascending:
            return range(self.left, self.right + 1, 1)
        else:
            return range(self.left, self.right - 1, -1)

    def values(self) -> Iterable[Any]:
        """Returns copy of stored values"""
        return tuple(self._value)

    def __iter__(self) -> Iterator[Any]:
        """Iterator over the values"""
        return iter(self.values())

    def __reversed__(self) -> Iterator[Any]:
        """Reversed iterator over the values"""
        return reversed(self._value)

    @overload
    def __getitem__(self, item: int) -> Any:
        """Returns element at given index"""

    @overload
    def __getitem__(self, item: slice) -> "Array":
        """
        Returns new array containing the given slice

        New array's bounds are the same as the slice.
        Do not supply a ``step`` to the slice.
        Empty slice ``start`` value means the left bound.
        Empty slice ``stop`` value means the right bound.
        The entire array can be easily copied using the syntax ``array[:]``.
        """

    def __getitem__(self, item):
        if isinstance(item, int):
            idx = self._translate_index(item)
            return self._value[idx]
        elif isinstance(item, slice):
            if item.start is not None:
                left = item.start
            else:
                left = self.left
            if item.stop is not None:
                right = item.stop
            else:
                right = self.right
            if item.step is not None:
                raise IndexError("don't specify the step")
            ascending = _ascending(left, right)
            if ascending is not self.ascending:
                raise IndexError(
                    "expecting {self_ascending} slice, got {ascending} slice".format(
                        self_ascending=(
                            "ascending" if self.ascending else "descending"
                        ),
                        ascending=("ascending" if ascending else "descending"),
                    )
                )
            left_i = self._translate_index(left)
            right_i = self._translate_index(right)
            value = self._value[left_i : (right_i + 1)]
            return type(self)(left=left, right=right, value=value)
        else:
            raise TypeError(
                "indexes must be ints or slices, not '{type}'".format(
                    type=type(item).__name__
                )
            )

    @overload
    def __setitem__(self, item: int, value: Any) -> None:
        """Sets the value of the array at the given index"""

    @overload
    def __setitem__(self, item: slice, value: Iterable[Any]) -> None:
        """
        Sets multiple values in the given slice

        Value can be any sized iterable.
        Value must be same length as the slice being assigned to.
        Do not supply a ``step`` to the slice.
        Empty slice ``start`` value means the left bound.
        Empty slice ``stop`` value means the right bound.
        The entire array can be easily assigned to using the syntax ``array[:] = value``.
        """

    def __setitem__(self, item, value):
        conversion = self._conversion
        if isinstance(item, int):
            idx = self._translate_index(item)
            self._value[idx] = conversion(value)
        elif isinstance(item, slice):
            if item.start is not None:
                left = item.start
            else:
                left = self.left
            if item.stop is not None:
                right = item.stop
            else:
                right = self.right
            if item.step is not None:
                raise IndexError("don't specify the step")
            ascending = _ascending(left, right)
            if ascending is not self.ascending:
                raise IndexError(
                    "expecting {self_ascending} slice, got {ascending} slice".format(
                        self_ascending=(
                            "ascending" if self.ascending else "descending"
                        ),
                        ascending=("ascending" if ascending else "descending"),
                    )
                )
            left_i = self._translate_index(left)
            right_i = self._translate_index(right)
            length = _length(left_i, right_i)
            value = tuple(conversion(v) for v in value)
            if len(value) != length:
                raise ValueError(
                    "value of length '{value_length}'' not the same length as the slice {slice_length}".format(
                        value_length=len(value), slice_length=length
                    )
                )
            self._value[left_i : (right_i + 1)] = value
        else:
            raise TypeError(
                "indexes must be ints or slices, not '{type}'".format(
                    type=type(item).__name__
                )
            )

    def _translate_index(self, index: int) -> int:
        if self.ascending:
            idx = index - self.left
        else:
            idx = self.left - index
        if idx < 0 or len(self._value) <= idx:
            raise IndexError(
                "Index out of bounds {left}, {right}): {index}".format(
                    left=self.left, right=self.right, index=index
                )
            )
        return idx

    def __repr__(self) -> str:
        return "{cls_name}({left}, {right}, value={value!r})".format(
            cls_name=type(self).__name__,
            left=self.left,
            right=self.right,
            value=self._value,
        )

    def __eq__(self, other: "Array") -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        if len(self) != len(other):
            return False
        if not all(v == w for v, w in zip(self, other)):
            return False
        return True

    def __hash__(self) -> int:
        return reduce(operator.xor, (hash(v) for v in self))


def _ascending(left: int, right: int) -> bool:
    return left < right


def _length(left: int, right: int) -> int:
    if _ascending(left, right):
        return right - left + 1
    else:
        return left - right + 1
