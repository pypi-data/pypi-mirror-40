"""Lazy expression generator"""
from typing import Any, Optional, Set, TypeVar, cast
from functools import wraps
import operator
from ._lazy import Lazy as Lazy_
from .actions import Attr, Item, Call
from .util import OPERATORS, copy_, getattr_, setattr_


_Lazy = TypeVar('_Lazy', bound='Lazy')
_T = TypeVar('_T')


class Lazy(Lazy_):
    """Lazy expression generator

    This class is entrypoint of lazy expression

    >>> a = Lazy('a')
    >>> a
    a
    >>> a + 1
    a + 1
    >>> a + 2 * 3
    a + 6
    >>> a.b
    a.b
    >>> a(a, 1 + 2, b=3)
    a(a, 3, b=3)
    """

    def __getattribute__(self: _Lazy, name: str) -> _Lazy:
        if name.startswith('__') and name.endswith(
                '__') and name not in OPERATORS:
            return getattr_(self, name)  # type: ignore

        new = copy_(self)
        act = getattr_(new, '__action__')
        if isinstance(act, Attr):
            setattr_(
                new,
                '__action__',
                Attr(
                    act.target,
                    act.attr +
                    '.' +
                    name))
        else:
            setattr_(new, '__action__', Attr(self, name))
        setattr_(new, '__name__', '')

        if hasattr(new, '__clone__'):
            getattr_(new, '__clone__')()

        return new

    def __getitem__(self: _Lazy, idx: Any) -> _Lazy:
        new = copy_(self)
        if isinstance(idx, Lazy):
            syms = getattr_(
                self, '__symbols__').union(
                    getattr_(
                        idx, '__symbols__'))
            setattr_(new, '__symbols__', syms)
        setattr_(new, '__action__', Item(self, idx))
        setattr_(new, '__name__', '')

        if hasattr(new, '__clone__'):
            getattr_(new, '__clone__')()

        return new

    def __call__(self: _Lazy, *args: Any, **kwargs: Any) -> _Lazy:
        new = copy_(self)
        syms = getattr_(new, '__symbols__')
        syms.union({
            sym
            for arglist in (args, kwargs.values())
            for arg in arglist if isinstance(arg, Lazy)
            for sym in getattr_(arg, '__symbols__')
        })
        setattr_(new, '__symbols__', syms)
        setattr_(new, '__action__', Call(self, args, kwargs))
        setattr_(new, '__name__', '')

        if hasattr(new, '__clone__'):
            getattr_(new, '__clone__')()

        return new

    def __neg__(self, *args: Any, **kwargs: Any) -> Any:
        """Placeholder for unary operator warning"""

    def __pos__(self, *args: Any, **kwargs: Any) -> Any:
        """Placeholder for unary operator warning"""

    def __abs__(self, *args: Any, **kwargs: Any) -> Any:
        """Placeholder for unary operator warning"""

    def __invert__(self, *args: Any, **kwargs: Any) -> Any:
        """Placeholder for unary operator warning"""


def lazy_function(func: _T) -> _T:
    """Decorator that makes function able to handle lazy expr"""

    if callable(func):
        func_ = func

        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            symbols_ = {
                sym
                for arglist in (args, kwargs.values())
                for arg in arglist if isinstance(arg, Lazy)
                for sym in getattr_(arg, '__symbols__')
            }
            if symbols_:
                lazy = Lazy('@')
                setattr_(lazy, '__symbols__', symbols_)
                setattr_(lazy, '__name__', '')
                setattr_(lazy, '__action__', Call(func_, args, kwargs))
                return lazy
            return func_(*args, **kwargs)
        return cast(_T, wrapped)
    raise TypeError("lazy_function must be applied to callable")

# pylint: disable=invalid-name
lazy_getitem = lazy_function(operator.getitem)
lazy_setitem = lazy_function(operator.setitem)
# pylint: enable=invalid-name

def symbol(name: str) -> Any:
    """Create lazy-evaluatable symbol"""
    return cast(Any, Lazy(name))

def symbols(obj: Any) -> Optional[Set[str]]:
    """Return symbols not resolved.

    If given object is not a lazy expr, returns None.
    """
    if isinstance(obj, Lazy):
        return cast(Set[str], getattr_(obj, '__symbols__'))
    return None
