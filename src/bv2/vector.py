from abc import ABCMeta, abstractmethod
from typing import Optional, Iterable, Type, Any, overload
from functools import cached_property
from bv2.utils import weak_cache


class _ElemTypeParametizer(ABCMeta):

    @weak_cache
    def __getitem__(cls, arg: type) -> 'Vector':
        print("Running!")
        name = "{}[{}]".format(cls.__qualname__, arg.__qualname__)
        return _BoundTypeParameterizer(name, (_ElemTypeMixin, cls), {'_ElemType': arg})


class _ElemTypeMixin:
    _ElemType: type

    @property
    def ElemType(self) -> type:
        return self._ElemType

    @cached_property
    def VectorType(self) -> 'Vector':
        return Vector[self._ElemType]


class _BoundTypeParameterizer(_ElemTypeParametizer):

    @weak_cache
    def __getitem__(cls, arg: slice) -> 'Vector':
        left = arg.start if arg.start is not None else 1
        right = arg.stop if arg.stop is not None else 1
        if arg.step is not None:
            if arg.step == 1:
                ascending = True
            elif arg.step == -1:
                ascending = False
            else:
                raise ValueError("Invalid step value. Must be either 1 or -1.")
        else:
            ascending = right >= 1
        ascending_step = 1 if ascending else -1
        name = "{}[{}:{}:{}]".format(cls.__qualname__, left, right, ascending_step)
        return _FinishedParametizer(name, (_BoundsMixin, cls), {
            '_left': left,
            '_right': right,
            '_ascending': ascending})


class _BoundsMixin:
    _left: int
    _right: int
    _ascending: bool

    @property
    def left(self) -> int:
        return self._left

    @property
    def right(self) -> int:
        return self._right

    @property
    def ascending(self) -> bool:
        return self._ascending

    @cached_property
    def length(self) -> int:
        if self.ascending:
            leng = self.right - self.left + 1
        else:
            leng = self.left - self.right + 1
        return max(leng, 0)  # supports VHDL's null arrays


class _FinishedParametizer(_BoundTypeParameterizer):

    def __getitem__(cls, arg: Any) -> None:
        raise TypeError("'{}' is not subscriptable".format(cls.__qualname__))


class Vector(metaclass=_ElemTypeParametizer):

    def __init__(self, value: Optional[Iterable] = None):
        if value is None:
            self._value = [self.ElemType() for _ in range(self.length)]
        else:
            self._value = [self.ElemType(v) for v in value]
            if len(self._value) == self.length:
                raise ValueError("Initial value does not fit bounds")

    @property
    @abstractmethod
    def ElemType(self) -> type:
        """ Returns the element type """

    @property
    def VectorType(self) -> Type['Vector']:
        """ Returns the unbound version of this vector type """

    @property
    @abstractmethod
    def left(self) -> int:
        """ Returns the left bound of the vector """

    @property
    @abstractmethod
    def right(self) -> int:
        """ Returns the right bound of the vector """

    @property
    @abstractmethod
    def ascending(self) -> bool:
        """ Returns ``True`` if the bounds are ascending, ``False`` otherwise """

    @property
    @abstractmethod
    def length(self) -> int:
        """ Returns the number of elements the vector can store """

    def __len__(self):
        return self.length

    def __iter__(self):
        yield from self._value

    def __eq__(self, other: Iterable):
        if not isinstance(other, self.VectorType):
            # ensure 'other' is an iterable of the ElemType
            other = type(self)(other)
        if len(other) != len(self):
            raise ValueError()
        return all(a == b for a, b in zip(self, other))

    def _index(self, index: int) -> int:
        if self.ascending:
            ret = index - self.left
        else:
            ret = self.left - index
        if ret < 0 or self.length <= ret:
            raise IndexError()
        return ret

    @overload
    def __getitem__(self, item: int) -> Any:
        pass  # pragma: no cover

    @overload
    def __getitem__(self, item: slice) -> 'Vector':
        pass  # pragma: no cover

    def __getitem__(self, item):
        if isinstance(item, int):
            index = self._index(item)
            return self._value[index]

        elif isinstance(item, slice):
            start = item.start if item.start is not None else self.left
            stop = item.stop if item.stop is not None else self.right
            if item.step is not None:
                if (self.ascending and item.step != 1) or (not self.ascending and item.step != 1):
                    raise IndexError()
            start_index = self._index(start)
            stop_index = self._index(stop)
            sliced = self._value[start_index:stop_index]
            return self.VectorType[start:stop:self.ascending](sliced)

        else:
            raise TypeError()

    @overload
    def __setitem__(self, item: int, value: Any) -> None:
        pass  # pragma: no cover

    @overload
    def __setitem__(self, item: slice, value: Iterable) -> None:
        pass  # pragma: no cover

    def __setitem__(self, item, value):
        if isinstance(item, int):
            index = self._index(item)
            self._value[index] = self.ElemType(value)

        elif isinstance(item, slice):
            start = item.start if item.start is not None else self.left
            stop = item.stop if item.stop is not None else self.right
            if item.step is not None:
                if (self.ascending and item.step != 1) or (not self.ascending and item.step != 1):
                    raise IndexError()
            start_index = self._index(start)
            stop_index = self._index(stop)
            new_value = [self.ElemType(v) for v in value]
            self._value[start_index:stop_index] = new_value

        else:
            raise TypeError()

    def __repr__(self):
        return '{}({})'.format(type(self).__qualname__, repr(self._value))
