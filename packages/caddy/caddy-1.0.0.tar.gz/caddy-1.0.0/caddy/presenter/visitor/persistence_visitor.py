from typing import Iterable, Tuple, List

from caddy.model.actions import ActionVisitor, RemoveAction, ListAction, MoveAction
from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.model.shape import ShapeVisitor
from caddy.shared.command_interface import CommandInterface
from caddy.shared.point import Point


class StringView(CommandInterface):

    def __init__(self) -> None:
        self._commands: List[str] = []

    def __str__(self) -> str:
        return '\n'.join(self._commands)

    def add_text_command(self, command: str, command_result: str = ""):
        self._commands.append(command)


class PersistenceVisitor(ShapeVisitor, ActionVisitor):

    def __init__(self, view: CommandInterface) -> None:
        self.view = view

    @staticmethod
    def process_points(points: Iterable[Point]) -> List[str]:
        """Converts absolute points with negative coordinates to relative points according to the grammar in the
        assignment"""
        result = []
        prev_point = Point(0,0)

        for p in points:
            current_point = p

            if p.x < 0 or p.y < 0:
                relative_point = current_point - prev_point
                result.append('%+d,%+d' % (relative_point.x, relative_point.y))
            else:
                result.append('%d,%d' % (p.x, p.y))

            prev_point = p

        return result

    @staticmethod
    def render_command(long_cmd: str, short_cmd: str, points: Iterable[Point], other: str = '') -> Tuple[str, str]:
        c_other, r_other = (' ' + other, ', ' + other) if other else (other, other)
        command_points = ' '.join(str_point for str_point in PersistenceVisitor.process_points(points))
        absolute_points = ', '.join('AbsolutePoint(' + '%d,%d' % (p.x, p.y) + ')' for p in points)

        command = short_cmd + ' ' + command_points + c_other
        result = long_cmd + '(' + absolute_points + r_other + ')'
        return command, result

    @staticmethod
    def pluralize(num, text):
        return '%d %s%s' % (num, text, 's'[num == 1:])

    def visit_polyline(self, line: PolyLine):
        command, result = self.render_command('Polyline', 'line', line.points)
        self.view.add_text_command(command, result)

    def visit_rectangle(self, rectangle: Rectangle):
        points = (rectangle.top_left_corner, rectangle.bottom_right_corner)

        command, result = self.render_command('Rectangle', 'rect', points)
        self.view.add_text_command(command, result)

    def visit_circle(self, circle: Circle):
        command, result = self.render_command('Circle', 'circle', (circle.center,), str(circle.radius))
        self.view.add_text_command(command, result)

    def visit_remove_action(self, action: RemoveAction):
        point = (action.point,)

        command, result = self.render_command('Remove', 'remove', point)
        result = result + '\n' + self.pluralize(action.count, 'object') + ' affected.'
        self.view.add_text_command(command, result)

    def visit_move_action(self, action: MoveAction):
        points = (action.overlapping, action.overlapping + action.offset)

        command, result = self.render_command('Move', 'move', points)
        result = result + '\n' + self.pluralize(action.count, 'object') + ' affected.'
        self.view.add_text_command(command, result)

    def visit_list_action(self, action: ListAction):
        command = 'list ' + '%d,%d' % (action.overlapping.x,action.overlapping.y)
        string_view = StringView()
        list_visitor = PersistenceVisitor(string_view)

        for shape in action.shapes:
            shape.accept_visitor(list_visitor)

        result = str(string_view)
        if not result:
            result = 'No objects found.'
        self.view.add_text_command(command, result)
