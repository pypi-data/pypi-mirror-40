from unittest import TestCase, mock
from unittest.mock import Mock

from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.presenter.visitor.drawing_visitor import DrawingVisitor
from caddy.shared.point import Point


class TestDrawingVisitor(TestCase):

    def test_visit_polyline(self):
        add_line = Mock()
        view = Mock()
        view.add_line = add_line
        drawing_visitor = DrawingVisitor(view)

        points = [Point(0, 0), Point(10, 10), Point(10, 0)]
        line = PolyLine(0, points)
        line.accept_visitor(drawing_visitor)
        add_line.assert_has_calls([mock.call((0, 0), (10, 10), line.color), mock.call((10, 10), (10, 0), line.color)])

    def test_visit_rectangle(self):
        add_rectangle = Mock()
        view = Mock()
        view.add_rectangle = add_rectangle
        drawing_visitor = DrawingVisitor(view)

        rectangle = Rectangle(0, Point(1, 2), Point(2, 1))
        rectangle.accept_visitor(drawing_visitor)
        add_rectangle.assert_called_once_with((1, 2), (2, 1), rectangle.color)

    def test_visit_circle(self):
        add_circle = Mock()
        view = Mock()
        view.add_circle = add_circle
        drawing_visitor = DrawingVisitor(view)

        circle = Circle(0, Point(10, 6), 5)
        circle.accept_visitor(drawing_visitor)
        add_circle.assert_called_once_with((10, 6), 5, circle.color)
        add_circle.reset_mock()

        circle = Circle(1, Point(-5, -10), 10)
        circle.accept_visitor(drawing_visitor)
        add_circle.assert_called_once_with((-5, -10), 10, circle.color)
