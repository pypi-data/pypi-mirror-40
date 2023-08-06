# An implementation of C-style, mutable structs that should have
# (in theory) relatively good performance.


def structure(**kwargs):
    """Creates a struct given some keyword arguments.

    Note that all objects created with `structure` will have the same
    class type.

    Example:

        >>> player = structure(health=100, stamina=75, magic=50)
        >>> monster = structure(health=150, stamina=100, magic=0)

    """
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


def Struct(*args, **kwargs):
    """Creates a structure template.

    Can be used in instances where you do not want to initialize your
    struct when it is defined. Similar to a `class` to the innocent,
    hence the capitalized name.

    Example:

        >>> Npc = Struct("health", "stamina", "magic")
        >>> player = Npc(health=100, stamina=75, magic=50)

    """
    def fn(**qwargs):
        z = kwargs
        z.update({arg: None for arg in args})
        struc = structure(**z)
        if qwargs is None:
            return struc
        return struc.apply(**qwargs)

    return fn
