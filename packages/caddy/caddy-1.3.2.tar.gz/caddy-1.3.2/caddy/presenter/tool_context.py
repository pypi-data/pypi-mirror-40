from typing import List

from caddy.model.model_interface import ModelInterface
from caddy.presenter.tool.base_tool import BaseTool
from caddy.presenter.tool.circle_tool import CircleTool, CircleStageTool
from caddy.presenter.tool.default_tool import DefaultTool
from caddy.presenter.tool.eraser_tool import EraserTool
from caddy.presenter.tool.line_tool import LineTool, LineStageTool, LineSegmentTool
from caddy.presenter.tool.list_tool import ListTool
from caddy.presenter.tool.move_tool import MoveTool, MoveStageTool
from caddy.presenter.tool.rectangle_tool import RectangleTool, RectangleStageTool
from caddy.shared.point import Point
from caddy.view.canvas_interface import CanvasInterface


class ToolContext:
    # Class attributes containing instances of all possible states/tool
    default_tool = DefaultTool()
    line_tool = LineTool()
    line_stage_tool = LineStageTool()
    line_segment_tool = LineSegmentTool()
    rectangle_tool = RectangleTool()
    rectangle_stage_tool = RectangleStageTool()
    circle_tool = CircleTool()
    circle_stage_tool = CircleStageTool()
    move_tool = MoveTool()
    move_stage_tool = MoveStageTool()
    eraser_tool = EraserTool()
    list_tool = ListTool()

    def __init__(self, model: ModelInterface, view: CanvasInterface):
        self._current_tool: BaseTool = None
        self.points: List[Point] = []
        self.model = model
        self.view = view

        self.set_tool(self.default_tool)

    def set_tool(self, state: BaseTool):
        self._current_tool = state
        self.view.set_state_indicator(state.INDICATOR)

    def clear(self):
        self.points.clear()

    def file_save(self, path: str):
        self._current_tool.tool_cursor(self)
        self.view.set_state_indicator("[Cursor] Saved " + path)

    def file_load(self, path: str):
        self._current_tool.tool_cursor(self)
        self.view.set_state_indicator("[Cursor] Loaded " + path)

    def canvas_click(self, point: Point):
        self._current_tool.canvas_click(self, point)

    def tool_cursor(self):
        self._current_tool.tool_cursor(self)

    def tool_move(self):
        self._current_tool.tool_move(self)

    def tool_remove(self):
        self._current_tool.tool_remove(self)

    def tool_list(self):
        self._current_tool.tool_list(self)

    def tool_add_line(self):
        self._current_tool.tool_add_line(self)

    def tool_add_rectangle(self):
        self._current_tool.tool_add_rectangle(self)

    def tool_add_circle(self):
        self._current_tool.tool_add_circle(self)
