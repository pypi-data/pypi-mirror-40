from unittest import TestCase
from unittest.mock import MagicMock, Mock

from caddy.model.actions import MoveAction, RemoveAction, ListAction, ClearAction


class TestMoveAction(TestCase):
    def test_accept_visitor(self):
        a = MoveAction(Mock(), Mock(), 1)
        visitor = MagicMock()
        a.accept_visitor(visitor)
        visitor.visit_move_action.assert_called_once_with(a)


class TestRemoveAction(TestCase):
    def test_accept_visitor(self):
        a = RemoveAction(Mock(), 1)
        visitor = MagicMock()
        a.accept_visitor(visitor)
        visitor.visit_remove_action.assert_called_once_with(a)


class TestListAction(TestCase):
    def test_accept_visitor(self):
        a = ListAction(Mock(), [1])
        visitor = MagicMock()
        a.accept_visitor(visitor)
        visitor.visit_list_action.assert_called_once_with(a)


class TestClearAction(TestCase):
    def test_accept_visitor(self):
        a = ClearAction()
        visitor = MagicMock()
        a.accept_visitor(visitor)
        visitor.visit_clear_action.assert_called_once_with(a)
