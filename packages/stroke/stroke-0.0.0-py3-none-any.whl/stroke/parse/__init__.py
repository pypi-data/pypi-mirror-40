import functools

from . import abstract


__all__ = ('clause', 'flag', 'group', 'split')


escape = '\\'


start = '('


stop = ')'


def seek(values, escape = escape, start = start, stop = stop):

    return abstract.seek(escape, start, stop, values)


def clause(values, escape = escape, start = start, seek = seek):

    """
    Yield clauses.
    Every second clause is an inner clause.
    """

    yield from abstract.clause(escape, start, seek, values)


def skip(value, escape = escape):

    return value.startswith(escape)


def flag(value, *keys, skip = skip):

    """
    Differenciate values according to keywords.
    """

    return abstract.flag(skip, value, keys)


def group(values, *keys, flag = flag):

    """
    Group key-value pairs by the key.
    """

    initial, *extras = flag(values, *keys)

    junk, initial = initial

    store = {key: [] for key in keys}

    for (key, value) in extras:

        store[key].append(value)

    (keys, values) = zip(*store.items())

    return (initial, *values)


def split(values, key, group = group):

    """
    Separate and clean flags by the key.
    """

    value, values = group(values, key)

    values.insert(0, value)

    yield from filter(bool, values)
