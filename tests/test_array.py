from bv2 import Array
import pytest
from itertools import zip_longest


def test_array_construction():
    Array(-3, 4)
    Array(4, -3)
    Array(0, 3, value="test")
    Array(7, 4, value=range(4))
    Array(1, 4, value=[True, 0, "wew", object()])
    with pytest.raises(ValueError):
        Array(0, 1, value="too long")
    with pytest.raises(ValueError):
        Array(7, -7, value="too short")


def test_array_attributes():
    a = Array(-3, 4)
    b = Array(7, 2)

    assert a.left == -3
    assert a.right == 4
    assert a.ascending is True
    assert a.length == 8
    assert len(a) == 8
    assert b.left == 7
    assert b.right == 2
    assert b.ascending is False
    assert b.length == 6
    assert len(b) == 6


def test_array_indexing():
    a = Array(-3, 4)
    b = Array(7, 2)

    assert a[-3] is None
    a[-1] = 7
    assert a[-1] == 7
    with pytest.raises(IndexError):
        a[9]

    assert b[4] is None
    b[5] = 'test'
    assert b[5] == 'test'
    with pytest.raises(IndexError):
        b[9]

    with pytest.raises(TypeError):
        a['1']
    with pytest.raises(TypeError):
        a[object()] = 8


def iter_equals(a, b):
    nil = object()
    return all(a_ == b_ for a_, b_ in zip_longest(a, b, fillvalue=nil))


def test_array_iterators():
    a_init = "testing1"
    b_init = "test12"
    a = Array(-4, 3, value=a_init)
    b = Array(7, 2, value=b_init)
    assert iter_equals(a.indexes(), range(-4, 4))
    assert iter_equals(a.values(), a_init)
    assert iter_equals(iter(a), a_init)
    assert iter_equals(reversed(a), reversed(a_init))

    assert iter_equals(b.indexes(), range(7, 1, -1))
    assert iter_equals(b.values(), b_init)
    assert iter_equals(iter(b), b_init)
    assert iter_equals(reversed(b), reversed(b_init))


def test_array_slicing():
    a = Array(-4, 3)
    b = Array(7, 2)

    a[0:3] = "test"
    assert iter_equals(a[0:3], "test")
    with pytest.raises(IndexError):
        a[-5:0]
    assert iter_equals(a[:], a[:])
    expected = reversed(a.values())
    a[:] = tuple(reversed(a))
    assert iter_equals(a, expected)

    b[4:2] = "lol"
    assert iter_equals(b[4:2], "lol")
    with pytest.raises(IndexError):
        b[2:0]
    assert iter_equals(b[:], b[:])
    expected = reversed(b.values())
    b[:] = tuple(reversed(b))
    assert iter_equals(b, expected)

    # don't specify step
    with pytest.raises(IndexError):
        a[::-1]
    with pytest.raises(IndexError):
        a[::4] = 7

    # incorrect length set
    with pytest.raises(ValueError):
        a[:] = []

    # mismatched ascendency
    with pytest.raises(IndexError):
        b[2:4]
    with pytest.raises(IndexError):
        b[2:4] = "lol"


def test_array_equality():
    assert Array(0, 3, value="test") == Array(0, -3, value="test")
    assert Array(0, 3, value="test") != Array(0, -3, value="lol1")
    assert Array(0, 3, value="test") != Array(0, -4, value="test1")
    assert Array(0, 0) != [0]
    assert Array(0, 3, value="test") == "test"


def test_repr():
    a = Array(0, 3, value="test")
    assert eval(repr(a)) == a
