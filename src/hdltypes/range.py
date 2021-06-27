import typing

Self = typing.TypeVar("Self")


def _guess_direction(left: int, right: int) -> str:
    return "to" if left <= right else "downto"


def _direction_to_step(direction: str) -> int:
    if direction == "to":
        return 1
    elif direction == "downto":
        return -1
    raise ValueError("Direction must be 'to' or 'downto'")


class Range(typing.Sequence[int]):
    __slots__ = ("_range", "_direction")

    @typing.overload
    def __init__(self, left: int, direction: str, right: int) -> None:
        ...

    @typing.overload
    def __init__(self, left: int, right: int) -> None:
        ...

    def __init__(self, left, direction=None, right=None):  # type: ignore
        if direction is None and right is not None:
            direction = _guess_direction(left, right)
        elif direction is not None and right is None:
            right = direction
            direction = _guess_direction(left, right)
        elif direction is not None and right is not None:
            pass
        else:
            raise TypeError(
                "Range takes a left bound, right bound, and optionally a direction"
            )
        self._direction = direction
        step = _direction_to_step(direction)
        self._range = range(left, right + step, step)

    @classmethod
    def from_range(cls, rng: range) -> "Range":
        if rng.step not in (1, -1):
            raise ValueError("range must have a step of 1 or -1")
        r = Range.__new__(cls)
        r._range = rng
        return r

    def to_range(self) -> range:
        return self._range

    @property
    def left(self) -> int:
        return self._range.start

    @property
    def right(self) -> int:
        return self._range.stop - self._range.step

    @property
    def direction(self) -> str:
        return self._direction

    def __len__(self) -> int:
        return len(self._range)

    @typing.overload
    def __getitem__(self, item: int) -> int:
        ...

    @typing.overload
    def __getitem__(self, item: slice) -> "Range":
        ...

    def __getitem__(self, item):  # type: ignore
        if isinstance(item, int):
            return self._range[item]
        elif isinstance(item, slice):
            return type(self).from_range(self._range[item])
        raise TypeError(
            f"Range indices must be ints or slices, not {type(item).__qualname__}"
        )

    def __eq__(self, other: typing.Any) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return self._range == other._range

    def __hash__(self) -> int:
        return hash(self._range)

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({self.left!r}, {self.direction!r}, {self.right!r})"
