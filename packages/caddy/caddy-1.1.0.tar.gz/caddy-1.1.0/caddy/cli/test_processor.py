from unittest import TestCase
from unittest.mock import MagicMock
from caddy.cli.processor import Processor, ProcessorEvent
from caddy.cli.lang.parser import Action
from caddy.model.model import Model
from caddy.shared.point import Point

class TestProcessor(TestCase):
    def test_rect(self):
        with self.subTest("Point rectangle"):
            rect = self.perform_action("rect 12,13 +3,-2")
            self.assertEqual(rect.top_left_corner, Point(12, 13))
            self.assertEqual(rect.bottom_right_corner, Point(15, 11))
        with self.subTest("Dimension rectangle"):
            rect = self.perform_action("rect +12,+13 5 10")
            self.assertEqual(rect.top_left_corner, Point(12, 13))
            self.assertEqual(rect.bottom_right_corner, Point(17, 3))

    def test_circle(self):
        with self.subTest("Radius circle"):
            c = self.perform_action("circle 2,2 10")
            self.assertEqual(c.center, Point(2, 2))
            self.assertEqual(c.radius, 10)
        with self.subTest("Point circle"):
            c = self.perform_action("circle 0,0 2,0")
            self.assertEqual(c.center, Point(1, 0))
            self.assertEqual(c.radius, 1)

    def test_line(self):
        l = self.perform_action("line 10,10 -5,+12 31,15 -10,-5 16,50")
        self.assertEqual(l.points, [
            Point(10, 10),
            Point(5, 22),
            Point(31, 15),
            Point(21, 10),
            Point(16, 50)
        ])

    def test_move_by(self):
        m = MagicMock()
        a = Action("move 10,10 13,5").result()
        Processor(m).process_command(a)
        m.move_by.assert_called_once_with(Point(10, 10), Point(3, -5))

    def test_clear(self):
        a = Action("clear").result()
        processor = Processor(None)
        m = MagicMock()
        processor.register_handler(ProcessorEvent.CLEAR, m)
        processor.process_command(a)
        m.assert_called_once()

    def test_remove(self):
        m = MagicMock()
        a = Action("remove +10,+10").result()
        Processor(m).process_command(a)
        m.remove_overlapping_with.assert_called_once_with(Point(10, 10))
    
    def test_save(self):
        a = Action("save /home/kayalan/out.cad").result()
        processor = Processor(None)
        m = MagicMock()
        processor.register_handler(ProcessorEvent.SAVE, m)
        processor.process_command(a)
        m.assert_called_once_with("/home/kayalan/out.cad")

    def test_load(self):
        a = Action("load /home/kayalan/out.cad").result()
        processor = Processor(None)
        m = MagicMock()
        processor.register_handler(ProcessorEvent.LOAD, m)
        processor.process_command(a)
        m.assert_called_once_with("/home/kayalan/out.cad")

    def test_ls(self):
        processor = Processor(None)
        with self.subTest("ls all"):
            a = Action("ls").result()
            m = MagicMock()
            Processor(m).process_command(a)
            m.list.assert_called_once()
        with self.subTest("ls overlapping"):
            a = Action("ls 12,10").result()
            m = MagicMock()
            Processor(m).process_command(a)
            m.list.assert_called_once_with(Point(12, 10))

    def test_quit(self):
        a = Action("quit").result()
        processor = Processor(None)
        m1 = MagicMock()
        processor.register_handler(ProcessorEvent.QUIT, m1)
        m2 = MagicMock()
        processor.register_handler(ProcessorEvent.QUIT, m2)
        processor.process_command(a)
        m1.assert_called_once()
        m2.assert_called_once()

    def perform_action(self, action):
        m = Model()
        processor = Processor(m)
        a = Action(action).result()
        processor.process_command(a)
        return m.shapes[0]
