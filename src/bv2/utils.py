from weakref import WeakValueDictionary


def weak_cache(func):

    cache = WeakValueDictionary()
    cache_get = cache.get
    sentinel = object()

    def helper(*args, **kwargs):
        key = args
        if kwargs:
            key += tuple(kwargs.items())
        res = cache_get(key, sentinel)
        if res is not sentinel:
            return res
        res = func(*args, **kwargs)
        cache[key] = res
        return res

    return helper
