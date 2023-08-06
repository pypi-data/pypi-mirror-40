"""Define operator applied lazy expr handler"""
from typing import Any, Callable, Tuple, TypeVar
import operator
from dataclasses import dataclass
from .actions import LazyAction
from .util import (FORWARD_OPERATORS, REVERSE_OPERATORS, OPERATORS,
                   copy_, evaluate, getattr_, setattr_)
from .lazy import Lazy

_Lazy = TypeVar('_Lazy', bound=Lazy)


@dataclass
class Operator(LazyAction):
    """Operator applied expression"""
    __slots__ = ['operator', 'operands']

    operator: str
    operands: Tuple[Any, ...]

    def __repr__(self) -> str:
        ops = FORWARD_OPERATORS[self.operator]
        if len(self.operands) == 1:
            return ops + repr(self.operands[0])
        if ops.endswith('()') or len(self.operands) > 2:
            opr = ops[:-2] if ops.endswith('()') else ops
            return opr + '(' + ', '.join(repr(operand)
                                         for operand in self.operands) + ')'
        return ' '.join((repr(self.operands[0]),
                         ops,
                         repr(self.operands[1])))

    def evaluate(self, **kwargs: Any) -> Any:
        return getattr(operator, self.operator)(
            *(evaluate(operand, **kwargs) for operand in self.operands))


def _generate_operator_method(name: str) -> Callable[..., Any]:
    name_ = name + ""
    if name_ in REVERSE_OPERATORS:
        name_ = REVERSE_OPERATORS[name_]

        def operation(self: _Lazy, *args: Any) -> _Lazy:
            new = copy_(self)
            syms = getattr_(new, '__symbols__').union({
                sym
                for arg in args if isinstance(arg, Lazy)
                for sym in getattr_(arg, '__symbols__')
            })
            setattr_(new, '__symbols__', syms)
            setattr_(new, '__action__', Operator(name_, (args[0], self)))
            return new
    elif name_ in FORWARD_OPERATORS:
        def operation(self: _Lazy, *args: Any) -> _Lazy:
            new = copy_(self)
            syms = getattr_(new, '__symbols__').union({
                sym
                for arg in args if isinstance(arg, Lazy)
                for sym in getattr_(arg, '__symbols__')
            })
            setattr_(new, '__symbols__', syms)
            setattr_(new, '__action__', Operator(name_, (self,) + args))
            return new
    else:
        raise ValueError(f"{name} is not an operator dunder method")

    operation.__name__ = name
    return operation

for _opr in OPERATORS:
    setattr(Lazy, _opr, _generate_operator_method(_opr))
