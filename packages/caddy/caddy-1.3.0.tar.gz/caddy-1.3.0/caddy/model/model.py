import copy
from typing import Sequence, List

from caddy.model.actions import RemoveAction, ListAction, MoveAction, ActionInterface, ClearAction
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

    def add_circle(self, center: Point, radius: int, color: str = '#000000'):
        circle = Circle(self._id_gen.next(), center, radius, color)
        self.shapes.append(circle)
        self._update_shape(circle)

    def add_rectangle(self, top_left_corner: Point, bottom_right_corner: Point, color: str = '#000000'):
        rectangle = Rectangle(self._id_gen.next(), top_left_corner, bottom_right_corner, color)
        self.shapes.append(rectangle)
        self._update_shape(rectangle)

    def add_polyline(self, points: Sequence[Point], color: str = '#000000'):
        polyline = PolyLine(self._id_gen.next(), copy.deepcopy(points), color)
        self.shapes.append(polyline)
        self._update_shape(polyline)

    def add_polyline_ghost(self, points: Sequence[Point]):
        polyline = PolyLine(self._id_gen.next(), points, '#CCCCCC')
        self.shapes.append(polyline)
        self._update_shape(polyline, False)
        self.shapes = [s for s in self.shapes if s.shape_id != polyline.shape_id]

    def remove_overlapping_with(self, point: Point):
        orig_len = len(self.shapes)
        self.shapes = [s for s in self.shapes if not s.contains_point(point)]
        self._update_action(RemoveAction(point, orig_len - len(self.shapes)), orig_len != len(self.shapes))

    def overlapping_with(self, point: Point) -> List[Shape]:
        return [s for s in self.shapes if s.contains_point(point)]

    def list(self, point=None):
        shapes = self.shapes
        if point is not None:
            shapes = self.overlapping_with(point)
        self._update_action(ListAction(point, shapes), False)

    def clear(self):
        self.shapes = []
        self._update_action(ClearAction(), True)

    def move_by(self, overlapping: Point, offset: Point) -> MoveAction:
        overlapping_shapes = self.overlapping_with(overlapping)
        for shape in overlapping_shapes:
            shape.move_by(offset)
        move_action = MoveAction(overlapping, offset, len(overlapping_shapes))
        self._update_action(move_action)
        return move_action

    def accept_visitor(self, visitor):
        for shape in self.shapes:
            shape.accept_visitor(visitor)

    def _update_shape(self, shape: Shape, effective: bool = True):
        for o in self._observers:
            o.on_shape_added(shape, effective)

    def _update_action(self, action: ActionInterface, visible: bool = True):
        for o in self._observers:
            o.on_action(action, visible)
