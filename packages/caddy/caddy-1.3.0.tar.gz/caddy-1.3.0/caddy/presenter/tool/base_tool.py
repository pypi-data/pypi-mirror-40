from __future__ import annotations
from abc import ABC, abstractmethod
import typing

from caddy.shared.point import Point

if typing.TYPE_CHECKING:
    from caddy.presenter.tool_context import ToolContext


class BaseTool(ABC):
    INDICATOR = ''

    def tool_cursor(self, context: ToolContext):
        context.clear()
        context.set_tool(context.default_tool)

    def tool_move(self, context: ToolContext):
        context.clear()
        context.set_tool(context.move_tool)

    def tool_remove(self, context: ToolContext):
        context.clear()
        context.set_tool(context.eraser_tool)

    def tool_add_line(self, context: ToolContext):
        context.clear()
        context.set_tool(context.line_tool)

    def tool_add_rectangle(self, context: ToolContext):
        context.clear()
        context.set_tool(context.rectangle_tool)

    def tool_add_circle(self, context: ToolContext):
        context.clear()
        context.set_tool(context.circle_tool)

    def tool_list(self, context: ToolContext):
        context.clear()
        context.set_tool(context.list_tool)

    @abstractmethod
    def canvas_click(self, context: ToolContext, point: Point):
        raise NotImplementedError
