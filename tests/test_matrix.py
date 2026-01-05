from matrix import Matrix, Row
from fractions import Fraction

import pytest


def test_init_list_of_lists():
    data = [[1], [1.0], [complex(1, 1)], [Fraction(1, 2)]]
    assert isinstance(Matrix(data), Matrix)


def test_init_matrix():
    m1 = Matrix([[]])
    assert isinstance(Matrix(m1), Matrix)


def test_eq():
    m1 = Matrix(
        [
            [1, 2, 3],
            [10, 20, 30],
        ]
    )
    m2 = Matrix(
        [
            [1, 2, 3],
            [10, 20, 30],
        ]
    )
    assert m1 == m2
    assert m1 is not m2, "Reinstantiation is a new matrix"
    assert m1._rows is not m2._rows, "Reinstantiation creates new row collection"
    assert all(m1._rows[i] is not m2._rows[i] for i in range(len(m1._rows))), (
        "Reinstantiation creates new rows"
    )


def test_ne_width():
    m1 = Matrix([[]])
    m2 = Matrix([[1]])
    assert m1 != m2


def test_ne_height():
    m1 = Matrix([[]])
    m2 = Matrix([[], []])
    assert m1 != m2


def test_get_item():
    r1 = Row([])
    m1 = Matrix([r1])
    assert m1[0] == r1
    assert m1[0] == Row([])


def test_set_item():
    m1 = Matrix([[1, 2, 3]])
    m1[0] = Row([10, 20, 30])
    assert m1 == Matrix([[10, 20, 30]])


def test_dimension():
    m1 = Matrix([[1, 1], [2, 1], [3, 2], [4, 2]])
    assert m1.dimensions == (4, 2)


def test_empty_dimension():
    m1 = Matrix([])
    assert m1.dimensions == (0, 0)


def test_scalar_mul():
    m1 = Matrix(
        [
            [1, 1, 1],
            [10, 10, 10],
        ]
    )
    m2 = m1 * 3.5

    assert m1 == Matrix([[1, 1, 1], [10, 10, 10]]), "Self is not changed"
    assert m2 == Matrix([[3.5, 3.5, 3.5], [35.0, 35.0, 35.0]])


def test_scalar_floordiv():
    m1 = Matrix([[3, 3], [3, 3], [3, 3]])
    m2 = m1 // 2
    assert m1 == Matrix(
        [
            [3, 3],
            [3, 3],
            [3, 3],
        ]
    ), "Self is not changed"
    assert m2 == Matrix(
        [
            [1, 1],
            [1, 1],
            [1, 1],
        ]
    )


def test_scalar_truediv():
    m1 = Matrix([[3, 3], [3, 3], [3, 3]])
    m2 = m1 / 2
    assert m1 == Matrix(
        [
            [3, 3],
            [3, 3],
            [3, 3],
        ]
    ), "Self is not changed"
    assert m2 == Matrix(
        [
            [1.5, 1.5],
            [1.5, 1.5],
            [1.5, 1.5],
        ]
    )


def test_add():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[10, 20]])
    m3 = m1 + m2
    assert m1 == Matrix([[1, 2]]), "Self is not changed"
    assert m3 == Matrix([[11, 22]])


def test_append():
    m1 = Matrix([[1, 2, 3]])
    m1.append([10, 20, 30])
    assert m1 == Matrix([[1, 2, 3], [10, 20, 30]])


def test_iter_rows():
    m1 = Matrix(
        [
            [1, 2, 3],
            [10, 20, 30],
        ]
    )
    m1_rows = m1.iter_rows()
    assert next(m1_rows) == Row([1, 2, 3])
    assert next(m1_rows) == Row([10, 20, 30])
    with pytest.raises(StopIteration):
        next(m1_rows)


def test_iter_rows_empty():
    m1 = Matrix([])
    m1_rows = m1.iter_rows()
    with pytest.raises(StopIteration):
        next(m1_rows)


def test_iter_cols():
    m1 = Matrix(
        [
            [1, 2, 3],
            [10, 20, 30],
        ]
    )
    m1_cols = m1.iter_cols()
    assert next(m1_cols) == Row([1, 10])
    assert next(m1_cols) == Row([2, 20])
    assert next(m1_cols) == Row([3, 30])
    with pytest.raises(StopIteration):
        next(m1_cols)


def test_iter_cols_empty():
    m1 = Matrix([])
    m1_cols = m1.iter_cols()
    with pytest.raises(StopIteration):
        next(m1_cols)
