import os
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock

from caddy.presenter.file_reader import FileReader, ParseError


class TestFileWriter(TestCase):
    def test_load_multiple(self):
        file_path = tempfile.mkstemp()[1]
        with open(file_path, "w") as f:
            print("circle 0,0 10", file=f)
            print("rect 10,10 20,20", file=f)
            print("line 0,0 10,10 20,20", file=f)
        try:
            m = MagicMock()
            r = FileReader(file_path, m)
            self.assertTrue(r.validate())
            r.load()
            m.process_command.assert_called()   
        finally:
            os.remove(file_path)

    def test_load_error(self):
        file_path = tempfile.mkstemp()[1]
        with open(file_path, "w") as f:
            print("notacommand", file=f)
        try:
            m = MagicMock()
            r = FileReader(file_path, m)
            self.assertRaisesRegex(ParseError, "Syntax error on line 1", r.validate)
        finally:
            os.remove(file_path)
