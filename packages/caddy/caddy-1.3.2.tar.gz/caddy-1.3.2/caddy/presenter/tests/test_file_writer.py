import os
import tempfile
from unittest import TestCase

from caddy.presenter.file_writer import FileWriter


class TestFileWriter(TestCase):

    def test_add_multiple(self):

        file_path = tempfile.mkstemp()[1]
        try:
            file_writer = FileWriter(file_path)
            file_writer.add_text_command('command 1')
            file_writer.add_text_command('command 2')
            file_writer.add_text_command('command 3')
            file_writer.close()
            result = open(file_path)
            contents = result.read()
            result.close()
        finally:
            os.remove(file_path)

        self.assertEqual(contents, 'command 1\ncommand 2\ncommand 3\n')
