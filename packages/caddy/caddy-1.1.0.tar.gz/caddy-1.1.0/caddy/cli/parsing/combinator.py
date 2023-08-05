from __future__ import annotations
from typing import Callable, Generic, List, TypeVar
from caddy.cli.parsing.result import Result, Accept

T = TypeVar('T')
R = TypeVar('R')
Parser = Callable[[str], Result[T]]


class Combinator(Generic[T]):
    """
    A parser combinator is a class that can be called and will consume
    part of a string and return a result, specified by its action.

    It also defines multiple operators that allow composing parsers.

    Some of the functions in this class are based on Filip Krikava
    parser combinator example, located at:
    https://gitlab.fit.cvut.cz/BI-OOP/lecture-5-code/tree/master/src/main/java/parser
    """

    def __init__(self, action: Parser):
        """Create a Combinator from a simple function consuming a str and returning a result"""
        self.action = action

    def __call__(self, inp: str) -> Result[T]:
        """Try to parse the given string according to Combinator's action"""
        return self.action(inp)

    def __or__(self, other: Parser[T]) -> Combinator[T]:
        """
        Create a new Combinator that either accepts string accepted
        by this Combinator or by the other one
        """
        return Combinator(lambda inp: self(inp).or_else(lambda: other(inp)))

    def __rshift__(self, other: Parser[R]) -> Combinator[R]:
        """
        Create a new Combinator that first parses the string using this
        Combinator and then parses the rest of it using the other Combinator,
        returning the Result produced by the other Combinator.
        """
        return Combinator(lambda inp: self(inp).map(
            lambda x: other(x.rest())))

    def __lshift__(self, other: Parser[R]) -> Combinator[R]:
        """
        Create a new Combinator that first parses the string using this
        Combinator and then parses the rest of it using the other Combinator,
        returning the Result produced by the this Combinator.
        """
        return Combinator(lambda inp: self(inp).map(
            lambda x: other(x.rest()).map(
                lambda y: Accept(x.result(), y.rest()))))

    def __add__(self, other: Parser[T]) -> Combinator[List[T]]:
        """
        Create a new Combinator that first parses the string using this
        Combinator and then parses the rest of it using the other Combinator,
        returning a Result class which contains a list of results from the respective
        combinators in its result() property.

        This function creates a flattened list, so as not to produce unnecessarily nested lists.
        For example:
            parser = String("a") + String("b") + String("c")
            parser("abcd") == Accept(["a", "b", "c"], "d")

        This may unfortunately trip you up, note the joining of two unrelated lists in this case:
            parser = (Number.iterate(Whitespace)) + String("a")
            parser("1 2 3 4b") == Accept([1, 2, 3, 4, "b"], "")

        Whereas you may have expected result to be:
            Result([[1, 2, 3, 4], "b"])
        """
        def _join_results(r1, r2) -> List[T]:
            res1 = r1.result()
            if isinstance(res1, list):
                res1.append(r2.result())
                return res1
            return [res1, r2.result()]

        def _add_result(res: Result[T]):
            return res.map(lambda res1: other(res1.rest())
                           .map(lambda res2: Accept(
                               _join_results(res1, res2), res2.rest())))

        return Combinator(lambda imp: self(imp).map(_add_result))

    def map(self, f: Callable[[T], R]) -> Combinator[T]:
        """
        Create a new Combinator which accepts the same inputs as this one
        but the result() property of its Results has `f` applied to it.
        """
        return Combinator(lambda inp: self(inp).map(
            lambda res: Accept(f(res.result()), res.rest())))

    def iterate(self, sep: Combinator[T]) -> Combinator[List[T]]:
        """
        Create what's essentially a Kleene Star version of this Combinator but
        with separators defined by `sep` inserted between strings accepted by
        the Combinator.

        For example:
            parser = Number.iterate(Whitespace)
            parser("1 2       3 4    5") == Accept([1, 2, 3, 4, 5], "")
            parser("") == Accept([], "")
        """
        return Combinator(lambda inp: self._iterate_inner(sep, inp))

    def _iterate_inner(self, sep: Combinator[T], inp: str) -> Result[List[T]]:
        items = []
        rest = inp
        result = self(rest)

        while result.is_accepted():
            items.append(result.result())
            rest = result.rest()
            result = sep(rest).map(lambda res: self(res.rest()))

        return Accept(items, rest)
