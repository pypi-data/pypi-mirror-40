from abc import ABC, abstractmethod
from typing import Iterable, List

from caddy.model.actions import ActionVisitor, RemoveAction, ListAction, MoveAction, ClearAction
from caddy.model.circle import Circle
from caddy.model.polyline import PolyLine
from caddy.model.rectangle import Rectangle
from caddy.model.shape import ShapeVisitor
from caddy.shared.command_interface import CommandInterface
from caddy.shared.point import Point


class CommandStrategy(ABC):

    @abstractmethod
    def add_command(self, view: CommandInterface, command: str):
        raise NotImplementedError

    @abstractmethod
    def add_text(self, view: CommandInterface, text: str):
        raise NotImplementedError


class StandardStrategy(CommandStrategy):

    def add_command(self, view: CommandInterface, command: str):
        view.add_text_command(command)

    def add_text(self, view: CommandInterface, text: str):
        view.add_text(text)


class CommandsAsTextStrategy(CommandStrategy):

    def add_command(self, view: CommandInterface, command: str):
        self.add_text(view, command)

    def add_text(self, view: CommandInterface, text: str):
        view.add_text(text)


class PersistenceVisitor(ShapeVisitor, ActionVisitor):
    standard_strategy = StandardStrategy()
    commands_as_text_strategy = CommandsAsTextStrategy()

    def __init__(self, view: CommandInterface) -> None:
        self.view = view
        self.command_strategy: CommandStrategy = self.standard_strategy

    def add_command(self, command: str):
        self.command_strategy.add_command(self.view, command)

    def add_text(self, text: str):
        self.command_strategy.add_text(self.view, text)

    @staticmethod
    def process_points(points: Iterable[Point]) -> List[str]:
        """Converts absolute points with negative coordinates to relative points according to the grammar in the
        assignment"""
        result = []
        prev_point = Point(0, 0)

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
    def render_command(short_cmd: str, points: Iterable[Point], other: str = '') -> str:
        c_other = ' ' + other if other else other
        command_points = ' '.join(str_point for str_point in PersistenceVisitor.process_points(points))
        return short_cmd + ' ' + command_points + c_other

    @staticmethod
    def pluralize(num: int, text: str) -> str:
        return '%d %s%s' % (num, text, 's'[num == 1:])

    def visit_polyline(self, line: PolyLine):
        command = self.render_command('line', line.points)
        self.add_command(command)

    def visit_rectangle(self, rectangle: Rectangle):
        points = (rectangle.top_left_corner, rectangle.bottom_right_corner)

        command = self.render_command('rect', points)
        self.add_command(command)

    def visit_circle(self, circle: Circle):
        command = self.render_command('circle', (circle.center,), str(circle.radius))
        self.add_command(command)

    def visit_remove_action(self, action: RemoveAction):
        point = (action.point,)

        command = self.render_command('remove', point)
        result = self.pluralize(action.count, 'object') + ' affected.'
        self.add_command(command)
        self.add_text(result)

    def visit_move_action(self, action: MoveAction):
        points = (action.overlapping, action.overlapping + action.offset)

        command = self.render_command('move', points)
        result = self.pluralize(action.count, 'object') + ' affected.'
        self.add_command(command)
        self.add_text(result)

    def visit_list_action(self, action: ListAction):
        command = 'ls ' + '%d,%d' % (action.overlapping.x, action.overlapping.y)
        self.add_command(command)
        self.command_strategy = self.commands_as_text_strategy
        for shape in action.shapes:
            shape.accept_visitor(self)
        self.command_strategy = self.standard_strategy

    def visit_clear_action(self, action: ClearAction):
        self.add_command('clear')
