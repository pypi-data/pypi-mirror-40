from unittest import TestCase
from caddy.shared.point import Point
from caddy.cli.lang.points import AbsolutePoint, RelativePoint

class TestPoints(TestCase):
    def _point_test(self, c1, c2):
        p = c1(3, 6)
        self.assertTrue(p == c1(3, 6))
        self.assertFalse(p == c1(4, 5))
        self.assertFalse(p == c2(3, 6))
        self.assertEqual(repr(p), f"{c1.__name__}(3, 6)")
    
    def test_relative_point(self):
        self._point_test(RelativePoint, AbsolutePoint)
        p = RelativePoint(3, -6)
        self.assertEqual(p.as_absolute(None), Point(3, -6))
        self.assertEqual(p.as_absolute(AbsolutePoint(2, 4)), Point(5, -2))
        self.assertEqual(p.as_relative(Point(10, 10)), Point(3, -6))

    def test_absolute_point(self):
        self._point_test(AbsolutePoint, RelativePoint)
        p = AbsolutePoint(3, 6)
        self.assertEqual(p.as_absolute(Point(3, 10)), Point(3, 6))
        self.assertEqual(p.as_relative(Point(10, 5)), Point(-7, 1))