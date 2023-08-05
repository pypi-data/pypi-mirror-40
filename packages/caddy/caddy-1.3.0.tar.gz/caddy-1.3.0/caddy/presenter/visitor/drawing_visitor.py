from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.model.shape import ShapeVisitor
from caddy.view.canvas_interface import CanvasInterface


class DrawingVisitor(ShapeVisitor):

    def __init__(self, view: CanvasInterface) -> None:
        super().__init__()
        self.view = view

    def visit_polyline(self, line: PolyLine):
        prev_point = line.points[0]
        for next_point in line.points[1:]:
            self.view.add_line(tuple(prev_point), tuple(next_point), line.color)
            prev_point = next_point

    def visit_rectangle(self, rectangle: Rectangle):
        self.view.add_rectangle(tuple(rectangle.top_left_corner),
                                tuple(rectangle.bottom_right_corner), rectangle.color)

    def visit_circle(self, circle: Circle):
        self.view.add_circle(tuple(circle.center), circle.radius, circle.color)
