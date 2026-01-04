from fractions import Fraction
from matrix import Matrix, Row


def test_init_int_row():
    r = Row([1, 2, 3])
    assert r is not None


def test_init_float_row():
    r = Row([0.1, 10.001])
    assert r is not None


def test_init_complex_row():
    assert Row([complex(1, 2)]) is not None


def test_init_fraction_row():
    assert Row([Fraction(3, 4)]) is not None


def test_init_from_row():
    r = Row([1, 2, 3])
    assert Row(r) is not None


def test_init_mixed():
    r = Row([1, complex(2), Fraction(3, 4), 5.6])
    assert r is not None


def test_eq_row():
    r1 = Row([1, 2, 3])
    r2 = Row([1, 2, 3])
    r3 = Row(r1)
    assert r1 == r2
    assert r2 == r3
    assert r1 == r3


def test_len_row():
    vals = [1, 2, 3]
    r = Row(vals)
    assert len(vals) == len(r)
