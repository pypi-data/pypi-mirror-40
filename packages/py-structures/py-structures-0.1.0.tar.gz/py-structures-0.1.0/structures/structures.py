# An implementation of C-style, mutable structs that should have
# (in theory) relatively good performance.


def _struct(**kwargs):
    class Structure(object):
        __slots__ = list(kwargs.keys())

        def __repr__(self):
            attribs = []
            for k in self.__slots__:
                try:
                    attribs.append("{}={}".format(k, self.__getattribute__(k)))
                except AttributeError:
                    attribs.append("{}=Undefined".format(k))
            return "Struct Attributes: {}".format(", ".join(attribs))

        def apply(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
            return self

    struc = Structure()

    for k, v in kwargs.items():
        setattr(struc, k, v)

    return struc


def structure(**kwargs):
    """Creates a struct given some keyword arguments."""
    struc = _struct(**kwargs)
    return struc

def Struct(*args, **kwargs):
    """Creates an uninitialized structure.

    Can be used in instances where you do not want to initialize your
    struct when it is defined.  like a 'class' to the innocent, hence
    the capitalized name.

    Example:

        >>> foo = Struct("health", "stamina", "magic")
        >>> foo.apply(health=100, stamina=100, magic=50)

    """
    def fn(**qwargs):
        z = kwargs
        z.update({arg: None for arg in args})
        struc = structure(**z)
        if qwargs is None:
            return struc
        else:
            return struc.apply(**qwargs)

    return fn