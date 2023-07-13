import contextlib
import shelve

from .constants import CACHE_FILE_NAME


class ShelveCache:
    def __init__(self, cache_file_name: str) -> None:
        self._cache_file_name = cache_file_name

    @contextlib.contextmanager
    def session(self):
        with shelve.open(CACHE_FILE_NAME) as persistent_dictionary:
            yield persistent_dictionary

    def wrap_callable(self, key, source_callback):
        with self.session() as persistent_dictionary:
            if key not in persistent_dictionary:
                persistent_dictionary[key] = source_callback()
            return persistent_dictionary[key]


def shelve_it(func):
    cache = ShelveCache(CACHE_FILE_NAME)

    def new_func(*args, **kwargs):
        return cache.wrap_callable(func.__name__, lambda: func(*args, **kwargs))

    return new_func
