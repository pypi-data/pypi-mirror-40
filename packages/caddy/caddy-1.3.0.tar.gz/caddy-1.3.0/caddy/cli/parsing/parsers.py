import re
from typing import TypeVar
from caddy.cli.parsing.combinator import Combinator
from caddy.cli.parsing.result import Accept, Reject, Result

T = TypeVar("T")


class String(Combinator):
    """
    Parses a literal string from the input when called.
    """
    def __init__(self, string: str):
        Combinator.__init__(self, self._parse)
        self.string = string

    def _parse(self, inp: str) -> Result[str]:
        str_len = len(self.string)
        if inp.startswith(self.string):
            return Accept(self.string, inp[str_len:])
        else:
            return Reject(
                f"Expected '{self.string}', got '{inp[:str_len]}'")


class Regex(Combinator):
    """
    Parses a regex from the input when called.
    """
    def __init__(self, pattern: str):
        Combinator.__init__(self, self._parse)
        self.regex = re.compile(pattern)

    def _parse(self, inp: str) -> Result[str]:
        match = self.regex.match(inp)
        if match:
            return Accept(match.group(), inp[match.end():])
        else:
            return Reject(f"No match for '{self.regex.pattern}'")


def ws_after(parser: Combinator[T], require_ws=True) -> Combinator[T]:
    """
    Create a new combinator which accepts the same strings as `parser`
    but which also discards all the Whitespace that's located after them.

    If require_ws is True, the produces Combinator requires at least one
    whitespace character at the end of the input.
    """
    regex = "\\s+" if require_ws else "\\s*"
    return parser << Regex(regex)
