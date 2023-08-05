from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

T = TypeVar('T')
R = TypeVar('R')


class Result(ABC, Generic[T]):
    """
    A class indicating the result of parsing, either success of failure.
    """

    @abstractmethod
    def is_accepted(self) -> bool:
        pass

    @abstractmethod
    def result(self) -> T:
        pass

    @abstractmethod
    def rest(self) -> str:
        pass

    @abstractmethod
    def error_msg(self) -> str:
        pass

    @abstractmethod
    def map(self, f: Callable[[Accept[T]], Result[R]]) -> Result[R]:
        pass

    @abstractmethod
    def or_else(self, v: Callable[[], Result[T]]) -> Result[T]:
        pass


class Accept(Result, Generic[T]):
    """
    A class indicating a successful result of parsing.
    """

    def __init__(self, result: T, rest: str):
        self._result = result
        self._rest = rest

    def is_accepted(self) -> bool:
        return True

    def result(self) -> T:
        return self._result

    def rest(self) -> str:
        return self._rest

    def error_msg(self) -> str:
        raise TypeError('Trying to get error message from an Accept Result')

    def map(self, f: Callable[[Accept[T]], Result[R]]) -> Result[R]:
        return f(self)

    def or_else(self, v: Callable[[], Result[T]]) -> Result[T]:
        return self

    def __eq__(self, other):
        return self.result() == other.result() and \
            self.rest() == other.rest()

    def __str__(self) -> str:
        return f'Accept({repr(self.result())}, {repr(self.rest())})'

    def __repr__(self) -> str:
        return str(self)


class Reject(Result, Generic[T]):
    """
    A class indicating a failure while parsing.
    """

    def __init__(self, error: str):
        self._error = error

    def is_accepted(self) -> bool:
        return False

    def result(self) -> T:
        raise TypeError('Trying to get a result from a Reject Result')

    def rest(self) -> str:
        raise TypeError('Trying to get a rest from a Reject Result')

    def error_msg(self) -> str:
        return self._error

    def map(self, f: Callable[[Accept[T]], Result[R]]) -> Result[R]:
        return self

    def or_else(self, v: Callable[[], Result[T]]) -> Result[T]:
        return v()

    def __eq__(self, other):
        return self.error_msg() == other.error_msg()

    def __str__(self) -> str:
        return f'Reject({repr(self.error_msg())})'

    def __repr__(self) -> str:
        return str(self)
