import sys as _sys

if _sys.version_info < (3, 8):
    from functools import cache
else:
    from functools import lru_cache

    def cache(f):
        return lru_cache(maxsize=None)(f)
