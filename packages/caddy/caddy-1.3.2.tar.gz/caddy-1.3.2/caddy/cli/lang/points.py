from __future__ import annotations
from abc import ABC, abstractmethod
from caddy.shared.point import Point


class CLIPoint(Point, ABC):
    def __str__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self.x == other.x and self.y == other.y

    @abstractmethod
    def as_absolute(self, previous: Point) -> Point:
        pass

    @abstractmethod
    def as_relative(self, origin: Point) -> Point:
        pass


class AbsolutePoint(CLIPoint):
    def as_absolute(self, previous: Point) -> Point:
        return Point(self.x, self.y)

    def as_relative(self, origin: Point) -> Point:
        return self - origin


class RelativePoint(CLIPoint):
    def as_absolute(self, previous: Point) -> Point:
        if previous is None:
            return Point(self.x, self.y)
        return previous + self

    def as_relative(self, origin: Point) -> Point:
        return Point(self.x, self.y)
