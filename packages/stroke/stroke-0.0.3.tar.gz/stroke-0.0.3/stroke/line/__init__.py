
from . import abstract


__all__ = ('sub', 'trail', 'prefix', 'parse', 'context', 'invoke')


def sub(store, *names, cls = None):

    def decorator(call):

        value = (cls or dict)()

        state = (call, value)

        for name in names:

            store[name] = state

        return value

    return decorator


def trail(store, *names):

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

    call = trail(store, *names) if names else None

    return start, names, arguments, call


class Store(dict):

    __slots__ = ()

    def sub(self, *names, use = sub):

        return use(self, *names, cls = self.__class__)

    def trail(self, *names, use = trail):

        return use(self, *names)

    def context(self, starts, value, use = context):

        return use(self, starts, value)
