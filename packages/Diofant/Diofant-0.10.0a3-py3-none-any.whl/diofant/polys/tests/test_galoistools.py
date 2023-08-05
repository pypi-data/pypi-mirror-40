import pytest

from diofant import nextprime, pi
from diofant.domains import FF, ZZ
from diofant.polys import polyconfig as config
from diofant.polys.galoistools import (csolve_prime, gf_add, gf_add_ground,
                                       gf_add_mul, gf_berlekamp, gf_cofactors,
                                       gf_compose, gf_compose_mod, gf_crt,
                                       gf_crt1, gf_crt2, gf_csolve,
                                       gf_ddf_shoup, gf_ddf_zassenhaus,
                                       gf_diff, gf_div, gf_edf_shoup,
                                       gf_edf_zassenhaus, gf_eval, gf_expand,
                                       gf_exquo, gf_factor, gf_factor_sqf,
                                       gf_frobenius_map,
                                       gf_frobenius_monomial_base,
                                       gf_from_dict, gf_from_int_poly, gf_gcd,
                                       gf_gcdex, gf_int, gf_irred_p_ben_or,
                                       gf_irred_p_rabin, gf_irreducible,
                                       gf_irreducible_p, gf_lcm, gf_monic,
                                       gf_mul, gf_mul_ground, gf_neg, gf_pow,
                                       gf_pow_mod, gf_Qbasis, gf_Qmatrix,
                                       gf_quo, gf_rem, gf_sqr, gf_sub,
                                       gf_sub_ground, gf_sub_mul, gf_to_dict,
                                       gf_to_int_poly, gf_trace_map, gf_value,
                                       linear_congruence)
from diofant.polys.polyerrors import ExactQuotientFailed
from diofant.polys.rings import ring


__all__ = ()


def test_gf_crt():
    U = [49, 76, 65]
    M = [99, 97, 95]

    p = 912285
    u = 639985

    assert gf_crt(U, M, ZZ) == u

    E = [9215, 9405, 9603]
    S = [62, 24, 12]

    assert gf_crt1(M, ZZ) == (p, E, S)
    assert gf_crt2(U, M, p, E, S, ZZ) == u


def test_gf_int():
    assert gf_int(0, 5) == 0
    assert gf_int(1, 5) == 1
    assert gf_int(2, 5) == 2
    assert gf_int(3, 5) == -2
    assert gf_int(4, 5) == -1
    assert gf_int(5, 5) == 0


def test_gf_from_to_dict():
    f = {11: 12, 6: 2, 0: 25}
    F = {11: 1, 6: 2, 0: 3}
    g = [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3]

    assert gf_from_dict(f, 11, ZZ) == g
    assert gf_to_dict(g, 11) == F

    f = {11: -5, 4: 0, 3: 1, 0: 12}
    F = {11: -5, 3: 1, 0: 1}
    g = [6, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]

    assert gf_from_dict(f, 11, ZZ) == g
    assert gf_to_dict(g, 11) == F

    assert gf_to_dict([10], 11, symmetric=True) == {0: -1}
    assert gf_to_dict([10], 11, symmetric=False) == {0: 10}


def test_gf_from_to_int_poly():
    assert gf_from_int_poly([1, 0, 7, 2, 20], 5) == [1, 0, 2, 2, 0]
    assert gf_to_int_poly([1, 0, 4, 2, 3], 5) == [1, 0, -1, 2, -2]

    assert gf_to_int_poly([10], 11, symmetric=True) == [-1]
    assert gf_to_int_poly([10], 11, symmetric=False) == [10]


def test_gf_monic():
    assert gf_monic([], 11, ZZ) == (0, [])

    assert gf_monic([1], 11, ZZ) == (1, [1])
    assert gf_monic([2], 11, ZZ) == (2, [1])

    assert gf_monic([1, 2, 3, 4], 11, ZZ) == (1, [1, 2, 3, 4])
    assert gf_monic([2, 3, 4, 5], 11, ZZ) == (2, [1, 7, 2, 8])


