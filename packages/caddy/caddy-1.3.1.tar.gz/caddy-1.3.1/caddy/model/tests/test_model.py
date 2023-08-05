from unittest import TestCase, mock
from unittest.mock import MagicMock, Mock

from caddy.model.actions import ListAction
from caddy.model.circle import Circle
from caddy.model.model import Model
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.shared.point import Point


class TestModel(TestCase):

    def test_attach_observer(self):
        model = Model()
        observer = MagicMock()
        model.attach_observer(observer)
        model.add_circle(Point(1, 1), 5)
        observer.on_shape_added.assert_called_once()

    def test_detach_observer(self):
        model = Model()
        observer = MagicMock()
        model.attach_observer(observer)
        model.add_circle(Point(1, 1), 5)
        model.detach_observer(observer)
        model.add_circle(Point(1, 2), 6)
        observer.on_shape_added.assert_called_once()

    def test_add_circle(self):
        model = Model()
        m = Mock()
        model._update_shape = m
        model.add_circle(Point(1, 1), 5)
        self.assertEqual(Circle(1, Point(1, 1), 5), model.shapes[0])
        m.assert_called_once()

    def test_add_rectangle(self):
        model = Model()
        m = Mock()
        model._update_shape = m
        model.add_rectangle(Point(1, 1), Point(5, 4))
        self.assertEqual(Rectangle(1, Point(1, 1), Point(5, 4)), model.shapes[0])
        m.assert_called_once()

    def test_add_polyline(self):
        model = Model()
        m = Mock()
        model._update_shape = m
        model.add_polyline([Point(1, 1)])
        self.assertEqual(PolyLine(1, [Point(1, 1)]), model.shapes[0])
        m.assert_called_once()

    def test_add_polyline_ghost(self):
        model = Model()
        m = Mock()
        model._update_shape = m
        model.add_polyline_ghost([Point(1, 1)])
        self.assertEqual([], model.shapes)
        m.assert_called_once()

    def test_remove_overlapping_with(self):
        def get_last_shape_id():
            return model.shapes[len(model.shapes) - 1].shape_id

        model = Model()
        model.add_polyline([Point(1, 1), Point(3, 1)])
        polyline_id = get_last_shape_id()
        model.add_rectangle(Point(0, 30), Point(20, 0))
        rectangle1_id = get_last_shape_id()
        model.add_rectangle(Point(10, 15), Point(20, 5))
        rectangle2_id = get_last_shape_id()
        model.add_circle(Point(10, 10), 3)
        circle_id = get_last_shape_id()

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes created')

        model.remove_overlapping_with(Point(1, 2))
        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([rectangle2_id, circle_id], shape_ids, 'shapes removed')

        model.remove_overlapping_with(Point(10, 8))
        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([], shape_ids, 'shapes removed')

    def test_overlapping_with(self):
        def get_last_shape_id():
            return model.shapes[len(model.shapes) - 1].shape_id

        model = Model()
        model.add_polyline([Point(1, 1), Point(3, 1)])
        polyline_id = get_last_shape_id()
        model.add_rectangle(Point(0, 30), Point(20, 0))
        rectangle1_id = get_last_shape_id()
        model.add_rectangle(Point(10, 15), Point(20, 5))
        rectangle2_id = get_last_shape_id()
        model.add_circle(Point(10, 10), 3)
        circle_id = get_last_shape_id()

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes created')

        shape_ids = list(map(lambda s: s.shape_id, model.overlapping_with(Point(1, 2))))
        self.assertEqual([polyline_id, rectangle1_id], shape_ids, 'shapes overlapping')

        shape_ids = list(map(lambda s: s.shape_id, model.overlapping_with(Point(10, 8))))
        self.assertEqual([rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes overlapping')

        shape_ids = list(map(lambda s: s.shape_id, model.shapes))
        self.assertEqual([polyline_id, rectangle1_id, rectangle2_id, circle_id], shape_ids, 'shapes unchanged')

    def test_clear(self):
        model = Model()
        model.add_polyline([Point(1, 1), Point(3, 1)])
        model.add_rectangle(Point(0, 30), Point(20, 30))
        model.clear()
        self.assertEqual([], model.shapes, 'shapes created')

    def test_move_by(self):
        model = Model()
        mock_shape1 = MagicMock()
        mock_shape2 = MagicMock()
        model.shapes = [mock_shape1, mock_shape2]
        point = Point(1, 1)
        offset = Point(1, 2)

        overlapping_mock = MagicMock(return_value=[mock_shape1, mock_shape2])
        model.overlapping_with = overlapping_mock
        moved_count = model.move_by(point, offset).count
        overlapping_mock.assert_called_once_with(point)
        mock_shape1.move_by.assert_called_once_with(offset)
        mock_shape2.move_by.assert_called_once_with(offset)
        self.assertEqual(2, moved_count)

        overlapping_mock = MagicMock(return_value=[mock_shape2])
        model.overlapping_with = overlapping_mock
        moved_count = model.move_by(point, offset).count
        self.assertEqual(1, overlapping_mock.call_count)
        self.assertEqual(1, mock_shape1.move_by.call_count)
        self.assertEqual(2, mock_shape2.move_by.call_count)
        self.assertEqual(1, moved_count)

    def test_accept_visitor(self):
        model = Model()
        visitor = MagicMock()
        model.add_polyline([Point(1, 1), Point(3, 1)])
        model.add_rectangle(Point(0, 30), Point(20, 30))
        model.add_circle(Point(10, 10), 3)
        model.accept_visitor(visitor)
        visitor.visit_polyline.assert_called_once()
        visitor.visit_rectangle.assert_called_once()
        visitor.visit_circle.assert_called_once()

    def test_update(self):
        model = Model()
        with self.subTest("update shape"):
            observer1 = MagicMock()
            observer2 = MagicMock()
            model.attach_observer(observer1)
            model.attach_observer(observer2)
            model._update_shape(Mock())
            observer1.on_shape_added.assert_called_once()
            observer2.on_shape_added.assert_called_once()
        with self.subTest("update action"):
            observer1 = MagicMock()
            observer2 = MagicMock()
            model.attach_observer(observer1)
            model.attach_observer(observer2)
            model._update_action(Mock())
            observer1.on_action.assert_called_once()
            observer2.on_action.assert_called_once()

    def test_list(self):
        model = Model()
        shape1 = MagicMock()
        shape2 = MagicMock()
        model.shapes = [shape1, shape2]

        with self.subTest("list all"):
            m1 = Mock()
            model._update_action = m1
            m2 = Mock()
            model.overlapping_with = m2
            model.list(None)
            m1.assert_called_once()
            call = m1.call_args
            call_args, call_kwargs = call
            self.assertEqual(call_args[0].shapes, model.shapes)
            self.assertEqual(call_args[1], False)

        with self.subTest("list certain point"):
            m1 = Mock()
            model._update_action = m1
            m2 = MagicMock(return_value=[shape1])
            model.overlapping_with = m2
            model.list(Point(0, 0))
            m1.assert_called_once()
            call = m1.call_args
            call_args, call_kwargs = call
            self.assertEqual(call_args[0].shapes, [shape1])
            self.assertEqual(call_args[0].overlapping, Point(0, 0))
            self.assertEqual(call_args[1], False)
