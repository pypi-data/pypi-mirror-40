import functools
import collections

from . import abstract


__all__ = ('sub', 'trail', 'prefix', 'parse', 'context', 'invoke')


State = collections.namedtuple('State', ('call', 'store'))


def sub(store, *names):

    def decorator(call):

        value = State(call, {})

        for name in names:

            store[name] = value

        return value

    return decorator


def trail(store, names):

    return abstract.trail(store, names)


def prefix(values, content):

    for value in values:

        if content.startswith(value):

            break

    else:

        raise ValueError()

    content = content[len(value):]

    return value, content


lower = '.'


middle = ' '


upper = ' '


def parse(content, lower = lower, middle = middle, upper = upper):

    return abstract.parse(content, lower, middle, upper)


def context(store, starts, content, prefix = prefix, parse = parse):

    start, content = prefix(starts, content)

    names, arguments = parse(content)

    call = trail(store, names) if names else None

    return start, names, arguments, call