def test_gf_arith():
    assert gf_neg([], 11, ZZ) == []
    assert gf_neg([1], 11, ZZ) == [10]
    assert gf_neg([1, 2, 3], 11, ZZ) == [10, 9, 8]

    assert gf_add_ground([], 0, 11, ZZ) == []
    assert gf_sub_ground([], 0, 11, ZZ) == []

    assert gf_add_ground([], 3, 11, ZZ) == [3]
    assert gf_sub_ground([], 3, 11, ZZ) == [8]

    assert gf_add_ground([1], 3, 11, ZZ) == [4]
    assert gf_sub_ground([1], 3, 11, ZZ) == [9]

    assert gf_add_ground([8], 3, 11, ZZ) == []
    assert gf_sub_ground([3], 3, 11, ZZ) == []

    assert gf_add_ground([1, 2, 3], 3, 11, ZZ) == [1, 2, 6]
    assert gf_sub_ground([1, 2, 3], 3, 11, ZZ) == [1, 2, 0]

    assert gf_mul_ground([], 0, 11, ZZ) == []
    assert gf_mul_ground([], 1, 11, ZZ) == []

    assert gf_mul_ground([1], 0, 11, ZZ) == []
    assert gf_mul_ground([1], 1, 11, ZZ) == [1]

    assert gf_mul_ground([1, 2, 3], 0, 11, ZZ) == []
    assert gf_mul_ground([1, 2, 3], 1, 11, ZZ) == [1, 2, 3]
    assert gf_mul_ground([1, 2, 3], 7, 11, ZZ) == [7, 3, 10]

    assert gf_add([], [], 11, ZZ) == []
    assert gf_add([1], [], 11, ZZ) == [1]
    assert gf_add([], [1], 11, ZZ) == [1]
    assert gf_add([1], [1], 11, ZZ) == [2]
    assert gf_add([1], [2], 11, ZZ) == [3]

    assert gf_add([1, 2], [1], 11, ZZ) == [1, 3]
    assert gf_add([1], [1, 2], 11, ZZ) == [1, 3]

    assert gf_add([1, 2, 3], [8, 9, 10], 11, ZZ) == [9, 0, 2]

    assert gf_sub([], [], 11, ZZ) == []
    assert gf_sub([1], [], 11, ZZ) == [1]
    assert gf_sub([], [1], 11, ZZ) == [10]
    assert gf_sub([1], [1], 11, ZZ) == []
    assert gf_sub([1], [2], 11, ZZ) == [10]

    assert gf_sub([1, 2], [1], 11, ZZ) == [1, 1]
    assert gf_sub([1], [1, 2], 11, ZZ) == [10, 10]

    assert gf_sub([3, 2, 1], [8, 9, 10], 11, ZZ) == [6, 4, 2]

    assert gf_add_mul(
        [1, 5, 6], [7, 3], [8, 0, 6, 1], 11, ZZ) == [1, 2, 10, 8, 9]
    assert gf_sub_mul(
        [1, 5, 6], [7, 3], [8, 0, 6, 1], 11, ZZ) == [10, 9, 3, 2, 3]

    assert gf_mul([], [], 11, ZZ) == []
    assert gf_mul([], [1], 11, ZZ) == []
    assert gf_mul([1], [], 11, ZZ) == []
    assert gf_mul([1], [1], 11, ZZ) == [1]
    assert gf_mul([5], [7], 11, ZZ) == [2]

    assert gf_mul([3, 0, 0, 6, 1, 2], [4, 0, 1, 0], 11, ZZ) == [1, 0,
                                                                3, 2, 4, 3, 1, 2, 0]
    assert gf_mul([4, 0, 1, 0], [3, 0, 0, 6, 1, 2], 11, ZZ) == [1, 0,
                                                                3, 2, 4, 3, 1, 2, 0]

    assert gf_mul([2, 0, 0, 1, 7], [2, 0, 0, 1, 7], 11, ZZ) == [4, 0,
                                                                0, 4, 6, 0, 1, 3, 5]

    assert gf_sqr([], 11, ZZ) == []
    assert gf_sqr([2], 11, ZZ) == [4]
    assert gf_sqr([1, 2], 11, ZZ) == [1, 4, 4]

    assert gf_sqr([2, 0, 0, 1, 7], 11, ZZ) == [4, 0, 0, 4, 6, 0, 1, 3, 5]


