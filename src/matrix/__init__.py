from dataclasses import dataclass
from typing import Collection, Self
from fractions import Fraction


type Scalar = int | float | complex | Fraction

from copy import copy


@dataclass
class Row:
    _vals: list[Scalar]

    def __add__(self, other) -> Row:
        if not isinstance(other, Row):
            raise TypeError(
                "Rowwise addition has not been implemented for values of type "
                + type(other).__name__
            )
        width = len(self._vals)
        if width != len(other._vals):
            raise ValueError("Cannot sum rows of different lengths")

        return Row([self._vals[i] + other._vals[i] for i in range(width)])

    def __init__(
        self,
        vals: Collection[Scalar] | Self,
    ):
        if isinstance(vals, Row):
            self._vals = vals._vals
        else:
            self._vals = list(vals)

    def __str__(self) -> str:
        return f"[{', '.join(str(val) for val in self._vals)}]"

    def __len__(self) -> int:
        return len(self._vals)

    def __getitem__(self, key) -> Scalar:
        return self._vals.__getitem__(key)

    def __setitem__(self, key, value) -> None:
        return self._vals.__setitem__(key, value)

    def __delitem__(self, key) -> None:
        return self._vals.__delitem__(key)

    def __mul__(self, other) -> Row:
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return Row([val * other for val in self._vals])

    def __copy__(self) -> Row:
        return Row(copy(self._vals))


class Matrix:
    _rows: list[Row]

    def __init__(
        self,
        data: Collection[Collection[Scalar] | Row],
    ):
        self._rows = [Row(vals=row) for row in data]

    def __str__(self) -> str:
        col_widths = []
        for j in range(len(self._rows[0])):
            max_width = 0
            for i in range(len(self._rows)):
                width = len(str(self._rows[i][j]))
                max_width = max((max_width, width))
            col_widths.append(max_width)

        return f"""{
            "\n".join(
                f'''│{
                    "".join(
                        str(self._rows[i][j])
                        .ljust(col_widths[j] + 1)
                        .rjust(col_widths[j] + 2)
                        for j in range(len(self._rows[0]))
                    )
                }│'''
                for i in range(len(self._rows))
            )
        }"""

    def append(self, row: Row) -> None:
        self._rows.append(row)

    def __getitem__(self, key) -> Row:
        return copy(self._rows.__getitem__(key))

    def __setitem__(self, key, value) -> Row:
        return self._rows.__setitem__(key, value)

    def __delitem__(self, key):
        return self._rows.__delitem__(key)

    def __mul__(self, other):
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return Matrix([row.__mul__(other) for row in self._rows])
