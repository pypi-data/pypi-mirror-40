"""Define some useful functions"""
from typing import Any, Optional, Set, TypeVar, cast
from copy import copy
from ._actions import LazyAction

_T = TypeVar('_T')

# pylint: disable=invalid-name
getattr_ = object.__getattribute__
setattr_ = object.__setattr__
# pylint: enable=invalid-name


def copy_(obj: _T) -> _T:
    """Copy object with `__slots__`"""
    new: _T = object.__new__(type(obj))
    slots = {
        slot
        for typ in type(obj).mro() if hasattr(typ, '__slots__')
        for slot in typ.__slots__
    }
    for slot in slots:
        setattr_(new, slot, copy(getattr_(obj, slot)))
    return new


def _get_action(obj: Any) -> Optional[LazyAction]:
    if hasattr(obj, '__action__'):
        action = getattr_(obj, '__action__')
        if isinstance(action, LazyAction):
            return action
    return None


def evaluate(obj: _T, **kwargs: Any) -> _T:
    """Evaluate expression

    To substitute actual value for specific symbol, give value with keyword argument.
    """
    action = _get_action(obj)
    if action:
        ret = action.evaluate(**kwargs)
        if _get_action(ret):
            symbols = getattr_(ret, '__symbols__').difference(set(kwargs))
            setattr_(ret, '__symbols__', symbols)

        return cast(_T, ret)
    return obj


def update(obj: _T, val: _T, **kwargs: Any) -> None:
    """Update the value of expression

    To substitute actual value for specific symbol, give value with keyword argument.

    Given val must not have any symbol not resolved.
    """

    val_act = _get_action(val)
    if val_act:
        symbols: Set[str] = getattr_(val, '__symbols__')
        if any(sym not in kwargs for sym in symbols):
            raise TypeError("Symbol(s) {} is/are not substituted".format(
                ', '.join(sym for sym in symbols if sym not in kwargs)))
        val = evaluate(val, **kwargs)

    action = _get_action(obj)
    if action:
        action.update(val, **kwargs)
    else:
        raise AttributeError("Read only expression")


FORWARD_OPERATORS = {
    '__lt__': '<',
    '__le__': '<=',
    '__eq__': '==',
    '__ne__': '!=',
    '__gt__': '>',
    '__ge__': '>=',
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__matmul__': '@',
    '__truediv__': '/',
    '__floordiv__': '//',
    '__mod__': '%',
    '__divmod__': 'divmod()',
    '__pow__': '**',
    '__lshift__': '<<',
    '__rshift__': '>>',
    '__and__': '&',
    '__xor__': '^',
    '__or__': '|',
    '__neg__': '-',
    '__pos__': '+',
    '__abs__': 'abs()',
    '__invert__': '~',
}

REVERSE_OPERATORS = {
    '__radd__': '__add__',
    '__rsub__': '__sub__',
    '__rmul__': '__mul__',
    '__rmatmul__': '__matmul__',
    '__rtruediv__': '__truediv__',
    '__rfloordiv__': '__floordiv__',
    '__rmod__': '__mod__',
    '__rdivmod__': '__divmod__',
    '__rpow__': '__pow__',
    '__rlshift__': '__lshift__',
    '__rrshift__': '__rshift__',
    '__rand__': '__and__',
    '__rxor__': '__xor__',
    '__ror__': '__or__',
}

OPERATORS = set(FORWARD_OPERATORS).union(set(REVERSE_OPERATORS))