def test_gf_division():
    pytest.raises(ZeroDivisionError, lambda: gf_div([1, 2, 3], [], 11, ZZ))
    pytest.raises(ZeroDivisionError, lambda: gf_rem([1, 2, 3], [], 11, ZZ))
    pytest.raises(ZeroDivisionError, lambda: gf_quo([1, 2, 3], [], 11, ZZ))
    pytest.raises(ZeroDivisionError, lambda: gf_quo([1, 2, 3], [], 11, ZZ))

    assert gf_div([1], [1, 2, 3], 7, ZZ) == ([], [1])
    assert gf_rem([1], [1, 2, 3], 7, ZZ) == [1]
    assert gf_quo([1], [1, 2, 3], 7, ZZ) == []

    f = [5, 4, 3, 2, 1, 0]
    g = [1, 2, 3]
    q = [5, 1, 0, 6]
    r = [3, 3]

    assert gf_div(f, g, 7, ZZ) == (q, r)
    assert gf_rem(f, g, 7, ZZ) == r
    assert gf_quo(f, g, 7, ZZ) == q

    pytest.raises(ExactQuotientFailed, lambda: gf_exquo(f, g, 7, ZZ))

    f = [5, 4, 3, 2, 1, 0]
    g = [1, 2, 3, 0]
    q = [5, 1, 0]
    r = [6, 1, 0]

    assert gf_div(f, g, 7, ZZ) == (q, r)
    assert gf_rem(f, g, 7, ZZ) == r
    assert gf_quo(f, g, 7, ZZ) == q

    pytest.raises(ExactQuotientFailed, lambda: gf_exquo(f, g, 7, ZZ))

    assert gf_quo([1, 2, 1], [1, 1], 11, ZZ) == [1, 1]


def test_gf_expand():
    F = [([1, 1], 2), ([1, 2], 3)]

    assert gf_expand(F, 11, ZZ) == [1, 8, 3, 5, 6, 8]
    assert gf_expand((4, F), 11, ZZ) == [4, 10, 1, 9, 2, 10]


def test_gf_powering():
    assert gf_pow([1, 0, 0, 1, 8], 0, 11, ZZ) == [1]
    assert gf_pow([1, 0, 0, 1, 8], 1, 11, ZZ) == [1, 0, 0, 1, 8]
    assert gf_pow([1, 0, 0, 1, 8], 2, 11, ZZ) == [1, 0, 0, 2, 5, 0, 1, 5, 9]

    assert gf_pow([1, 0, 0, 1, 8], 5, 11, ZZ) == \
        [1, 0, 0, 5, 7, 0, 10, 6, 2, 10, 9, 6, 10, 6, 6, 0, 5, 2, 5, 9, 10]

    assert gf_pow([1, 0, 0, 1, 8], 8, 11, ZZ) == \
        [1, 0, 0, 8, 9, 0, 6, 8, 10, 1, 2, 5, 10, 7, 7, 9, 1, 2, 0, 0, 6, 2,
         5, 2, 5, 7, 7, 9, 10, 10, 7, 5, 5]

    assert gf_pow([1, 0, 0, 1, 8], 45, 11, ZZ) == \
        [ 1, 0, 0,  1,  8, 0, 0, 0, 0, 0, 0,  0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0,
          0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0,  4, 0, 0,  4, 10, 0, 0, 0, 0, 0, 0,
          10, 0, 0, 10,  3, 0, 0, 0, 0, 0, 0,  0, 0, 0,  0,  0, 0, 0, 0, 0, 0, 0,
          6, 0, 0,  6,  4, 0, 0, 0, 0, 0, 0,  8, 0, 0,  8,  9, 0, 0, 0, 0, 0, 0,
          10, 0, 0, 10,  3, 0, 0, 0, 0, 0, 0,  4, 0, 0,  4, 10, 0, 0, 0, 0, 0, 0,
          8, 0, 0,  8,  9, 0, 0, 0, 0, 0, 0,  9, 0, 0,  9,  6, 0, 0, 0, 0, 0, 0,
          3, 0, 0,  3,  2, 0, 0, 0, 0, 0, 0, 10, 0, 0, 10,  3, 0, 0, 0, 0, 0, 0,
          10, 0, 0, 10,  3, 0, 0, 0, 0, 0, 0,  2, 0, 0,  2,  5, 0, 0, 0, 0, 0, 0,
          4, 0, 0,  4, 10]

    assert gf_pow_mod([1, 0, 0, 1, 8], 0, [2, 0, 7], 11, ZZ) == [1]
    assert gf_pow_mod([1, 0, 0, 1, 8], 1, [2, 0, 7], 11, ZZ) == [1, 1]
    assert gf_pow_mod([1, 0, 0, 1, 8], 2, [2, 0, 7], 11, ZZ) == [2, 3]
    assert gf_pow_mod([1, 0, 0, 1, 8], 5, [2, 0, 7], 11, ZZ) == [7, 8]
    assert gf_pow_mod([1, 0, 0, 1, 8], 8, [2, 0, 7], 11, ZZ) == [1, 5]
    assert gf_pow_mod([1, 0, 0, 1, 8], 45, [2, 0, 7], 11, ZZ) == [5, 4]


