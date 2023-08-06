"""Lazy expression generator"""
from typing import Any
from dataclasses import dataclass
from ._actions import LazyAction
from .util import getattr_, setattr_

@dataclass
class Symbol(LazyAction):
    """Just symbol"""

    __slots__ = ['name', 'lazy']
    name: str
    lazy: 'Lazy'

    def __repr__(self) -> str:
        return self.name

    def evaluate(self, **kwargs: Any) -> Any:
        if self.name in kwargs:
            return kwargs[self.name]
        return self.lazy


class Lazy:  # pylint: disable=too-few-public-methods
    """Internal Lazy Expr Generator base class"""
    __slots__ = ['__name__', '__symbols__', '__action__']

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Name must be specified")
        setattr_(self, '__name__', name)
        setattr_(self, '__symbols__', {name})
        setattr_(self, '__action__', Symbol(name, self))

    def __repr__(self) -> str:
        return repr(getattr_(self, '__action__'))
