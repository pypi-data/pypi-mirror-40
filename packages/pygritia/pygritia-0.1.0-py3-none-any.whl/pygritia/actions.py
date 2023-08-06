"""Define basic lazy expression handlers"""
from typing import Any, Mapping, Tuple, TypeVar
from dataclasses import dataclass
import operator
from ._actions import LazyAction
from ._lazy import Lazy
from .util import evaluate

_T = TypeVar('_T')


@dataclass
class Attr(LazyAction):
    """Attr accessor"""

    __slots__ = ['target', 'attr']
    target: Lazy
    attr: str

    def __repr__(self) -> str:
        return repr(self.target) + '.' + self.attr

    def evaluate(self, **kwargs: Any) -> Any:
        return operator.attrgetter(self.attr)(evaluate(self.target, **kwargs))

    def update(self, val: Any, **kwargs: Any) -> None:
        if '.' in self.attr:
            prior, attr = self.attr.rsplit('.', 1)
            obj = operator.attrgetter(prior)(evaluate(self.target, **kwargs))
        else:
            attr = self.attr
            obj = evaluate(self.target, **kwargs)
        setattr(obj, attr, evaluate(val, **kwargs))


@dataclass
class Item(LazyAction):
    """Item accessor"""
    __slots__ = ['target', 'index']

    target: Any
    index: Any

    def __repr__(self) -> str:
        return repr(self.target) + '[' + repr(self.index) + ']'

    def evaluate(self, **kwargs: Any) -> Any:
        return evaluate(self.target, **kwargs)[evaluate(self.index, **kwargs)]

    def update(self, val: Any, **kwargs: Any) -> None:
        obj = evaluate(self.target, **kwargs)
        index = evaluate(self.index, **kwargs)
        value = evaluate(val, **kwargs)
        obj[index] = value


@dataclass
class Call(LazyAction):
    """Function call"""
    __slots__ = ['target', 'args', 'kwargs']

    target: Any
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __repr__(self) -> str:
        if isinstance(self.target, Lazy):
            name = repr(self.target)
        elif hasattr(self.target, '__name__'):
            name = self.target.__name__
        else:
            name = str(self.target)
        return (name + '(' +
                ', '.join(
                    item
                    for items in (
                        (repr(arg) for arg in self.args),
                        (key + '=' + repr(value) for key, value in self.kwargs.items())
                    )
                    for item in items
                ) + ')')

    def evaluate(self, **kwargs: Any) -> Any:
        callable_ = evaluate(self.target, **kwargs)
        args_ = (evaluate(arg, **kwargs) for arg in self.args)
        kwargs_ = {key: evaluate(value, **kwargs) for key, value in self.kwargs.items()}
        return callable_(*args_, **kwargs_)