def test_gf_gcdex():
    assert gf_gcdex([], [], 11, ZZ) == ([1], [], [])
    assert gf_gcdex([2], [], 11, ZZ) == ([6], [], [1])
    assert gf_gcdex([], [2], 11, ZZ) == ([], [6], [1])
    assert gf_gcdex([2], [2], 11, ZZ) == ([], [6], [1])

    assert gf_gcdex([], [3, 0], 11, ZZ) == ([], [4], [1, 0])
    assert gf_gcdex([3, 0], [], 11, ZZ) == ([4], [], [1, 0])

    assert gf_gcdex([3, 0], [3, 0], 11, ZZ) == ([], [4], [1, 0])

    assert gf_gcdex([1, 8, 7], [1, 7, 1, 7], 11, ZZ) == ([5, 6], [6], [1, 7])


def test_gf_gcd():
    assert gf_gcd([], [], 11, ZZ) == []
    assert gf_gcd([2], [], 11, ZZ) == [1]
    assert gf_gcd([], [2], 11, ZZ) == [1]
    assert gf_gcd([2], [2], 11, ZZ) == [1]

    assert gf_gcd([], [1, 0], 11, ZZ) == [1, 0]
    assert gf_gcd([1, 0], [], 11, ZZ) == [1, 0]

    assert gf_gcd([3, 0], [3, 0], 11, ZZ) == [1, 0]
    assert gf_gcd([1, 8, 7], [1, 7, 1, 7], 11, ZZ) == [1, 7]


def test_gf_lcm():
    assert gf_lcm([], [], 11, ZZ) == []
    assert gf_lcm([2], [], 11, ZZ) == []
    assert gf_lcm([], [2], 11, ZZ) == []
    assert gf_lcm([2], [2], 11, ZZ) == [1]

    assert gf_lcm([], [1, 0], 11, ZZ) == []
    assert gf_lcm([1, 0], [], 11, ZZ) == []

    assert gf_lcm([3, 0], [3, 0], 11, ZZ) == [1, 0]
    assert gf_lcm([1, 8, 7], [1, 7, 1, 7], 11, ZZ) == [1, 8, 8, 8, 7]


def test_gf_cofactors():
    assert gf_cofactors([], [], 11, ZZ) == ([], [], [])
    assert gf_cofactors([2], [], 11, ZZ) == ([1], [2], [])
    assert gf_cofactors([], [2], 11, ZZ) == ([1], [], [2])
    assert gf_cofactors([2], [2], 11, ZZ) == ([1], [2], [2])

    assert gf_cofactors([], [1, 0], 11, ZZ) == ([1, 0], [], [1])
    assert gf_cofactors([1, 0], [], 11, ZZ) == ([1, 0], [1], [])

    assert gf_cofactors([3, 0], [3, 0], 11, ZZ) == ([1, 0], [3], [3])
    assert gf_cofactors([1, 8, 7], [1, 7, 1, 7], 11, ZZ) == (([1, 7], [1, 1],
                                                              [1, 0, 1]))


