from fractions import Fraction
from matrix import Row


def test_init_int():
    assert isinstance(Row([1, 2, 3]), Row)


def test_init_float():
    assert isinstance(Row([0.1, 0.01]), Row)


def test_init_complex():
    assert isinstance(Row([complex(1, 2)]), Row)


def test_init_fraction():
    assert isinstance(Row([Fraction(3, 4)]), Row)


def test_init_from():
    r = Row([1, 2, 3])
    assert isinstance(Row(r), Row)


def test_init_mixed():
    r = Row([1, complex(2), Fraction(3, 4), 5.6])
    assert isinstance(r, Row)


def test_init_empty():
    assert isinstance(Row([]), Row)


def test_eq():
    r1 = Row([1, 2, 3])
    r2 = Row([1, 2, 3])
    r3 = Row(r1)
    assert r1 == r2
    assert r2 == r3
    assert r1 == r3


def test_len():
    vals = [1, 2, 3]
    r = Row(vals)
    assert len(vals) == len(r)


def test_add():
    r1 = Row([1, 2, 3])
    r2 = Row([10, 20, 30])
    add = r1 + r2
    assert r1 == Row([1, 2, 3]), "Self unchanged"
    assert r2 == Row([10, 20, 30]), "Argument unchanged"
    assert add == Row([11, 22, 33])


def test_get_item():
    r1 = Row([1, 2, 3])
    assert r1[0] == 1


def test_set_item():
    r1 = Row([1, 2, 3])
    r1[0] = 4
    assert r1 == Row([4, 2, 3])


def test_mul_scalar():
    r1 = Row([1, 2, 3])
    r2 = r1 * 2
    assert r1 == Row([1, 2, 3]), "Self unchanged"
    assert r2 == Row([2, 4, 6])


def test_floordiv():
    r1 = Row([5])
    r2 = r1.__floordiv__(2)
    r3 = r1 // 2
    assert r1 == Row([5]), "Self unchanged"
    assert r2 == Row([2])
    assert r3 == Row([2])


def test_truediv():
    r1 = Row([5])
    r2 = r1 / 2
    assert r1 == Row([5]), "Self unchanged"
    assert r2 == Row([2.5])


def test_copy():
    from copy import copy

    r1 = Row([1, 2.0, complex(3, 4), Fraction(5, 6)])
    r2 = copy(r1)
    assert r1 == r2, "Copy loses no data"
    assert r1 is not r2, "Copy creates new object"
    assert r1._vals is not r2._vals, "Copy creates new underlying list"
