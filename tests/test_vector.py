from bv2 import Vector
import pytest


def test_():

    IntVector = Vector[int]
    assert issubclass(IntVector, Vector)

    V1 = IntVector[0:7]  # ascending
    assert issubclass(V1, Vector)
    assert issubclass(V1, IntVector)

    v1 = V1()
    assert v1.left == 0
    assert v1.right == 7
    assert v1.ascending
    assert v1.length == 8

    V2 = IntVector[3:-4:-1]  # descending
    assert issubclass(V2, Vector)
    assert issubclass(V2, IntVector)

    v2 = V2()
    assert v2.left == 3
    assert v2.right == -4
    assert not v2.ascending
    assert v2.length == 8

    assert not issubclass(V2, V1)
    assert not issubclass(V1, V2)
