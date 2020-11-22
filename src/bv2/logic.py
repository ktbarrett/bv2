from typing import Optional
from functools import lru_cache


class Logic:

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

    @lru_cache
    def __new__(cls, value: Optional = None):
        self = object.__new__(cls)
        if isinstance(value, Logic):
            self._repr = value._repr
        else:
            try:
                self._repr = cls._repr_map[value]
            except KeyError:
                raise ValueError("{!r} is not a {} literal".format(value, type(self).__qualname__)) from None
        return self

    @lru_cache
    def __and__(self, other):
        if not isinstance(other, Logic):
            try:
                other = Logic(other)
            except ValueError:
                return NotImplemented
        return Logic((
            ('0', '0', '0', '0'),
            ('0', '1', 'X', 'X'),
            ('0', 'X', 'X', 'X'),
            ('0', 'X', 'X', 'X'))[self._repr][other._repr])

    @lru_cache
    def __rand__(self, other):
        return self & other

    @lru_cache
    def __or__(self, other):
        if not isinstance(other, Logic):
            try:
                other = Logic(other)
            except ValueError:
                return NotImplemented
        return Logic((
            ('0', '1', 'X', 'X'),
            ('1', '1', '1', '1'),
            ('X', '1', 'X', 'X'),
            ('X', '1', 'X', 'X'))[self._repr][other._repr])

    @lru_cache
    def __ror__(self, other):
        return self | other

    @lru_cache
    def __xor__(self, other):
        if not isinstance(other, Logic):
            try:
                other = Logic(other)
            except ValueError:
                return NotImplemented
        return Logic((
            ('0', '1', 'X', 'X'),
            ('1', '0', 'X', 'X'),
            ('X', 'X', 'X', 'X'),
            ('X', 'X', 'X', 'X'))[self._repr][other._repr])

    @lru_cache
    def __rxor__(self, other):
        return self ^ other

    @lru_cache
    def __invert__(self):
        return Logic(('1', '0', 'X', 'X')[self._repr])

    @lru_cache
    def __eq__(self, other):
        if not isinstance(other, Logic):
            try:
                other = Logic(other)
            except ValueError:
                return NotImplemented
        return self._repr == other._repr

    @lru_cache
    def __repr__(self):
        return "{}({!r})".format(type(self).__qualname__, str(self))

    @lru_cache
    def __str__(self):
        return ('0', '1', 'X', 'Z')[self._repr]

    @lru_cache
    def __bool__(self):
        if self._repr < 2:
            return bool(self._repr)
        raise ValueError()

    @lru_cache
    def __int__(self):
        if self._repr < 2:
            return self._repr
        raise ValueError()

    __hash__ = object.__hash__
