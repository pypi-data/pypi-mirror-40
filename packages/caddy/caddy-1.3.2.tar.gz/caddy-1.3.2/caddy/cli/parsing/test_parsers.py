from unittest import TestCase
# from src.cli.result import Accept, Reject
from caddy.cli.parsing.parsers import Regex, String, ws_after


class TestString(TestCase):
    def test_success(self):
        parser = String("Hello")
        res = parser("Hello, world")
        self.assertTrue(res.is_accepted(), "input should get accepted")
        self.assertEqual(res.result(), "Hello")
        self.assertEqual(res.rest(), ", world")

    def test_failure(self):
        parser = String("Hello")
        res = parser("Goodbye, world")
        self.assertFalse(res.is_accepted(), "input should get rejected")
        self.assertEqual(res.error_msg(), "Expected 'Hello', got 'Goodb'")


class TestRegex(TestCase):
    def test_success(self):
        parser = Regex("Hello+")
        res = parser("Helloooo!!")
        self.assertTrue(res.is_accepted(), "input should get accepted")
        self.assertEqual(res.result(), "Helloooo")
        self.assertEqual(res.rest(), "!!")

    def test_no_rest(self):
        parser = Regex("Hello+")
        res = parser("Helloooo")
        self.assertTrue(res.is_accepted(), "input should get accepted")
        self.assertEqual(res.result(), "Helloooo")
        self.assertEqual(res.rest(), "")

    def test_failure(self):
        parser = Regex("Hello+")
        res = parser("Heloooo!")
        self.assertFalse(res.is_accepted())
        self.assertEqual(res.error_msg(), "No match for 'Hello+'")


class TestWsAfter(TestCase):
    def test_success(self):
        parser = ws_after(String("Hello"))
        res = parser("Hello world!")
        self.assertTrue(res.is_accepted())
        self.assertEqual(res.result(), "Hello")
        self.assertEqual(res.rest(), "world!")

    def test_failure(self):
        parser = ws_after(String("Hello"))
        res = parser("Helloworld!")
        self.assertFalse(res.is_accepted())

    def test_not_required(self):
        parser = ws_after(String("Hello"), False)
        res = parser("Helloworld!")
        self.assertTrue(res.is_accepted())
        self.assertEqual(res.result(), "Hello")
        self.assertEqual(res.rest(), "world!")
