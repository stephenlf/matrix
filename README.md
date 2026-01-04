# Matrix

A super simple Matrix library.

This library is meant as a pedagogical tool in my linear algebra studies. It handles basic matrix arithmetic without abstracting away the hard parts. Its syntax is loosely inspired by Polars expression syntax.

## Usage

```python
from matrix import Matrix
from fractions import Fraction

>>> m = Matrix([
...   [1, 10, 2.4],
...   [complex(2, 4), 0, Fraction(3, 4)],
... ])

>>> print(m)
│ 1       10  2.4 │
│ (2+4j)  0   3/4 │

>>> m.append(m[0] + (m[1] * 2))
>>> print(m)
│ 1       10  2.4 │
│ (2+4j)  0   3/4 │
│ (5+8j)  10  3.9 │

>>> print(m * 0.5)
│ 0.5       5.0  1.2   │
│ (1+2j)    0.0  0.375 │
│ (2.5+4j)  5.0  1.95  │
```
```
