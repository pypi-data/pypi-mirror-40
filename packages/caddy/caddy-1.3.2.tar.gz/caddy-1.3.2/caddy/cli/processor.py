from enum import Enum
from typing import Dict, List, Callable
from caddy.model.model import ModelInterface
from caddy.shared.point import Point


class ProcessorEvent(Enum):
    SAVE = "save"
    LOAD = "load"
    QUIT = "quit"
    CLEAR = "clear"


class Processor:
    def __init__(self, model: ModelInterface):
        self.model = model
        self.method_map = {
            "line": self.line,
            "rect": self.rect,
            "circle": self.circle,
            "save": self.save,
            "load": self.load,
            "remove": self.remove,
            "move": self.move,
            "ls": self.ls,
            "clear": self.clear,
            "quit": self.quit
        }
        self.event_handlers: Dict[ProcessorEvent, List[Callable]] = {}

    def process_command(self, parsed_cmd):
        return self.method_map[parsed_cmd[0]](parsed_cmd)

    def register_handler(self, event: ProcessorEvent, action: Callable):
        if event not in self.event_handlers:
            self.event_handlers[event] = [action]
        else:
            self.event_handlers[event].append(action)

    def line(self, cmd):
        points = [
            cmd[1].as_absolute(None),
            cmd[2].as_absolute(cmd[1])
        ]
        if len(cmd) == 4:
            for p in cmd[3]:
                points.append(p.as_absolute(points[-1]))
        return self.model.add_polyline(points)

    def rect(self, cmd):
        if len(cmd) == 2:
            return self.point_rect(cmd)
        return self.dimensions_rect(cmd)

    def point_rect(self, cmd):
        assert len(cmd) == 2
        points = cmd[1]
        return self.model.add_rectangle(
            points[0].as_absolute(None),
            points[1].as_absolute(points[0]))

    def dimensions_rect(self, cmd):
        assert len(cmd) == 4
        start_point = cmd[1].as_absolute(None)
        additional_point = start_point + Point(cmd[2], -cmd[3])
        return self.model.add_rectangle(start_point, additional_point)

    def circle(self, cmd):
        if len(cmd) == 2:
            return self.endpoint_circle(cmd)
        return self.radius_circle(cmd)

    def radius_circle(self, cmd):
        assert len(cmd) == 3
        return self.model.add_circle(cmd[1].as_absolute(None), cmd[2])

    def endpoint_circle(self, cmd):
        assert len(cmd) == 2
        points = cmd[1]
        point_sum = points[0] + points[1]
        center = Point(point_sum.x/2, point_sum.y/2)
        radius = round(center.dist_from(points[0]))
        return self.model.add_circle(center, radius)

    def save(self, cmd):
        self._call_event_handlers(ProcessorEvent.SAVE, cmd[1])

    def load(self, cmd):
        self._call_event_handlers(ProcessorEvent.LOAD, cmd[1])

    def remove(self, cmd):
        self.model.remove_overlapping_with(cmd[1].as_absolute(None))

    def move(self, cmd):
        points = cmd[1]
        self.model.move_by(points[0].as_absolute(None),
                           points[1].as_relative(points[0]))

    def ls(self, cmd):
        argument = None
        if len(cmd) == 2:
            argument = cmd[1].as_absolute(None)
        self.model.list(argument)

    def clear(self, _):
        self._call_event_handlers(ProcessorEvent.CLEAR, None)

    def quit(self, _):
        self._call_event_handlers(ProcessorEvent.QUIT, None)

    def _call_event_handlers(self, event: ProcessorEvent, argument):
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                handler(argument)
