from unittest import TestCase
import caddy.cli.parsing.parsers as parsers


class TestCombinator(TestCase):
    Number = parsers.Regex("(\\+|\\-)?\\d+").map(int)
    Whitespace = parsers.Regex("\\s+")
    Triple = (Number << Whitespace) + (Number << Whitespace) + Number

    def test_or(self):
        s1 = parsers.String("ab")
        s2 = parsers.String("cd")
        comb = (s1 | s2)

        with self.subTest("First alternative"):
            res = comb("abad")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), "ab")
            self.assertEqual(res.rest(), "ad")

        with self.subTest("Second alternative"):
            res = comb("cd-rom")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), "cd")
            self.assertEqual(res.rest(), "-rom")

        with self.subTest("Rejection"):
            res = comb("nonono")
            self.assertFalse(res.is_accepted())

    def test_rshift(self):
        combined = parsers.String("cd") >> parsers.String("-") >> parsers.String("rom")
        with self.subTest("Acceptance"):
            res = combined("cd-rome")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), "rom")
            self.assertEqual(res.rest(), "e")

        with self.subTest("Rejection"):
            res = combined("cd+rom")
            self.assertFalse(res.is_accepted())

    def test_lshift(self):
        combined = parsers.String("cd") << parsers.String("-") << parsers.String("rom")

        with self.subTest("Acceptance"):
            res = combined("cd-rome")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), "cd")
            self.assertEqual(res.rest(), "e")

        with self.subTest("Rejection"):
            res = combined("cd+rom")
            self.assertFalse(res.is_accepted())

    def test_add(self):
        with self.subTest("Acceptance"):
            res = TestCombinator.Triple("+13 -2 5")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), [13, -2, 5])
            self.assertEqual(res.rest(), "")

        with self.subTest("Rejection"):
            res2 = TestCombinator.Triple("+13 -a")
            self.assertFalse(res2.is_accepted())

    def test_iterate(self):
        NumberList = TestCombinator.Number.iterate(TestCombinator.Whitespace)
        with self.subTest("Multi-element"):
            res = NumberList("12 13 14 89 notanumber")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), [12, 13, 14, 89])
            self.assertEqual(res.rest(), " notanumber")

        with self.subTest("Empty list"):
            res = NumberList("notanumber")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), [])
            self.assertEqual(res.rest(), "notanumber")

        with self.subTest("Empty string"):
            res = NumberList("")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), [])
            self.assertEqual(res.rest(), "")
