"""Definitions of common exceptions for :mod:`diofant.core` module. """


class BaseCoreError(Exception):
    """Base class for core related exceptions. """


class NonCommutativeExpression(BaseCoreError):
    """Raised when expression didn't have commutative property. """
