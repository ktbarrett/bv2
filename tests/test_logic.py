import pytest
from bv2 import Logic


def test_constructors():
    _ = Logic(0)
    _ = Logic(1)
    _ = Logic(True)
    _ = Logic(False)
    _ = Logic('0')
    _ = Logic('1')
    _ = Logic('X')
    _ = Logic('Z')
    with pytest.raises(ValueError):
        Logic('j')
    _ = Logic(Logic(0))
    Logic()


def test_comparison():
    assert Logic(0) == Logic('0')
    assert Logic(0) != Logic('X')
    assert Logic(0) != object()


def test_bool_conversions():
    assert bool(Logic('1')) is True
    assert bool(Logic('0')) is False
    with pytest.raises(ValueError):
        bool(Logic('X'))
    with pytest.raises(ValueError):
        bool(Logic('Z'))


def test_str_conversions():
    assert str(Logic('0')) == '0'
    assert str(Logic('1')) == '1'
    assert str(Logic('X')) == 'X'
    assert str(Logic('Z')) == 'Z'


def test_int_conversions():
    assert int(Logic('0')) == 0
    assert int(Logic('1')) == 1
    with pytest.raises(ValueError):
        int(Logic('X'))
    with pytest.raises(ValueError):
        int(Logic('Z'))


def test_repr():
    assert eval(repr(Logic('0'))) == Logic('0')
    assert eval(repr(Logic('1'))) == Logic('1')
    assert eval(repr(Logic('X'))) == Logic('X')
    assert eval(repr(Logic('Z'))) == Logic('Z')


def test_and():
    assert Logic('0') & Logic('Z') == Logic(0)
    assert Logic(1) & Logic('1') == Logic(1)
    assert Logic('X') & Logic('Z') == Logic('X')
    with pytest.raises(TypeError):
        Logic('1') & 8
    with pytest.raises(TypeError):
        8 & Logic('1')


def test_or():
    assert Logic('1') | Logic('Z') == Logic('1')
    assert Logic(0) | Logic('0') == Logic(0)
    assert Logic('X') | Logic('Z') == Logic('X')
    with pytest.raises(TypeError):
        8 | Logic(0)
    with pytest.raises(TypeError):
        Logic(0) | 8


def test_xor():
    assert (Logic('1') ^ Logic(True)) == Logic(0)
    assert (Logic(1) ^ Logic('X')) == Logic('X')
    assert (Logic(1) ^ Logic(False)) == Logic(1)
    with pytest.raises(TypeError):
        Logic(1) ^ ()
    with pytest.raises(TypeError):
        () ^ Logic(1)


def test_invert():
    assert ~Logic(0) == Logic(1)
    assert ~Logic('Z') == Logic('X')
