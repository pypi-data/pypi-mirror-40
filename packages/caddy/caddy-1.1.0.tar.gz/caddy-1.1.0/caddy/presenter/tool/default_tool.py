from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class DefaultTool(BaseTool):
    INDICATOR = '[Cursor]'

    def canvas_click(self, context, point: Point):
        pass
