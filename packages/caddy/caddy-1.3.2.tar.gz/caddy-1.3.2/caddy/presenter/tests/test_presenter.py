import os
import tempfile
from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch
from caddy.presenter.file_reader import ParseError
from caddy.presenter.presenter import Presenter


class TestPresenter(TestCase):
    action_mock = MagicMock()

    def test_on_model_changed(self):
        model_mock = MagicMock()
        canvas_mock = MagicMock()
        mock_drawing_visitor = Mock()
        presenter = Presenter(model_mock, (Mock(), Mock(), canvas_mock, Mock()))
        presenter.drawing_visitor = mock_drawing_visitor
        presenter.on_model_changed()
        canvas_mock.canvas_clear.assert_called_once()
        model_mock.accept_visitor.assert_called_once_with(mock_drawing_visitor)

    def test_on_shape_added(self):
        shape_mock = MagicMock()
        mock_cli_visitor = Mock()
        on_model_changed_mock = MagicMock()
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))
        presenter.cli_visitor = mock_cli_visitor
        presenter.on_model_changed = on_model_changed_mock
        presenter.on_shape_added(shape_mock, True)
        on_model_changed_mock.assert_called_once()
        shape_mock.accept_visitor.assert_called_once_with(mock_cli_visitor)
        presenter.on_shape_added(shape_mock, False)
        shape_mock.accept_visitor.assert_called_once_with(mock_cli_visitor)
        self.assertEqual(on_model_changed_mock.call_count, 2)

    def test_on_action(self):
        on_model_changed_mock = MagicMock()
        mock_cli_visitor = Mock()
        mock_action = MagicMock()
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))
        presenter.on_model_changed = on_model_changed_mock
        presenter.cli_visitor = mock_cli_visitor
        presenter.on_action(mock_action, True)
        on_model_changed_mock.assert_called_once()
        mock_action.accept_visitor.assert_called_once_with(mock_cli_visitor)

    def test_on_new_file(self):
        mock_cli = MagicMock()
        mock_model = MagicMock()
        mock_context = MagicMock()
        presenter = Presenter(mock_model, (Mock(), Mock(), Mock(), Mock()))
        presenter.cli = mock_cli
        presenter.context = mock_context
        presenter.on_new_file()
        mock_cli.cli_clear.assert_called_once()
        mock_model.clear.assert_called_once()
        mock_context.tool_cursor.assert_called_once()

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

    @patch('caddy.presenter.presenter.FileReader')
    def test_on_file_load(self, file_reader):

        reader_object = MagicMock()
        reader_object.validate = MagicMock()
        reader_object.load = MagicMock()
        mock_on_new_file = MagicMock()
        file_reader.return_value = reader_object
        path = "n/a"
        mock_cli = MagicMock()
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), mock_cli))
        presenter.on_new_file = mock_on_new_file

        presenter.on_file_load(path)
        reader_object.validate.assert_called_once()
        reader_object.load.assert_called_once()

        reader_object.validate = MagicMock(side_effect=ParseError('text'))
        file_reader.return_value = reader_object
        presenter.on_file_load(path)

        reader_object.validate.assert_called_once()
        reader_object.load.assert_called_once()
        mock_cli.add_text.assert_called_once_with('text')

    @patch('caddy.presenter.presenter.Action')
    def test_on_cli_command(self, mock_action):
        mock_action_obj = MagicMock()
        mock_action_obj.is_accepted = MagicMock(return_value=True)
        mock_action_obj.result = MagicMock()
        mock_action.return_value = mock_action_obj
        mock_cli_processor = MagicMock()
        mock_cli = MagicMock()
        presenter = Presenter(Mock(), (Mock(), Mock(), Mock(), Mock()))
        presenter.cli_processor = mock_cli_processor
        presenter.cli = mock_cli

        command = 'rect 10,10 20,20'
        presenter.on_cli_command(command)

        mock_cli_processor.process_command.assert_called_once_with(mock_action_obj.result())

        command = 'erect 10,10 20,20'
        mock_action_obj.is_accepted = MagicMock(return_value=False)
        mock_action.return_value = mock_action_obj
        presenter.on_cli_command(command)

        mock_cli_processor.process_command.assert_called_once_with(mock_action_obj.result())
        mock_cli.add_text.assert_called_once_with("Syntax Error, please try again")
