from dataclasses import dataclass
from copy import copy
from typing import Collection, Self
from fractions import Fraction


type Scalar = int | float | complex | Fraction


@dataclass
class Row:
    _vals: list[Scalar]

    def __add__(self, other) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(
                "Rowwise addition has not been implemented for values of type "
                + type(other).__name__
            )
        width = len(self._vals)
        if width != len(other._vals):
            raise ValueError("Cannot sum rows of different lengths")

        return self.__class__([self._vals[i] + other._vals[i] for i in range(width)])

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

    def __mul__(self, other) -> Self:
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return self.__class__([val * other for val in self._vals])

    def __floordiv__(self, other: Scalar) -> Self:
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return self.__class__([val.__floordiv__(other) for val in self._vals])

    def __rfloordiv__(self, other: Scalar) -> Self:
        return self.__floordiv__(other)

    def __truediv__(self, other: Scalar) -> Self:
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return self.__class__([val.__truediv__(other) for val in self._vals])

    def __rtruediv__(self, other: Scalar) -> Self:
        return self.__truediv__(other)

    def __copy__(self) -> Self:
        return self.__class__(copy(self._vals))

    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, self.__class__)
            and len(self._vals) == len(value._vals)
            and all(self._vals[i] == value._vals[i] for i in range(len(self._vals)))
        )


class Matrix:
    _rows: list[Row]

    def __init__(
        self,
        data: Collection[Collection[Scalar] | Row] | Self,
    ):
        if isinstance(data, self.__class__):
            self._rows = [copy(row) for row in data._rows]
            return
        if len(data) == 0:
            self._rows = []
            return
        width = len(data[0])
        if any(len(row) != width for row in data):
            raise ValueError("Rows must be of the same length")
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

    @property
    def dimensions(self) -> tuple[int, int]:
        """Returns matrix dimensions as (rows, cols)"""
        if len(self._rows) == 0:
            return 0, 0
        return len(self._rows), len(self._rows[0])

    def append(self, row: Row | Collection[Scalar]) -> None:
        if len(self._rows) > 0 and (
            expected_width := len(self._rows[0]) != (actual_width := len(row))
        ):
            raise ValueError(
                f"Was expecting row of width {expected_width}, got {actual_width}"
            )
        self._rows.append(Row(row))

    def iter_rows(self):
        """Iterate over matrix rows without mutating matrix."""
        return (copy(row) for row in self._rows)

    def iter_cols(self):
        """Iterate over matrix columns without mutating matrix."""
        if len(self._rows) == 0 or len(self._rows[0]) == 0:
            yield from ()
            return
        for i in range(len(self._rows[0])):
            yield Row([row[i] for row in self._rows])

    def __getitem__(self, key: int) -> Row:
        return copy(self._rows.__getitem__(key))

    def __setitem__(self, key, value: Row | Collection[Scalar]) -> None:
        if len(self._rows) == 0:
            raise IndexError("No rows to assign to")
        if (actual_width := len(value)) != (expected_width := len(self._rows[0])):
            raise ValueError(
                f"Expected row of width {expected_width}, got {actual_width}"
            )
        return self._rows.__setitem__(key, Row(value))

    def __delitem__(self, key: int):
        return self._rows.__delitem__(key)

    def __mul__(self, other: Scalar):
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return Matrix([row.__mul__(other) for row in self._rows])

    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, self.__class__)
            and len(self._rows) == len(value._rows)
            and all(self._rows[i] == value._rows[i] for i in range(len(self._rows)))
        )

    def __floordiv__(self, other: Scalar):
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return Matrix([row.__floordiv__(other) for row in self._rows])

    def __truediv__(self, other: Scalar):
        if not isinstance(other, (int, float, complex, Fraction)):
            raise TypeError("Expected a scalar, got " + type(other).__name__)
        return Matrix([row.__truediv__(other) for row in self._rows])

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot add {other.__class__} to {self.__class__}")
        if not self.dimensions == other.dimensions:
            raise ValueError("Cannot only add matrices with the same dimensions")
        if self.dimensions == (0, 0):
            return self.__class__([])
        return self.__class__(
            [self._rows[i] + other._rows[i] for i in range(len(self._rows))]
        )
