from unittest import TestCase
from caddy.cli.lang.points import AbsolutePoint, RelativePoint
import caddy.cli.lang.parser as lang


class TestParser(TestCase):
    def test_point(self):
        with self.subTest("AbsolutePoint"):
            res = lang.Point("12,14")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), AbsolutePoint(12, 14))
        with self.subTest("RelativePoint"):
            res = lang.Point("-5,+9")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), RelativePoint(-5, 9))

    def test_point_pair(self):
        with self.subTest("Absolute"):
            res = lang.PointPair("12,14        90,92")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), (AbsolutePoint(12, 14), AbsolutePoint(90, 92)))
        with self.subTest("Relative"):
            res = lang.PointPair("-12,+14        +90,+92")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), (RelativePoint(-12, 14), RelativePoint(90, 92)))
        with self.subTest("Mixed"):
            res = lang.PointPair("12,14 +9,-9")
            self.assertTrue(res.is_accepted())
            self.assertEqual(res.result(), (AbsolutePoint(12, 14), RelativePoint(9, -9)))

    def test_line(self):
        with self.subTest("Simple line"):
            self._assert_action_result("line 10,10 -12,+12",
                                       ['line', AbsolutePoint(10, 10), RelativePoint(-12, 12)])

        with self.subTest("Polyline"):
            self._assert_action_result(
                "line 10,10 -12,+12 31,15 10,29 16,50",
                ['line', AbsolutePoint(10, 10), RelativePoint(-12, 12), [
                    AbsolutePoint(31, 15), AbsolutePoint(10, 29), AbsolutePoint(16, 50)]])

    def test_rect(self):
        with self.subTest("Point-defined"):
            self._assert_action_result(
                "rect 12,12 +20,-19",
                ["rect", (AbsolutePoint(12, 12), RelativePoint(20, -19))])
        with self.subTest("Size-defined"):
            self._assert_action_result(
                "rect 12,12 8 5",
                ["rect", AbsolutePoint(12, 12), 8, 5])

    def test_circle(self):
        with self.subTest("Point-defined"):
            self._assert_action_result(
                "circle 12,12 +20,-19",
                ["circle", (AbsolutePoint(12, 12), RelativePoint(20, -19))])
        with self.subTest("Size-defined"):
            self._assert_action_result(
                "circle 12,12 8",
                ["circle", AbsolutePoint(12, 12), 8])

    def test_load_save(self):
        filename = "/home/lang/out.out"
        for action in ["load", "save"]:
            with self.subTest(action):
                self._assert_action_result(f"{action} {filename}", [action, filename])

    def test_remove(self):
        self._assert_action_result("remove 12,12", ["remove", AbsolutePoint(12, 12)])
        self._assert_action_result("remove +12,+12", ["remove", RelativePoint(12, 12)])

    def test_move(self):
        self._assert_action_result("move 12,12 -1,+0", ["move", (AbsolutePoint(12, 12), RelativePoint(-1, 0))])

    def test_ls(self):
        with self.subTest("List all"):
            self._assert_action_result("ls", ["ls"])
        with self.subTest("List intersecting"):
            self._assert_action_result("ls 12,43", ["ls", AbsolutePoint(12, 43)])

    def _assert_action_result(self, inp: str, result, verbose=False):
        res = lang.Action(inp)
        if verbose:
            print(inp, ": ", res)
        self.assertTrue(res.is_accepted())
        self.assertEqual(res.result(), result)
