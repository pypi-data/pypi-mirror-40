# An implementation of C-style, mutable structs that should have
# (in theory) relatively good performance.

def __struct(**kwargs):
    class Inner(object):
        __slots__ = kwargs.keys()

    struc = Inner()

    for k, v in kwargs.items():
        setattr(struc, k, v)

    return struc


def structure(**kwargs):
    """Creates a struct given some keyword arguments."""
    struc = __struct(**kwargs)
    return struc
