import pytest

from diofant import (O, PoleError, Rational, Symbol, cos, exp, log, oo, sin,
                     sqrt, symbols)
from diofant.abc import x


__all__ = ()


@pytest.mark.slow
def test_simple():
    # Gruntz' theses pp. 91 to 96
    # 6.6
    e = sin(1/x + exp(-x)) - sin(1/x)
    assert e.aseries(x) == (1/(24*x**4) - 1/(2*x**2) + 1 + O(x**(-6), (x, oo)))*exp(-x)
    assert e.series(x, oo) == (1/(24*x**4) - 1/(2*x**2) + 1 + O(x**(-6), (x, oo)))*exp(-x)
    # 6.7
    e = exp(x) * (exp(1/x + exp(-x)) - exp(1/x))
    assert e.aseries(x, n=4) == 1/(6*x**3) + 1/(2*x**2) + 1/x + 1 + O(x**(-4), (x, oo))
    # 6.11
    e = exp(exp(x)/(1 - 1/x))
    assert e.aseries(x) == exp(exp(x)/(1 - 1/x))
    assert e.aseries(x, bound=3) == exp(exp(x)/x**2)*exp(exp(x)/x)*exp(-exp(x) + exp(x)/(1 - 1/x) -
                                                                       exp(x)/x - exp(x)/x**2)*exp(exp(x))
    # 6.12
    e = exp(sin(1/x + exp(-exp(x)))) - exp(sin(1/x))
    assert e.aseries(x, n=4) == (-1/(2*x**3) + 1/x + 1 + O(x**(-4), (x, oo)))*exp(-exp(x))

    # 6.15
    def e3(x):
        return exp(exp(exp(x)))

    e = e3(x)/e3(x-1/e3(x))
    assert e.aseries(x, n=3) == 1 + exp(x + exp(x))*exp(-exp(exp(x))) + ((-exp(x)/2 - Rational(1, 2))*exp(x + exp(x)) +
                                                                         exp(2*x + 2*exp(x))/2)*exp(-2*exp(exp(x))) + O(exp(-3*exp(exp(x))), (x, oo))

    # A New Algorithm for Computing Asymptotic Series by Gruntz - Examples
    e = exp(exp(x)) * (exp(sin(1/x + 1/exp(exp(x)))) - exp(sin(1/x)))
    assert e.aseries(x, n=4) == -1/(2*x**3) + 1/x + 1 + O(x**(-4), (x, oo))
    n = Symbol('n', integer=True)
    e = (sqrt(n)*log(n)**2*exp(sqrt(log(n))*log(log(n))**2*exp(sqrt(log(log(n)))*log(log(log(n)))**3)))/n
    assert e.aseries(n) == exp(exp(sqrt(log(log(n)))*log(log(log(n)))**3)*sqrt(log(n))*log(log(n))**2)*log(n)**2/sqrt(n)


def test_hierarchical():
    # Gruntz' thesis pp.
    # 6.21
    e = sin(1/x + exp(-x))
    assert e.aseries(x, n=3, hir=True) == -exp(-2*x)*sin(1/x)/2 + \
        exp(-x)*cos(1/x) + sin(1/x) + O(exp(-3*x), (x, oo))

    # A New Algorithm for Computing Asymptotic Series by Gruntz - Examples
    e = sin(x) * cos(exp(-x))
    assert e.aseries(x, hir=True) == exp(-4*x)*sin(x)/24 - \
        exp(-2*x)*sin(x)/2 + sin(x) + O(exp(-6*x), (x, oo))
    pytest.raises(PoleError, lambda: e.aseries(x))


def test_sympyissue_7872():
    a, b = symbols('a b', integer=True, nonzero=True)
    e = exp(1/x + exp(-x**2) * (exp(a*x) - exp(b*x))) - exp(1/x)
    assert e.aseries(x, n=3, hir=True) == (exp(2*a*x + 1/x)/2 + exp(2*b*x + 1/x)/2 -
                                           exp(a*x + b*x + 1/x))*exp(-2*x**2) + (exp(a*x + 1/x) -
                                                                                 exp(b*x + 1/x))*exp(-x**2) + O(exp(-3*x**2), (x, -oo))
