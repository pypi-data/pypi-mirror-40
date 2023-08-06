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
`structures` are superficially similiar to Ruby's `Struct` class.
Attributes can be called as if they were a class.

```python
from structures import *

foo = structure(a=1, b=2, c=3)
foo.a
>>> 1

foo.b
>>> 2

foo.c
>>> 3

# Struct is a factory function.
bar = Struct("health", "stamina", "magic")
baz = bar(health=10, stamina=7.5, magic=5)

baz.health
>>> 10
# ... and so on

```

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

asizeof.asizeof(test_struct)
>>> 96

asizeof.asizeof(test_dict)
>>> 424

asizeof.asizeof(test_class)
>>> 488
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

asizeof.asizeof(test_struct)
>>> 96

asizeof.asizeof(test_dict)
>>> 440

asizeof.asizeof(test_class)
>>> 368
```
