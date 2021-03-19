from typing import Optional, Any, Iterable, Iterator, overload
from functools import cached_property


class Array:
    r"""
    Fixed-size, arbitrarily-indexed, heterogenous array type
    Arrays are similar, but different from Python :class:`list`\ s.
    An array can store values of any type or multiple types at a time, just like a :class:`list`.
    Unlike :class:`list`\ s, an array's size cannot change.

    An array's indexes can start or end at any integer value, they are not limited to 0-based indexing.
    The left and right arguments, known as `bounds`, are used to describe the indexing.
    The bounds are used to determine the size of the array, which is the number of indexes between the two bounds.
    Bounds can be ascending (-3, 'to', 4), or descending (7, 'downto', 2).

    There is a special case where the direction mismatches the bounds resulting in a negative length array.
    These are called "null arrays" and the length of the array is 0.

    Args
        left: Left-most index of the array (inclusive).
        direction: 'to' for an array with ascending indexes, 'downto' for descending indexes
        right: Right-most index of the array (inclusive).
        value: Initial value for the array. Must be the same size as the array.
    """

    @overload
    def __init__(self, left: int, direction: str, right: int, value: Optional[Iterable[Any]] = None):
        pass

    @overload
    def __init__(self, *, left: int, right: int, value: Optional[Iterable[Any]] = None):
        pass

    @overload
    def __init__(self, left: int, right: int, *, value: Optional[Iterable[Any]] = None):
        pass

    @overload
    def __init__(self, left: int, right: int, value: Iterable[Any]):
        pass

    @overload
    def __init__(self, value: Iterable[Any]):
        pass

    @overload
    def __init__(self, *, value: Iterable[Any]):
        pass

    def __init__(self, left=None, direction=None, right=None, value=None):
        if isinstance(left, int) and isinstance(direction, str) and isinstance(right, int):
            """(int, str, int, Optional)"""
            self._left = left
            self._right = right
            self._direction = direction
            if direction not in ("to", "downto"):
                raise ValueError("Direction must be 'to' or 'downto'")
        elif isinstance(left, int) and direction is None and isinstance(right, int):
            """(int, None, int, Optional)"""
            self._left = left
            self._right = right
            self._direction = self._guess_direction(left, right)
        elif isinstance(left, int) and isinstance(direction, int) and right is None:
            """(int, int, None, Optional)"""
            self._left = left
            self._right = direction
            self._direction = self._guess_direction(left, direction)
        elif isinstance(left, int) and isinstance(direction, int) and right is not None and value is None:
            """(int, int, Value, None)"""
            self._left = left
            self._right = direction
            self._direction = self._guess_direction(left, direction)
            value = right
        elif left is not None and direction is None and right is None and value is None:
            """(Value, None, None, None)"""
            self._value = list(left)
            self._left = 0
            self._direction = 'to'
            self._right = len(self._value) - 1
            return  # exit early since we don't need to set or check self._value
        elif left is None and direction is None and right is None and value is not None:
            """(None, None, None, Value)"""
            self._value = list(value)
            self._left = 0
            self._direction = 'to'
            self._right = len(self._value) - 1
            return  # exit early since we don't need to set or check self._value
        elif left is None and direction is None and right is None and value is None:
            """(None, None, None, value=None)"""
            raise TypeError("Must specify bounds, initial value, or both")
        else:
            raise TypeError("Invalid bounds specification")

        if value is None:
            self._value = [None] * self.length
        else:
            self._value = list(value)
            if len(self._value) != self.length:
                raise ValueError(
                    "Init value of length '{}' does not fit in given bounds {}".format(
                        len(self._value), (self.left, self.right)
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

    @property
    def direction(self):
        """Array direction. Either 'to' or 'downto'."""
        return self._direction

    @cached_property
    def length(self) -> int:
        """Number of elements the array can store"""
        return self._length(self.left, self.direction, self.right)

    def __len__(self) -> int:
        """Number of elements the array can store"""
        return self.length

    def indexes(self) -> Iterable[int]:
        """Returns :class:`range` iterable of indexes from left to right"""
        if self.direction == 'to':
            return range(self.left, self.right + 1, 1)
        else:
            return range(self.left, self.right - 1, -1)

    def values(self) -> Iterable[Any]:
        """Returns copy of stored values"""
        return tuple(self._value)

    def __iter__(self) -> Iterator[Any]:
        return iter(self._value)

    def __reversed__(self) -> Iterator[Any]:
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
            direction = self._guess_direction(left, right)
            if direction is not self.direction:
                raise IndexError(
                    "expecting {self_direction!r} slice, got {direction!r} slice".format(
                        self_direction=self.direction,
                        direction=direction
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
            direction = self._guess_direction(left, right)
            if direction is not self.direction:
                raise IndexError(
                    "expecting {self_direction!r} slice, got {direction!r} slice".format(
                        self_direction=self.direction,
                        direction=direction
                    )
                )
            left_i = self._translate_index(left)
            right_i = self._translate_index(right)
            length = self._length(left_i, direction, right_i)
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
        return "{cls_name}({left!r}, {direction!r}, {right!r}, value={value!r})".format(
            cls_name=type(self).__name__,
            left=self.left,
            direction=self.direction,
            right=self.right,
            value=self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(v == w for v, w in zip(self, other))

    @staticmethod
    def _guess_direction(left: int, right: int) -> str:
        return 'to' if left <= right else 'downto'

    @staticmethod
    def _length(left: int, direction: str, right: int) -> int:
        if direction == 'to':
            return max(right - left + 1, 0)
        else:
            return max(left - right + 1, 0)
