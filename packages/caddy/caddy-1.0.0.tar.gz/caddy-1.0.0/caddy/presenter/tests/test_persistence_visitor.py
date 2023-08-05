from unittest import TestCase
from unittest.mock import Mock

from caddy.model.actions import RemoveAction, MoveAction, ListAction
from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.presenter.visitor.persistence_visitor import StringView, PersistenceVisitor
from caddy.shared.point import Point


class TestStringView(TestCase):

    def test_add_multiple(self):
        string_view = StringView()
        string_view.add_text_command('command 1')
        string_view.add_text_command('command 2')
        string_view.add_text_command('command 3')
        self.assertEqual(str(string_view), 'command 1\ncommand 2\ncommand 3')


class TestPersistenceVisitor(TestCase):

    def test_visit_polyline(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        points = [Point(0, 0), Point(10, 10), Point(10, 0)]
        line = PolyLine(0, points)
        line.accept_visitor(persistence_visitor)
        # add_text_command.assert_called_once_with('', '')

    def test_visit_rectangle(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        rectangle = Rectangle(0, Point(1, 2), Point(2, 1))
        rectangle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('rect 1,2 2,1',
                                                 'Rectangle(AbsolutePoint(1,2), AbsolutePoint(2,1))')
        add_text_command.reset_mock()

        rectangle = Rectangle(1, Point(-2, -1), Point(-1, -2))
        rectangle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('rect -2,-1 +1,-1',
                                                 'Rectangle(AbsolutePoint(-2,-1), AbsolutePoint(-1,-2))')
        add_text_command.reset_mock()

        rectangle = Rectangle(2, Point(-1, 10), Point(10, 1))
        rectangle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('rect -1,+10 10,1',
                                                 'Rectangle(AbsolutePoint(-1,10), AbsolutePoint(10,1))')
        add_text_command.reset_mock()

        rectangle = Rectangle(2, Point(1, 1), Point(2, -2))
        rectangle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('rect 1,1 +1,-3',
                                                 'Rectangle(AbsolutePoint(1,1), AbsolutePoint(2,-2))')

    def test_visit_circle(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        circle = Circle(0, Point(10, 6), 5)
        circle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('circle 10,6 5',
                                                 'Circle(AbsolutePoint(10,6), 5)')
        add_text_command.reset_mock()

        circle = Circle(1, Point(-5, 10), 10)
        circle.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('circle -5,+10 10',
                                                 'Circle(AbsolutePoint(-5,10), 10)')
        add_text_command.reset_mock()

    def test_visit_remove_action(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        remove_action = RemoveAction(Point(10, 10), 0)
        remove_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('remove 10,10',
                                                 'Remove(AbsolutePoint(10,10))\n'
                                                 '0 objects affected.')
        add_text_command.reset_mock()

        remove_action = RemoveAction(Point(-10, 10), 1)
        remove_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('remove -10,+10',
                                                 'Remove(AbsolutePoint(-10,10))\n'
                                                 '1 object affected.')
        add_text_command.reset_mock()

        remove_action = RemoveAction(Point(-10, -10), 2)
        remove_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('remove -10,-10',
                                                 'Remove(AbsolutePoint(-10,-10))\n'
                                                 '2 objects affected.')

    def test_visit_move_action(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        move_action = MoveAction(Point(10, 10), Point(5, 5), 0)
        move_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('move 10,10 15,15',
                                                 'Move(AbsolutePoint(10,10), AbsolutePoint(15,15))\n'
                                                 '0 objects affected.')
        add_text_command.reset_mock()

        move_action = MoveAction(Point(10, 10), Point(-20, 10), 1)
        move_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('move 10,10 -20,+10',
                                                 'Move(AbsolutePoint(10,10), AbsolutePoint(-10,20))\n'
                                                 '1 object affected.')
        add_text_command.reset_mock()

        move_action = MoveAction(Point(-10, -10), Point(-20, 10), 2)
        move_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('move -10,-10 -20,+10',
                                                 'Move(AbsolutePoint(-10,-10), AbsolutePoint(-30,0))\n'
                                                 '2 objects affected.')

    def test_visit_list_action(self):
        add_text_command = Mock()
        view = Mock()
        view.add_text_command = add_text_command
        persistence_visitor = PersistenceVisitor(view)

        shapes = [PolyLine(0, [Point(0, 0), Point(10, 10), Point(20, 0)]),
                  Rectangle(1, Point(1, 2), Point(2, 1)),
                  Circle(2, Point(1, 1), 5)]
        list_action = ListAction(Point(0, 0), shapes)
        list_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('list 0,0',
                                                 'line 0,0 10,10 20,0\n'
                                                 'rect 1,2 2,1\n'
                                                 'circle 1,1 5')
        add_text_command.reset_mock()

        shapes = []
        list_action = ListAction(Point(0, 0), shapes)
        list_action.accept_visitor(persistence_visitor)
        add_text_command.assert_called_once_with('list 0,0',
                                                 'No objects found.')
