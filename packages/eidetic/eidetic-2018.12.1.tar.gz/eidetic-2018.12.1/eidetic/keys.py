"""Key functions for memoizing decorators."""
from typing import Callable, Type


HASH_CONFIG = {}


def register_hash_function(obj_type: Type, function: Callable):
    """Registers a user defined hash function for a given type"""
    HASH_CONFIG[obj_type] = function


try:
    import numpy as np

    register_hash_function(np.ndarray, lambda x: hash(str(x)))
except ImportError:
    pass


def _hash(obj):
    try:
        return hash(obj)
    except TypeError as exc:
        hasher = HASH_CONFIG.get(type(obj))
        if hasher:
            return hasher(obj)
        raise exc


def hash_params(func, *args, **kwargs):
    if kwargs is None:
        kwargs = {}

    code = func.__code__

    params = [code.co_name, code.co_filename, code.co_code] + list(args) + sorted(kwargs.items())

    hashes = []
    for param in params:
        param_hash = _hash(param)
        hashes.append(param_hash)
    return f'{code.co_name}:{code.co_filename}:{hash(tuple(hashes))}'
