from bv2.utils import cache


class Logic:

    __singleton_cache__ = {}

    _repr_map = {
        # 0 and weak 0
        False: 0,
        0: 0,
        '0': 0,
        'L': 0,
        'l': 0,
        # 1 and weak 1
        True: 1,
        1: 1,
        '1': 1,
        'H': 1,
        'h': 1,
        # unknown, unassigned, and weak unknown
        None: 2,
        'X': 2,
        'x': 2,
        'U': 2,
        'u': 2,
        'W': 2,
        'w': 2,
        # high impedance
        'Z': 3,
        'z': 3}

    @cache
    def __new__(cls, value=None):
        # convert to internal representation
        try:
            _repr = cls._repr_map[value]
        except KeyError:
            raise ValueError("{!r} is not convertable to a {}".format(value, cls.__qualname__)) from None
        # ensure only one object is made per representation
        if _repr not in cls.__singleton_cache__:
            obj = super().__new__(cls)
            obj._repr = _repr
            cls.__singleton_cache__[_repr] = obj
        return cls.__singleton_cache__[_repr]

    @cache
    def __and__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)((
            ('0', '0', '0', '0'),
            ('0', '1', 'X', 'X'),
            ('0', 'X', 'X', 'X'),
            ('0', 'X', 'X', 'X'))[self._repr][other._repr])

    @cache
    def __rand__(self, other):
        return self & other

    @cache
    def __or__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)((
            ('0', '1', 'X', 'X'),
            ('1', '1', '1', '1'),
            ('X', '1', 'X', 'X'),
            ('X', '1', 'X', 'X'))[self._repr][other._repr])

    @cache
    def __ror__(self, other):
        return self | other

    @cache
    def __xor__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return type(self)((
            ('0', '1', 'X', 'X'),
            ('1', '0', 'X', 'X'),
            ('X', 'X', 'X', 'X'),
            ('X', 'X', 'X', 'X'))[self._repr][other._repr])

    @cache
    def __rxor__(self, other):
        return self ^ other

    @cache
    def __invert__(self):
        return type(self)(('1', '0', 'X', 'X')[self._repr])

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    @cache
    def __repr__(self):
        return "{}({!r})".format(type(self).__name__, str(self))

    @cache
    def __str__(self):
        return ('0', '1', 'X', 'Z')[self._repr]

    @cache
    def __bool__(self):
        if self._repr < 2:
            return bool(self._repr)
        raise ValueError("Cannot convert non-0/1 {} to bool".format(type(self).__qualname__))

    @cache
    def __int__(self):
        if self._repr < 2:
            return self._repr
        raise ValueError("Cannot convert non-0/1 {} to int".format(type(self).__qualname__))


class Bit(Logic):

    # must create a separate cache for Bit
    __singleton_cache__ = {}

    _repr_map = {
        # 0
        False: 0,
        0: 0,
        '0': 0,
        # 1
        True: 1,
        1: 1,
        '1': 1}


Logic._repr_map.update({
    Logic('0'): 0,
    Logic('1'): 1,
    Logic('X'): 2,
    Logic('Z'): 3,
    Bit('0'): 0,
    Bit('1'): 1
})

Bit._repr_map.update({
    Logic('0'): 0,
    Logic('1'): 1,
    Bit('0'): 0,
    Bit('1'): 1
})
