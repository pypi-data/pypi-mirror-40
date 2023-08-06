# Basic testing
import pytest
from structures import structure, Struct


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


def test_inner_class_doesnt_persist():
    foo = structure(a=1, b=2)
    bar = structure(c=3, d=4)

    with pytest.raises(AttributeError):
        foo.c

    with pytest.raises(AttributeError):
        foo.d

    with pytest.raises(AttributeError):
        bar.a

    with pytest.raises(AttributeError):
        bar.b


def test_struct_init_and_apply():
    foo = Struct("a", "b", "c")
    bar = foo()

    assert bar.a is None
    assert bar.b is None
    assert bar.c is None

    bar.apply(a=100, b=250, c=1024)

    assert bar.a == 100
    assert bar.b == 250
    assert bar.c == 1024


def test_struct_kwargs():
    foo = Struct(a=1, b=2, c=3)
    bar = foo()

    assert bar.a == 1
    assert bar.b == 2
    assert bar.c == 3


def test_struct_can_handle_uninitialized_and_initialized_attribs():
    foo = Struct("a", "b", "c", health=100, stamina=100, magic=100)
    bar = foo()

    assert bar.a is None
    assert bar.b is None
    assert bar.c is None
    assert bar.health == 100
    assert bar.stamina == 100
    assert bar.magic == 100


def test_structs_are_mutable():
    foo = Struct("a", "b", "c", health=100, stamina=100, magic=100)
    bar = foo()
    bar.apply(a=100, b=10, health=200, magic=0)

    assert bar.a == 100
    assert bar.b == 10
    assert bar.c is None
    assert bar.health == 200
    assert bar.stamina == 100
    assert bar.magic == 0


def test_different_structs_dont_conflict():
    foo = Struct("a", "b", "c")
    bar = foo(a=1, b=2, c=3)
    baz = foo(a=100, b=200, c=300)

    assert bar.a == 1
    assert bar.b == 2
    assert bar.c == 3
    assert baz.a == 100
    assert baz.b == 200
    assert baz.c == 300
