"""Define LazyAction interface"""
from typing import Any, List


class LazyAction:  # pylint: disable=too-few-public-methods
    """Lazy Expression Handler"""
    __slots__: List[str] = []

    def evaluate(self, **kwargs: Any) -> Any:
        """Evaluate expression

        To substitute actual value for specific symbol, give value with keyword argument.
        """
        raise NotImplementedError

    def update(self, val: Any, **kwargs: Any) -> None:  # pylint: disable=no-self-use
        """Update value of expression

        If the expression is readonly, it raises AttributeError
        """
        raise AttributeError("expr cannot be updated")
