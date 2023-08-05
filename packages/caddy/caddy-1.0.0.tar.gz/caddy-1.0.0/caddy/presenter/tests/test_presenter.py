import os
import tempfile
from unittest import TestCase
from unittest.mock import Mock

from caddy.presenter.presenter import Presenter


class TestPresenter(TestCase):
    # TODO

    def test_on_model_changed(self):
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))
        presenter.on_model_changed()

    def test_on_new_file(self):
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))
        presenter.on_new_file()

    def test_on_file_save(self):
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))

        file_path = tempfile.mkstemp()[1]
        try:
            presenter.on_file_save(file_path)
            result = open(file_path)
            contents = result.read()
            result.close()
        finally:
            os.remove(file_path)

        self.assertEqual(contents, '')
