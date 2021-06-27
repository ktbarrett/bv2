import typing
from abc import abstractmethod
from itertools import chain

from hdltypes.range import Range

T = typing.TypeVar("T")


@typing.runtime_checkable
class ArrayProto(typing.Protocol[T]):
    @abstractmethod
    def __init__(self, value: typing.Iterable[T], range: Range) -> None:
        ...

    @property  # type: ignore
    @abstractmethod
    def range(self) -> Range:
        ...

    @range.setter  # type: ignore
    @abstractmethod
    def range(self, range: Range) -> None:
        ...

    @abstractmethod
    def value(self) -> typing.Iterator[T]:
        ...

    @typing.overload
    def __getitem__(self, item: int) -> T:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> "ArrayProto[T]":
        ...

    @abstractmethod
    def __getitem__(self, item):  # type: ignore
        ...

    @typing.overload
    def __setitem__(self, item: int, value: T) -> None:
        ...

    @typing.overload
    def __setitem__(self, item: slice, value: typing.Iterable[T]) -> None:
        ...

    @abstractmethod
    def __setitem__(self, item, value):  # type: ignore
        ...

    @property
    def left(self) -> int:
        return self.range.left

    @property
    def right(self) -> int:
        return self.range.right

    @property
    def direction(self) -> str:
        return self.range.direction

    def __len__(self) -> int:
        return len(self.range)

    def __iter__(self) -> typing.Iterator[T]:
        return self.value()

    def __reversed__(self) -> typing.Iterator[T]:
        return reversed(tuple(self.value()))

    def __contains__(self, value: typing.Any) -> bool:
        return value in self.value()

    def index(
        self,
        value: typing.Any,
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None,
    ) -> int:
        if start is None:
            start = self.left
        if stop is None:
            stop = self.right
        for i, v in zip(Range(start, self.direction, stop), self[start:stop]):
            if v == value:
                return i
        raise ValueError(f"{value!r} is not in array")

    def count(self, value: typing.Any) -> int:
        return sum(1 for v in self if v == value)

    def __eq__(self, other: typing.Any) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}(value={tuple(self.value())!r}, range={self.range})"

    def __concat__(self: "ArrayProto[T]", other: "ArrayProto[T]") -> "ArrayProto[T]":
        return type(self)(
            value=chain(self, other), range=Range(0, "to", len(self) + len(other) - 1)
        )


class _ArrayBase(ArrayProto[T]):
    _constructor: typing.Callable[[typing.Any], T]

    _value: typing.List[typing.Any]
    _range: Range

    @typing.overload
    def __init__(self, value: typing.Iterable[typing.Any], range: Range) -> None:
        ...

    @typing.overload
    def __init__(self, value: typing.Iterable[typing.Any]) -> None:
        ...

    @typing.overload
    def __init__(self, *, range: Range) -> None:
        ...

    def __init__(self, value=None, range=None):  # type: ignore
        construct = type(self)._constructor
        if value is not None and range is not None:
            value = [construct(v) for v in value]
            if len(range) != len(value):
                raise ValueError("value and range arguments must have the same length")
        elif value is not None and range is None:
            value = [construct(v) for v in value]
            range = Range(0, "to", len(value) - 1)
        elif value is None and range is not None:
            value = [construct(None) for _ in range]
        else:
            raise TypeError("must pass value, range, or both")
        self._value = value
        self._range = range

    @property
    def range(self) -> Range:
        return self._range

    @range.setter
    def range(self, range: Range) -> None:
        if len(range) != len(self._range):
            raise ValueError("new range must have the same length as the old range")
        self._range = range

    def value(self) -> typing.Iterator[T]:
        return iter(self._value)

    @typing.overload
    def __getitem__(self, item: int) -> T:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> "_ArrayBase[T]":
        ...

    def __getitem__(self, item):  # type: ignore
        if isinstance(item, int):
            return self._value[self._range.index(item)]
        elif isinstance(item, slice):
            if item.start is None:
                start = self.left
            else:
                start = item.start
            if item.stop is None:
                stop = self.right
            else:
                stop = item.stop
            if item.step is not None:
                raise ValueError("do not specify a step")
            start_idx = self._range.index(start)
            stop_idx = self._range.index(stop)
            slc = self._value[start_idx : stop_idx + 1]
            rng = Range(start, self.direction, stop)
            return type(self)(value=slc, range=rng)
        else:
            raise TypeError(
                f"array indices must be ints or slices, not {type(item).__qualname__}"
            )

    @typing.overload
    def __setitem__(self, item: int, value: typing.Any) -> None:
        ...

    @typing.overload
    def __setitem__(self, item: slice, value: typing.Iterable[typing.Any]) -> None:
        ...

    def __setitem__(self, item, value):  # type: ignore
        construct = type(self)._constructor
        if isinstance(item, int):
            self._value[self._range.index(item)] = construct(value)
        elif isinstance(item, slice):
            if item.start is None:
                start = self.left
            else:
                start = item.start
            if item.stop is None:
                stop = self.right
            else:
                stop = item.stop
            if item.step is not None:
                raise ValueError("do not specify a step")
            start_idx = self._range.index(start)
            stop_idx = self._range.index(stop)
            rng = Range(start, self.direction, stop)
            value = [construct(v) for v in value]
            if len(value) != len(rng):
                raise ValueError("value does not fit in given bounds")
            self._value[start_idx : stop_idx + 1] = value
        else:
            raise TypeError(
                f"array indices must be ints or slices, not {type(item).__qualname__}"
            )


class Array(_ArrayBase[typing.Any]):
    __slots__ = ("_value", "_range")

    @staticmethod
    def _constructor(value: typing.Any) -> typing.Any:
        return value
