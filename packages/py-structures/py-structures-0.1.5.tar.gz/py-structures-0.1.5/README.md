[![Build Status](https://travis-ci.org/bholten/structures.svg?branch=master)](https://travis-ci.org/bholten/structures)

# structures
Pseudo C-style structs for Python

This instantiates a dummy class and forces and keyword arguments you
pass into the `__slots__` field.

The reason to do this is that `__slots__` attributes are stored more
efficiently, at least in the CPython implementation. There is less (if
any?) benefit to doing this in PyPy.

These are intended to be used as data containers, so the primary
constructor is simply a function called `structure` within the
module. There is also a helper factory function that generates an
uninitialized Struct.

## Usage
Here is an example:

```python
>>> from structures import *
>>> foo = structure(a=1, b=2, c=3)
>>> foo.a
1
>>> foo.b
2
>>> foo.c
3
```

Also note that there is a `Struct` factory function.

```python
>>> Character = Struct("health", "stamina", "magic")
>>> player = Character(health=10, stamina=7.5, magic=5)
>>> player.health
10
```
... and so on.

And here, attributes will be guarenteed to exist (at least as
`__slots__`). Uninitialized attributes will default to `None`.

```python
>>> monster = Character(health=15, stamina=10)
>>> monster.magic is None
True
```

## Limitations
Currently, anything created with `structure` or `Struct` will have the
same class type, namely `Structure` (hence *pseudo* structs).

```python
>>> Character = Struct("health", "stamina", "magic")
>>> player = Character(health=100, stamina=50, magic=25)
>>> type(player)
<class 'structures.structures.Structure'>
```

There may be some effort to improve this later, however I am not
highly bothered by this due to Python's duck typing.

## Install
```bash
pip install py-structures
```

## Examples
Using the `sys` module's `getsizeof` function is generally unreliable,
especially with nested data structures. For these tests, I used the
the excellent [pympler](https://pythonhosted.org/Pympler/) library.

### Python 2.7
Simple integer storage is a little over five times more efficient.

```python
from pympler import asizeof
from structures import structure

class DummyClass(object):
      def __init__(self, a, b, c):
          self.a = a
          self.b = b
          self.c = c

test_struct = structure(a=1024, b=1024, c=1024)
test_dict   = dict(a=1024, b=1024, c=1024)
test_class  = DummyClass(a=1024, b=1024, c=1024)

>>> asizeof.asizeof(test_struct)
96

>>> asizeof.asizeof(test_dict)
424

>>> asizeof.asizeof(test_class)
488
```

### Python 3.6
Python 3.6 reported [optimzations to their dict
implementation](https://docs.python.org/3/whatsnew/3.6.html). This
included a slightly better memory footprint for classes, which are
implemented as dicts behind the scenes. However, the preceeding
example is still about 3.8 times more efficient.

```python
from pympler import asizeof
from structures import structure

class DummyClass(object):
      def __init__(self, a, b, c):
          self.a = a
          self.b = b
          self.c = c

test_struct = structure(a=1024, b=1024, c=1024)
test_dict   = dict(a=1024, b=1024, c=1024)
test_class  = DummyClass(a=1024, b=1024, c=1024)

>>> asizeof.asizeof(test_struct)
96

>>> asizeof.asizeof(test_dict)
440

>>> asizeof.asizeof(test_class)
368
```
