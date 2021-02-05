from bv2.logic_array import LogicArray
from bv2.logic import Logic
import itertools


def iter_equals(a, b):
    nil = object()
    return all(a_ == b_ for a_, b_ in itertools.zip_longest(a, b, fillvalue=nil))


def test_logic_array():
    l = LogicArray(1, 4, value=[True, '0', Logic('X'), 1])
    assert all(isinstance(v, Logic) for v in l)

    l[2] = 'w'
    assert all(isinstance(v, Logic) for v in l)

    p = LogicArray(1, 4, value="01XZ")
    assert str(p) == "01XZ"


def test_logic_array_bitwise():
    a, b = [], []
    for a_, b_ in itertools.product("01XZ", repeat=2):
        a.append(Logic(a_))
        b.append(Logic(b_))

    l = LogicArray(1, len(a), value=a)
    p = LogicArray(1, len(b), value=b)

    and_ = l & p
    assert and_.left == 1
    assert isinstance(and_, LogicArray)
    assert len(and_) == len(l)

    and_expected = [l_ & p_ for l_, p_ in zip(l, p)]
    assert iter_equals(and_, and_expected)

    or_ = l | p
    or_expected = [l_ | p_ for l_, p_ in zip(l, p)]
    assert iter_equals(or_, or_expected)

    xor_ = l ^ p
    xor_expected = [l_ ^ p_ for l_, p_ in zip(l, p)]
    assert iter_equals(xor_, xor_expected)

    not_ = ~l
    not_expected = [~l_ for l_ in l]
    assert iter_equals(not_, not_expected)

    with pytest.raises(ValueError):
        l ^ LogicArray(0, 0, value=[1])

    with pytest.raises(TypeError):
        l ^ []
