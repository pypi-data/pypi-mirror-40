from unittest import TestCase
from unittest.mock import patch, Mock

from caddy.model.model_interface import ModelObserver


class TestModelObserver(TestCase):

    def test_cannot_instantiate(self):
        with self.assertRaises(TypeError):
            ModelObserver()

    @patch.multiple(ModelObserver, __abstractmethods__=set())
    def test_on_shape_added(self):
        m = ModelObserver()
        with self.assertRaises(NotImplementedError):
            m.on_shape_added(None, None)

    @patch.multiple(ModelObserver, __abstractmethods__=set())
    def test_on_action(self):
        m = ModelObserver()
        with self.assertRaises(NotImplementedError):
            m.on_action(None, None)
