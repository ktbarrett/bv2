from typing import Optional


def singleton(*args, **kwargs):
    def helper(f):
        return f(*args, **kwargs)
    return helper


class Logic:

    def __rand__(self, other):
        return self & other

    def __ror__(self, other):
        return self | other

    def __rxor__(self, other):
        return self ^ other

    def __repr__(self):
        return "Logic({!r})".format(str(self))

    def __eq__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        return self is other

    __hash__ = object.__hash__


@singleton()
class _0(Logic):
    __slots__ = ()

    def __and__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        return _0

    def __or__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is X or other is Z:
            return X
        else:
            return other

    def __xor__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is X or other is Z:
            return X
        elif other is _1:
            return _1
        else:
            return _0

    def __invert__(self):
        return _1

    def __str__(self):
        return "0"

    def __bool__(self):
        return False

    def __int__(self):
        return 0


@singleton()
class _1(Logic):
    __slots__ = ()

    def __and__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is X or other is Z:
            return X
        else:
            return other

    def __or__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        return _1

    def __xor__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is X or other is Z:
            return X
        elif other is _0:
            return _1
        else:
            return _0

    def __invert__(self):
        return _0

    def __str__(self):
        return "1"

    def __bool__(self):
        return True

    def __int__(self):
        return 1


@singleton()
class X(Logic):
    __slots__ = ()

    def __and__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is _0:
            return _0
        else:
            return X

    def __or__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        if other is _1:
            return _1
        else:
            return X

    def __xor__(self, other):
        try:
            other = Logic(other)
        except ValueError:
            return NotImplemented
        return X

    def __invert__(self):
        return X

    def __str__(self):
        return "X"

    def __bool__(self):
        raise ValueError("Cannot cast Logic value {!r} to bool".format(str(self)))

    def __int__(self):
        raise ValueError("Cannot cast Logic value {!r} to int".format(str(self)))


@singleton()
class Z(type(X)):
    __slots__ = ()

    def __str__(self):
        return "Z"


_conversions = {
    # 0 and weak 0
    False: _0,
    0: _0,
    '0': _0,
    'L': _0,
    'l': _0,
    _0: _0,
    # 1 and weak 1
    True: _1,
    1: _1,
    '1': _1,
    'H': _1,
    'h': _1,
    _1: _1,
    # unknown, unassigned, and weak unknown
    None: X,
    'X': X,
    'x': X,
    'U': X,
    'u': X,
    'W': X,
    'w': X,
    X: X,
    # high impedance
    'Z': Z,
    'z': Z,
    Z: Z}


def _construct(cls, value: Optional = None):
    try:
        return _conversions[value]
    except KeyError:
        raise ValueError("{!r} is not a {} literal".format(value, cls.__qualname__)) from None


Logic.__new__ = _construct
