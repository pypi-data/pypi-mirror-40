from unittest import TestCase
from unittest.mock import MagicMock, Mock

from caddy.presenter.tool.circle_tool import CircleTool, CircleStageTool
from caddy.presenter.tool.default_tool import DefaultTool
from caddy.presenter.tool.eraser_tool import EraserTool
from caddy.presenter.tool.line_tool import LineTool, LineStageTool, LineSegmentTool
from caddy.presenter.tool.list_tool import ListTool
from caddy.presenter.tool.move_tool import MoveTool, MoveStageTool
from caddy.presenter.tool.rectangle_tool import RectangleTool, RectangleStageTool
from caddy.presenter.tool_context import ToolContext
from caddy.shared.point import Point


class TestTool(TestCase):

    def setUp(self):
        self.context = ToolContext(MagicMock(), MagicMock())

    def test_move(self):
        self.context.tool_move()
        self.assertIsInstance(self.context._current_tool, MoveTool)

    def test_remove(self):
        self.context.tool_remove()
        self.assertIsInstance(self.context._current_tool, EraserTool)

    def test_add_line(self):
        self.context.tool_add_line()
        self.assertIsInstance(self.context._current_tool, LineTool)

    def test_add_rectangle(self):
        self.context.tool_add_rectangle()
        self.assertIsInstance(self.context._current_tool, RectangleTool)

    def test_add_circle(self):
        self.context.tool_add_circle()
        self.assertIsInstance(self.context._current_tool, CircleTool)

    def test_canvas_click(self):
        self.context.canvas_click(Mock())
        self.assertIsInstance(self.context._current_tool, DefaultTool)

    def test_move_tool(self):

        self.context.tool_move()
        self.assertIsInstance(self.context._current_tool, MoveTool)

        point1 = Point(1, 1)
        self.context.canvas_click(point1)
        self.assertIsInstance(self.context._current_tool, MoveStageTool)
        self.assertEqual(self.context.points[0], point1)

        point2 = Point(10, 10)
        move_by_mock = Mock()
        self.context.model.move_by = move_by_mock
        self.context.canvas_click(point2)
        self.assertIsInstance(self.context._current_tool, MoveTool)
        move_by_mock.assert_called_once_with(point1, Point(9, 9))

    def test_eraser_tool(self):
        point = Point(1, 1)
        self.context.tool_remove()
        self.assertIsInstance(self.context._current_tool, EraserTool)

        remove_overlapping_with = Mock()
        self.context.model.remove_overlapping_with = remove_overlapping_with
        self.context.canvas_click(point)
        remove_overlapping_with.assert_called_once_with(point)

    def test_list_tool(self):
        point = Point(1, 1)
        self.context.tool_list()
        self.assertIsInstance(self.context._current_tool, ListTool)

        list_mock = Mock()
        self.context.model.list = list_mock
        self.context.canvas_click(point)
        list_mock.assert_called_once_with(point)

    def test_line_tool(self):
        self.context.tool_add_line()
        self.assertIsInstance(self.context._current_tool, LineTool)

        points = [Point(x, x) for x in range(10)]
        self.context.canvas_click(points[0])
        self.assertIsInstance(self.context._current_tool, LineStageTool)

        self.context.canvas_click(points[1])
        self.assertIsInstance(self.context._current_tool, LineSegmentTool)

        add_polyline_ghost = Mock()
        self.context.model.add_polyline_ghost = add_polyline_ghost

        sad_iterator = 3
        for p in points[2:]:
            self.context.canvas_click(p)
            self.assertIsInstance(self.context._current_tool, LineSegmentTool)
            add_polyline_ghost.assert_called_once_with(points[:sad_iterator])
            add_polyline_ghost.reset_mock()
            sad_iterator = sad_iterator + 1

        self.assertEqual(self.context.points, points)

    def test_line_tool_prep(self):
        self.context.tool_add_line()
        self.assertIsInstance(self.context._current_tool, LineTool)
        self.context.canvas_click(Mock())
        self.assertIsInstance(self.context._current_tool, LineStageTool)
        self.context.canvas_click(Mock())
        self.assertIsInstance(self.context._current_tool, LineSegmentTool)

    def test_line_tool_cursor(self):
        self.test_line_tool_prep()
        self.context.tool_cursor()
        self.assertIsInstance(self.context._current_tool, DefaultTool)

    def test_line_tool_move(self):
        self.test_line_tool_prep()
        self.context.tool_move()
        self.assertIsInstance(self.context._current_tool, MoveTool)

    def test_line_tool_remove(self):
        self.test_line_tool_prep()
        self.context.tool_remove()
        self.assertIsInstance(self.context._current_tool, EraserTool)

    def test_list_tool_list(self):
        self.test_line_tool_prep()
        self.context.tool_list()
        self.assertIsInstance(self.context._current_tool, ListTool)

    def test_line_tool_add_line(self):
        self.test_line_tool_prep()
        self.context.tool_add_line()
        self.assertIsInstance(self.context._current_tool, LineTool)

    def test_line_tool_add_rectangle(self):
        self.test_line_tool_prep()
        self.context.tool_add_rectangle()
        self.assertIsInstance(self.context._current_tool, RectangleTool)

    def test_line_tool_add_circle(self):
        self.test_line_tool_prep()
        self.context.tool_add_circle()
        self.assertIsInstance(self.context._current_tool, CircleTool)

    def test_rectangle_tool(self):
        self.context.tool_add_rectangle()
        self.assertIsInstance(self.context._current_tool, RectangleTool)

        point1 = Point(1, 1)
        self.context.canvas_click(point1)
        self.assertIsInstance(self.context._current_tool, RectangleStageTool)
        self.assertEqual(self.context.points[0], point1)

        point2 = Point(10, 10)
        add_rectangle = Mock()
        self.context.model.add_rectangle = add_rectangle
        self.context.canvas_click(point2)
        self.assertIsInstance(self.context._current_tool, RectangleTool)
        add_rectangle.assert_called_once_with(point1, point2)

    def test_circle_tool(self):

        self.context.tool_add_circle()
        self.assertIsInstance(self.context._current_tool, CircleTool)

        point1 = Point(1, 1)
        self.context.canvas_click(point1)
        self.assertIsInstance(self.context._current_tool, CircleStageTool)
        self.assertEqual(self.context.points[0], point1)

        point2 = Point(1, 10)
        add_circle = Mock()
        self.context.model.add_circle = add_circle
        self.context.canvas_click(point2)
        self.assertIsInstance(self.context._current_tool, CircleTool)
        add_circle.assert_called_once_with(point1, 9)

    def test_file_save(self):
        self.context.tool_add_circle()
        set_state_indicator = Mock()
        self.context.view.set_state_indicator = set_state_indicator
        self.context.file_save('path/to/file.cad')
        set_state_indicator.assert_called_with('[Cursor] Saved path/to/file.cad')
