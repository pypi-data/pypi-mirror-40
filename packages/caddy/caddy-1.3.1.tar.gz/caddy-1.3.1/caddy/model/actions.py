from abc import abstractmethod, ABC
from typing import List

from caddy.shared.point import Point


class ActionVisitor(ABC):

    @abstractmethod
    def visit_remove_action(self, action: 'RemoveAction'):
        raise NotImplementedError

    @abstractmethod
    def visit_move_action(self, action: 'MoveAction'):
        raise NotImplementedError

    @abstractmethod
    def visit_list_action(self, action: 'ListAction'):
        raise NotImplementedError

    @abstractmethod
    def visit_clear_action(self, action: 'ClearAction'):
        raise NotImplementedError


class ActionInterface(ABC):

    @abstractmethod
    def accept_visitor(self, visitor: ActionVisitor):
        raise NotImplementedError


class RemoveAction(ActionInterface):

    def __init__(self, point: Point, removed_count: int):
        self.point = point
        self.count = removed_count

    def accept_visitor(self, visitor: ActionVisitor):
        visitor.visit_remove_action(self)


class MoveAction(ActionInterface):

    def __init__(self, overlapping: Point, offset: Point, moved_count: int):
        self.overlapping = overlapping
        self.offset = offset
        self.count = moved_count

    def accept_visitor(self, visitor: ActionVisitor):
        visitor.visit_move_action(self)


class ListAction(ActionInterface):

    def __init__(self, overlapping: Point, shapes: List):
        self.overlapping = overlapping
        self.shapes = shapes

    def accept_visitor(self, visitor: ActionVisitor):
        visitor.visit_list_action(self)


class ClearAction(ActionInterface):

    def accept_visitor(self, visitor: ActionVisitor):
        visitor.visit_clear_action(self)
