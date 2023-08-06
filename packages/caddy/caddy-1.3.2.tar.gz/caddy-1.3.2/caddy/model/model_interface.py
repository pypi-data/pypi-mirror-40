from abc import ABC, abstractmethod
from typing import Sequence

from caddy.model.actions import ActionInterface
from caddy.model.shape import Shape
from caddy.shared.point import Point


class ModelObserver(ABC):

    @abstractmethod
    def on_shape_added(self, shape: Shape, effective: bool):
        raise NotImplementedError()

    @abstractmethod
    def on_action(self, action: ActionInterface, visible: bool):
        raise NotImplementedError()


class ModelInterface(ABC):
    @abstractmethod
    def attach_observer(self, observer: ModelObserver):
        raise NotImplementedError()

    @abstractmethod
    def detach_observer(self, observer: ModelObserver):
        raise NotImplementedError()

    @abstractmethod
    def add_circle(self, center: Point, radius: int, color: str = '#000000'):
        raise NotImplementedError()

    @abstractmethod
    def add_rectangle(self, top_left_corner: Point, bottom_right_corner: Point, color: str = '#000000'):
        raise NotImplementedError()

    @abstractmethod
    def add_polyline(self, points: Sequence[Point], color: str = '#000000'):
        raise NotImplementedError()

    @abstractmethod
    def add_polyline_ghost(self, points: Sequence[Point]):
        raise NotImplementedError()

    @abstractmethod
    def remove_overlapping_with(self, point: Point):
        raise NotImplementedError()

    @abstractmethod
    def list(self, point=None):
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    @abstractmethod
    def move_by(self, overlapping: Point, offset: Point):
        raise NotImplementedError()

    @abstractmethod
    def accept_visitor(self, visitor):
        raise NotImplementedError()