def test_gf_diff():
    assert gf_diff([], 11, ZZ) == []
    assert gf_diff([7], 11, ZZ) == []

    assert gf_diff([7, 3], 11, ZZ) == [7]
    assert gf_diff([7, 3, 1], 11, ZZ) == [3, 3]

    assert gf_diff([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 11, ZZ) == []


def test_gf_eval():
    assert gf_eval([], 4, 11, ZZ) == 0
    assert gf_eval([], 27, 11, ZZ) == 0
    assert gf_eval([7], 4, 11, ZZ) == 7
    assert gf_eval([7], 27, 11, ZZ) == 7

    assert gf_eval([1, 0, 3, 2, 4, 3, 1, 2, 0], 0, 11, ZZ) == 0
    assert gf_eval([1, 0, 3, 2, 4, 3, 1, 2, 0], 4, 11, ZZ) == 9
    assert gf_eval([1, 0, 3, 2, 4, 3, 1, 2, 0], 27, 11, ZZ) == 5

    assert gf_eval([4, 0, 0, 4, 6, 0, 1, 3, 5], 0, 11, ZZ) == 5
    assert gf_eval([4, 0, 0, 4, 6, 0, 1, 3, 5], 4, 11, ZZ) == 3
    assert gf_eval([4, 0, 0, 4, 6, 0, 1, 3, 5], 27, 11, ZZ) == 9


def test_gf_compose():
    assert gf_compose([], [1, 0], 11, ZZ) == []
    assert gf_compose_mod([], [1, 0], [1, 0], 11, ZZ) == []

    assert gf_compose([1], [], 11, ZZ) == [1]
    assert gf_compose([1, 0], [], 11, ZZ) == []
    assert gf_compose([1, 0], [1, 0], 11, ZZ) == [1, 0]

    f = [1, 1, 4, 9, 1]
    g = [1, 1, 1]
    h = [1, 0, 0, 2]

    assert gf_compose(g, h, 11, ZZ) == [1, 0, 0, 5, 0, 0, 7]
    assert gf_compose_mod(g, h, f, 11, ZZ) == [3, 9, 6, 10]


def test_gf_trace_map():
    f = [1, 1, 4, 9, 1]
    a = [1, 1, 1]
    c = [1, 0]
    b = gf_pow_mod(c, 11, f, 11, ZZ)

    assert gf_trace_map(a, b, c, 0, f, 11, ZZ) == ([1, 1, 1], [1, 1, 1])
    assert gf_trace_map(a, b, c, 1, f, 11, ZZ) == ([5, 2, 10, 3], [5, 3, 0, 4])
    assert gf_trace_map(a, b, c, 2, f, 11, ZZ) == ([5, 9, 5, 3], [10, 1, 5, 7])
    assert gf_trace_map(a, b, c, 3, f, 11, ZZ) == ([1, 10, 6, 0], [7])
    assert gf_trace_map(a, b, c, 4, f, 11, ZZ) == ([1, 1, 1], [1, 1, 8])
    assert gf_trace_map(a, b, c, 5, f, 11, ZZ) == ([5, 2, 10, 3], [5, 3, 0, 0])
    assert gf_trace_map(a, b, c, 11, f, 11, ZZ) == ([1, 10, 6, 0], [10])


def test_gf_irreducible():
    assert gf_irreducible_p(gf_irreducible(1, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(2, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(3, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(4, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(5, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(6, 11, ZZ), 11, ZZ) is True
    assert gf_irreducible_p(gf_irreducible(7, 11, ZZ), 11, ZZ) is True


def test_gf_irreducible_p():
    assert gf_irred_p_ben_or([7], 11, ZZ) is True
    assert gf_irred_p_ben_or([7, 3], 11, ZZ) is True
    assert gf_irred_p_ben_or([7, 3, 1], 11, ZZ) is False

    assert gf_irred_p_rabin([7], 11, ZZ) is True
    assert gf_irred_p_rabin([7, 3], 11, ZZ) is True
    assert gf_irred_p_rabin([7, 3, 1], 11, ZZ) is False

    assert gf_irred_p_ben_or([2, 3, 4, 5, 6], 13, ZZ) is False
    assert gf_irred_p_ben_or([2, 3, 4, 5, 8], 13, ZZ) is True

    config.setup('GF_IRRED_METHOD', 'ben-or')

    assert gf_irreducible_p([7], 11, ZZ) is True
    assert gf_irreducible_p([7, 3], 11, ZZ) is True
    assert gf_irreducible_p([7, 3, 1], 11, ZZ) is False

    config.setup('GF_IRRED_METHOD', 'rabin')

    assert gf_irreducible_p([7], 11, ZZ) is True
    assert gf_irreducible_p([7, 3], 11, ZZ) is True
    assert gf_irreducible_p([7, 3, 1], 11, ZZ) is False

    config.setup('GF_IRRED_METHOD', 'other')
    pytest.raises(KeyError, lambda: gf_irreducible_p([7], 11, ZZ))
    config.setup('GF_IRRED_METHOD')

    f = [1, 9, 9, 13, 16, 15, 6, 7, 7, 7, 10]
    g = [1, 7, 16, 7, 15, 13, 13, 11, 16, 10, 9]

    h = gf_mul(f, g, 17, ZZ)

    assert gf_irred_p_ben_or(f, 17, ZZ) is True
    assert gf_irred_p_ben_or(g, 17, ZZ) is True

    assert gf_irred_p_ben_or(h, 17, ZZ) is False

    assert gf_irred_p_rabin(f, 17, ZZ) is True
    assert gf_irred_p_rabin(g, 17, ZZ) is True

    assert gf_irred_p_rabin(h, 17, ZZ) is False


def test_gf_frobenius_map():
    f = [2, 0, 1, 0, 2, 2, 0, 2, 2, 2]
    g = [1, 1, 0, 2, 0, 1, 0, 2, 0, 1]
    p = 3
    b = gf_frobenius_monomial_base(g, p, ZZ)
    h = gf_frobenius_map(f, g, b, p, ZZ)
    h1 = gf_pow_mod(f, p, g, p, ZZ)
    assert h == h1


def test_gf_berlekamp():
    f = gf_from_int_poly([1, -3, 1, -3, -1, -3, 1], 11)

    Q = [[1, 0, 0, 0, 0, 0],
         [3, 5, 8, 8, 6, 5],
         [3, 6, 6, 1, 10, 0],
         [9, 4, 10, 3, 7, 9],
         [7, 8, 10, 0, 0, 8],
         [8, 10, 7, 8, 10, 8]]

    V = [[1, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 0],
         [0, 0, 7, 9, 0, 1]]

    assert gf_Qmatrix(f, 11, ZZ) == Q
    assert gf_Qbasis(Q, 11, ZZ) == V

    assert gf_berlekamp(f, 11, ZZ) == [[1, 1], [1, 5, 3], [1, 2, 3, 4]]

    f = [1, 0, 1, 0, 10, 10, 8, 2, 8]

    Q = [[1, 0, 0, 0, 0, 0, 0, 0],
         [2, 1, 7, 11, 10, 12, 5, 11],
         [3, 6, 4, 3, 0, 4, 7, 2],
         [4, 3, 6, 5, 1, 6, 2, 3],
         [2, 11, 8, 8, 3, 1, 3, 11],
         [6, 11, 8, 6, 2, 7, 10, 9],
         [5, 11, 7, 10, 0, 11, 7, 12],
         [3, 3, 12, 5, 0, 11, 9, 12]]

    V = [[1, 0, 0, 0, 0, 0, 0, 0],
         [0, 5, 5, 0, 9, 5, 1, 0],
         [0, 9, 11, 9, 10, 12, 0, 1]]

    assert gf_Qmatrix(f, 13, ZZ) == Q
    assert gf_Qbasis(Q, 13, ZZ) == V

    assert gf_berlekamp(f, 13, ZZ) == [[1, 3], [1, 8, 4, 12], [1, 2, 3, 4, 6]]


def test_gf_ddf():
    f = gf_from_dict({15: ZZ(1), 0: ZZ(-1)}, 11, ZZ)
    g = [([1, 0, 0, 0, 0, 10], 1),
         ([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 2)]

    assert gf_ddf_zassenhaus(f, 11, ZZ) == g
    assert gf_ddf_shoup(f, 11, ZZ) == g

    f = gf_from_dict({63: ZZ(1), 0: ZZ(1)}, 2, ZZ)
    g = [([1, 1], 1),
         ([1, 1, 1], 2),
         ([1, 1, 1, 1, 1, 1, 1], 3),
         ([1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0,
           0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0,
           0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1], 6)]

    assert gf_ddf_zassenhaus(f, 2, ZZ) == g
    assert gf_ddf_shoup(f, 2, ZZ) == g

    f = gf_from_dict({6: ZZ(1), 5: ZZ(-1), 4: ZZ(1), 3: ZZ(1), 1: ZZ(-1)}, 3, ZZ)
    g = [([1, 1, 0], 1),
         ([1, 1, 0, 1, 2], 2)]

    assert gf_ddf_zassenhaus(f, 3, ZZ) == g
    assert gf_ddf_shoup(f, 3, ZZ) == g

    f = [1, 2, 5, 26, 677, 436, 791, 325, 456, 24, 577]
    g = [([1, 701], 1),
         ([1, 110, 559, 532, 694, 151, 110, 70, 735, 122], 9)]

    assert gf_ddf_zassenhaus(f, 809, ZZ) == g
    assert gf_ddf_shoup(f, 809, ZZ) == g

    p = ZZ(nextprime(int((2**15 * pi).evalf())))
    f = gf_from_dict({15: 1, 1: 1, 0: 1}, p, ZZ)
    g = [([1, 22730, 68144], 2),
         ([1, 64876, 83977, 10787, 12561, 68608, 52650, 88001, 84356], 4),
         ([1, 15347, 95022, 84569, 94508, 92335], 5)]

    assert gf_ddf_zassenhaus(f, p, ZZ) == g
    assert gf_ddf_shoup(f, p, ZZ) == g


def test_gf_edf():
    f = [1, 1, 0, 1, 2]
    g = [[1, 0, 1], [1, 1, 2]]

    assert gf_edf_zassenhaus(f, 2, 3, ZZ) == g
    assert gf_edf_shoup(f, 2, 3, ZZ) == g


def test_gf_factor():
    assert gf_factor([], 11, ZZ) == (0, [])
    assert gf_factor([1], 11, ZZ) == (1, [])
    assert gf_factor([1, 1], 11, ZZ) == (1, [([1, 1], 1)])

    assert gf_factor_sqf([], 11, ZZ) == (0, [])
    assert gf_factor_sqf([1], 11, ZZ) == (1, [])
    assert gf_factor_sqf([1, 1], 11, ZZ) == (1, [[1, 1]])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')

    assert gf_factor_sqf([], 11, ZZ) == (0, [])
    assert gf_factor_sqf([1], 11, ZZ) == (1, [])
    assert gf_factor_sqf([1, 1], 11, ZZ) == (1, [[1, 1]])

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')

    assert gf_factor_sqf([], 11, ZZ) == (0, [])
    assert gf_factor_sqf([1], 11, ZZ) == (1, [])
    assert gf_factor_sqf([1, 1], 11, ZZ) == (1, [[1, 1]])

    config.setup('GF_FACTOR_METHOD', 'shoup')

    assert gf_factor_sqf([], 11, ZZ) == (0, [])
    assert gf_factor_sqf([1], 11, ZZ) == (1, [])
    assert gf_factor_sqf([1, 1], 11, ZZ) == (1, [[1, 1]])

    f, p = [1, 0, 0, 1, 0], 2

    g = (1, [([1, 0], 1),
             ([1, 1], 1),
             ([1, 1, 1], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    g = (1, [[1, 0],
             [1, 1],
             [1, 1, 1]])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor_sqf(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor_sqf(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor_sqf(f, p, ZZ) == g

    f, p = gf_from_int_poly([1, -3, 1, -3, -1, -3, 1], 11), 11

    g = (1, [([1, 1], 1),
             ([1, 5, 3], 1),
             ([1, 2, 3, 4], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    f, p = [1, 5, 8, 4], 11

    g = (1, [([1, 1], 1), ([1, 2], 2)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    f, p = [1, 1, 10, 1, 0, 10, 10, 10, 0, 0], 11

    g = (1, [([1, 0], 2), ([1, 9, 5], 1), ([1, 3, 0, 8, 5, 2], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    f, p = gf_from_dict({32: 1, 0: 1}, 11, ZZ), 11

    g = (1, [([1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 10], 1),
             ([1, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 10], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    f, p = gf_from_dict({32: ZZ(8), 0: ZZ(5)}, 11, ZZ), 11

    g = (8, [([1, 3], 1),
             ([1, 8], 1),
             ([1, 0, 9], 1),
             ([1, 2, 2], 1),
             ([1, 9, 2], 1),
             ([1, 0, 5, 0, 7], 1),
             ([1, 0, 6, 0, 7], 1),
             ([1, 0, 0, 0, 1, 0, 0, 0, 6], 1),
             ([1, 0, 0, 0, 10, 0, 0, 0, 6], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    f, p = gf_from_dict({63: ZZ(8), 0: ZZ(5)}, 11, ZZ), 11

    g = (8, [([1, 7], 1),
             ([1, 4, 5], 1),
             ([1, 6, 8, 2], 1),
             ([1, 9, 9, 2], 1),
             ([1, 0, 0, 9, 0, 0, 4], 1),
             ([1, 2, 0, 8, 4, 6, 4], 1),
             ([1, 2, 3, 8, 0, 6, 4], 1),
             ([1, 2, 6, 0, 8, 4, 4], 1),
             ([1, 3, 3, 1, 6, 8, 4], 1),
             ([1, 5, 6, 0, 8, 6, 4], 1),
             ([1, 6, 2, 7, 9, 8, 4], 1),
             ([1, 10, 4, 7, 10, 7, 4], 1),
             ([1, 10, 10, 1, 4, 9, 4], 1)])

    config.setup('GF_FACTOR_METHOD', 'berlekamp')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    # Gathen polynomials: x**n + x + 1 (mod p > 2**n * pi)

    p = ZZ(nextprime(int((2**15 * pi).evalf())))
    f = gf_from_dict({15: 1, 1: 1, 0: 1}, p, ZZ)

    g = (1, [([1, 22730, 68144], 1),
             ([1, 81553, 77449, 86810, 4724], 1),
             ([1, 86276, 56779, 14859, 31575], 1),
             ([1, 15347, 95022, 84569, 94508, 92335], 1)])

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    g = (1, [[1, 22730, 68144],
             [1, 81553, 77449, 86810, 4724],
             [1, 86276, 56779, 14859, 31575],
             [1, 15347, 95022, 84569, 94508, 92335]])

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor_sqf(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor_sqf(f, p, ZZ) == g

    # Shoup polynomials: f = a_0 x**n + a_1 x**(n-1) + ... + a_n
    # (mod p > 2**(n-2) * pi), where a_n = a_{n-1}**2 + 1, a_0 = 1

    p = ZZ(nextprime(int((2**4 * pi).evalf())))
    f = [1, 2, 5, 26, 41, 39, 38]

    g = (1, [([1, 44, 26], 1),
             ([1, 11, 25, 18, 30], 1)])

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor(f, p, ZZ) == g

    g = (1, [[1, 44, 26],
             [1, 11, 25, 18, 30]])

    config.setup('GF_FACTOR_METHOD', 'zassenhaus')
    assert gf_factor_sqf(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'shoup')
    assert gf_factor_sqf(f, p, ZZ) == g

    config.setup('GF_FACTOR_METHOD', 'other')
    pytest.raises(KeyError, lambda: gf_factor([1, 1], 11, ZZ))
    config.setup('GF_FACTOR_METHOD')

    # IPoly interface:
    R, t = ring("t", FF(11))
    assert R.gf_factor_sqf(2*t + 3) == (2, [t + 7])


def test_gf_csolve():
    assert gf_value([1, 7, 2, 4], 11) == 2204

    assert linear_congruence(4, 3, 5) == [2]
    assert linear_congruence(0, 3, 5) == []
    assert linear_congruence(6, 1, 4) == []
    assert linear_congruence(0, 5, 5) == [0, 1, 2, 3, 4]
    assert linear_congruence(3, 12, 15) == [4, 9, 14]
    assert linear_congruence(6, 0, 18) == [0, 3, 6, 9, 12, 15]
    # with power = 1
    assert csolve_prime([1, 3, 2, 17], 7) == [3]
    assert csolve_prime([1, 3, 1, 5], 5) == [0, 1]
    assert csolve_prime([3, 6, 9, 3], 3) == [0, 1, 2]
    # with power > 1
    assert csolve_prime(
        [1, 1, 223], 3, 4) == [4, 13, 22, 31, 40, 49, 58, 67, 76]
    assert csolve_prime([3, 5, 2, 25], 5, 3) == [16, 50, 99]
    assert csolve_prime([3, 2, 2, 49], 7, 3) == [147, 190, 234]

    assert gf_csolve([1, 1, 7], 189) == [13, 49, 76, 112, 139, 175]
    assert gf_csolve([1, 3, 4, 1, 30], 60) == [10, 30]
    assert gf_csolve([1, 1, 7], 15) == []
