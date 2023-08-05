import copy
from typing import Sequence, List

from caddy.model.actions import RemoveAction, ListAction, MoveAction
from caddy.model.circle import Circle
from caddy.model.model_interface import ModelObserver, ModelInterface
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.model.shape import Shape
from caddy.shared.point import Point


class IdGenerator:
    def __init__(self, offset: int = 0):
        self.id: int = offset

    def next(self) -> int:
        self.id += 1
        return self.id


class Model(ModelInterface):
    def __init__(self):
        self.shapes: List[Shape] = []
        self._observers: List[ModelObserver] = []
        self._id_gen = IdGenerator()

    def attach_observer(self, observer: ModelObserver):
        self._observers.append(observer)

    def detach_observer(self, observer: ModelObserver):
        self._observers = [o for o in self._observers if o != observer]

    def add_circle(self, center: Point, radius: int, color: str = '#000000') -> Circle:
        circle = Circle(self._id_gen.next(), center, radius, color)
        self.shapes.append(circle)
        self._update()
        return circle

    def add_rectangle(self, top_left_corner: Point, bottom_right_corner, color: str = '#000000') -> Rectangle:
        rectangle = Rectangle(self._id_gen.next(), top_left_corner, bottom_right_corner, color)
        self.shapes.append(rectangle)
        self._update()
        return rectangle

    def add_polyline(self, points: Sequence[Point], color: str = '#000000') -> PolyLine:
        polyline = PolyLine(self._id_gen.next(), copy.deepcopy(points), color)
        self.shapes.append(polyline)
        self._update()
        return polyline

    def remove_overlapping_with(self, point: Point) -> RemoveAction:
        orig_len = len(self.shapes)
        self.shapes = [s for s in self.shapes if not s.contains_point(point)]
        orig_len != len(self.shapes) and self._update()
        return RemoveAction(point, orig_len - len(self.shapes))

    def overlapping_with(self, point: Point) -> List[Shape]:
        return [s for s in self.shapes if s.contains_point(point)]

    def list(self, point: Point):
        return ListAction(point, self.overlapping_with(point))

    def find_by_id(self, shape_id: int):
        lst = [s for s in self.shapes if s.shape_id == shape_id]
        return lst[0] if len(lst) else None

    def clear(self):
        self.shapes = []
        self._update()

    def move_by(self, overlapping: Point, offset: Point) -> MoveAction:
        overlapping_shapes = self.overlapping_with(overlapping)
        for shape in overlapping_shapes:
            shape.move_by(offset)
        len(self.shapes) and self._update()
        return MoveAction(overlapping, offset, len(overlapping_shapes))

    def accept_visitor(self, visitor):
        for shape in self.shapes:
            shape.accept_visitor(visitor)

    def _update(self):
        for o in self._observers:
            o.on_model_changed()

    def remove_by_id(self, shape_id):
        if shape_id < 0:
            return

        orig_len = len(self.shapes)
        self.shapes = [s for s in self.shapes if s.shape_id != shape_id]
        orig_len != len(self.shapes) and self._update()
