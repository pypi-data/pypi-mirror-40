from unittest import TestCase
from unittest.mock import Mock
import tkinter as tk

from caddy.view.application import Application


class TestCli(TestCase):

    def test_unregistered_entry_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)

        app.cli.handle_entry_command("test string with spaces")

    def test_registered_entry_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)
        mock = Mock(return_value="test string with spaces")
        app.cli.entry.insert(tk.END, "t")

        app.cli.register_entry_handler(mock)
        res = app.cli.handle_entry_command(Mock())
        mock.assert_called_once()
        self.assertEqual(res, "test string with spaces")

        res = app.cli.entry.get()
        self.assertEqual(res, "")

    def test_change_entry_handler(self):
        root = tk.Toplevel()
        app = Application(master=root)

        app.cli.entry.insert(tk.END, "t")
        mock = Mock(return_value="test string with spaces")
        app.cli.register_entry_handler(mock)
        res = app.cli.handle_entry_command(Mock())
        mock.assert_called_once()
        self.assertEqual(res, "test string with spaces")

        app.cli.entry.insert(tk.END, "t")
        mock = Mock(return_value="another test string containing some command")
        app.cli.register_entry_handler(mock)
        res = app.cli.handle_entry_command(Mock())
        mock.assert_called_once()
        self.assertEqual(res, "another test string containing some command")

    def test_entry_handler_with_empty_entry(self):
        root = tk.Toplevel()
        app = Application(master=root)

        mock = Mock(return_value="test string with spaces")
        app.cli.register_entry_handler(mock)
        res = app.cli.handle_entry_command(Mock())
        mock.assert_not_called()
        self.assertEqual(res, None)

    def test_add_text_command(self):
        root = tk.Toplevel()
        app = Application(master=root)

        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "\n")

        app.cli.add_text_command("command")
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "> command\n\n")

        app.cli.add_text_command("command")
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "> command\n> command\n\n")

    def test_add_text_command_result(self):
        root = tk.Toplevel()
        app = Application(master=root)

        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "\n")

        app.cli.add_text_command_result("command result")
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "command result\n\n")

        app.cli.add_text_command_result("command result")
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "command result\ncommand result\n\n")

    def test_cli_clear(self):
        root = tk.Toplevel()
        app = Application(master=root)
        app.cli.entry.insert(tk.END, "cmd")
        app.cli.text.config(state=tk.NORMAL)
        app.cli.text.insert(tk.END, "cmd, test string")
        app.cli.text.config(state=tk.DISABLED)

        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "cmd, test string\n")
        txt = app.cli.entry.get()
        self.assertEqual(txt, "cmd")

        app.cli.cli_clear()
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "\n")
        txt = app.cli.entry.get()
        self.assertEqual(txt, "")

    def test_cli_clear_on_empty(self):
        root = tk.Toplevel()
        app = Application(master=root)

        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "\n")
        txt = app.cli.entry.get()
        self.assertEqual(txt, "")

        app.cli.cli_clear()
        txt = app.cli.text.get(1.0, tk.END)
        self.assertEqual(txt, "\n")
        txt = app.cli.entry.get()
        self.assertEqual(txt, "")


