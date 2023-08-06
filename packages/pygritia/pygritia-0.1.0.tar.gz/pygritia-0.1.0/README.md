# Pygritia

Pygritia is a symbolic expression library.

It can

* create symbolic expressions with one or more symbols
* resolve symbolic expressions by substituting values to symbols
* partially resolve symbolic expression

Example:

```python
from pygritia import symbol, evaluate, update

this = symbol('this')
that = symbol('that')
arr = [1, 2, 3]
print(5 / this + 2 * 6)  # 5 / this + 12
print(evaluate(5 / this + 2 * 6, this=2))  # 14.5
print(evaluate(this[that], this=arr)) # [1, 2, 3][that]
update(this[that], 42, this=arr, that=1)
print(arr)  # [1, 42, 3]
```

Documentation of all public functions can be found in [`pygritia`][pygritia]

[pygritia]: https://gwangyi.github.io/pygritia/

