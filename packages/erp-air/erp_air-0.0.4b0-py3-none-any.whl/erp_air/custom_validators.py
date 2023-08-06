"""Costum validators.

Which we use in validating attributes of different
data structures.
"""
def from_zero_to_one(instance, attrib, val):
    if not 0 <= val <= 1:
        raise ValueError()


def from_zero_to_one_or_none(instance, attrib, val):
    if val:
        from_zero_to_one(instance, attrib, val)


def int_or_float(instance, attrib, val):
    if not (
        isinstance(val, float) or isinstance(val, int)
    ):
        raise ValueError()


def int_or_float_or_none(instance, attrib, val):
    if val:
        int_or_float(instance, attrib, val)
