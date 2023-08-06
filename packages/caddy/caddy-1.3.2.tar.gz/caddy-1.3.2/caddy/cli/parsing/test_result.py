from unittest import TestCase
from unittest.mock import Mock
from caddy.cli.parsing.result import Accept, Reject


class TestAccept(TestCase):
    def test_is_accepted(self):
        a = Accept(None, None)
        self.assertTrue(a.is_accepted())

    def test_accessors(self):
        a = Accept(42, "is the answer")
        self.assertEqual(a.result(), 42, "Result should be correct")
        self.assertEqual(a.rest(), "is the answer",
                         "rest should be correct")

    def test_error_msg(self):
        a = Accept(None, None)
        with self.assertRaises(TypeError):
            a.error_msg()

    def test_map(self):
        a = Accept(8, "")
        a.map(lambda x: self.assertEqual(
            a, x, "map should pass Accept instance in"))
        res = a.map(lambda x: Accept(x.result() ** 2, x.rest() + "test"))
        self.assertEqual(res, Accept(64, "test"))

    def test_or_else(self):
        a = Accept(8, "")
        self.assertEqual(a.or_else(lambda: 4), a)

    def test_repr(self):
        a = Accept(42, "is the answer")
        self.assertEqual(repr(a), "Accept(42, 'is the answer')")


class TestReject(TestCase):
    def test_is_accepted(self):
        r = Reject("Error msg")
        self.assertFalse(r.is_accepted())

    def test_accessors(self):
        r = Reject("Error msg")
        with self.assertRaises(TypeError):
            r.result()
        with self.assertRaises(TypeError):
            r.rest()

    def test_error_msg(self):
        r = Reject("Error msg")
        self.assertEqual(r.error_msg(), "Error msg")

    def test_map(self):
        r = Reject("Error msg")
        m = Mock()
        res = r.map(m.method)
        m.method.assert_not_called()
        self.assertEqual(res, r)

    def test_or_else(self):
        r = Reject("Error msg")
        a = Accept(4, "")
        self.assertEqual(r.or_else(lambda: a), a)

    def test_repr(self):
        r = Reject("Error msg")
        self.assertEqual(repr(r), "Reject('Error msg')")
