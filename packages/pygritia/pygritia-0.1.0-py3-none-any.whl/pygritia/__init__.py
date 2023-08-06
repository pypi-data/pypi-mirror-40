"""Pygritia: Lazy evaluation"""
from .lazy import symbol, lazy_function, lazy_getitem, lazy_setitem, symbols
from .util import evaluate, update
from . import lazyop

__all__ = [
    'symbol', 'symbols', 'lazy_function', 'lazy_getitem', 'lazy_setitem',
    'evaluate', 'update'
]
