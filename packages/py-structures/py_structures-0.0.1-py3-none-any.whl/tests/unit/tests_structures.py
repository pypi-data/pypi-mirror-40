# Basic testing
from structures import structure


def test_basic_structures():
    foo = structure(a=1, b=2, c=3, d=4)
    assert foo.a == 1
    assert foo.b == 2
    assert foo.c == 3
    assert foo.d == 4
    assert foo.__slots__ is not None

def test_structures_update():
    foo = structure(a=1, b=2, c=3, d=4)

    foo.a = 4
    foo.b = 3
    foo.c = 2
    foo.d = 1

    assert foo.a == 4
    assert foo.b == 3
    assert foo.c == 2
    assert foo.d == 1


def test_different_strucs_dont_conflict():
    foo = structure(a=1, b=2)
    bar = structure(c=3, d=4, a=3)

    assert foo.a == 1
    assert foo.b == 2
    assert bar.c == 3
    assert bar.d == 4
    assert bar.a == 3

    foo.a = bar.a
    bar.a = 100

    assert foo.a == 3
    assert bar.a == 100
