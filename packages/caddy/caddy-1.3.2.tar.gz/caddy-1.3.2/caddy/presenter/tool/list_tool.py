from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class ListTool(BaseTool):
    INDICATOR = '[List] Click to list all intersecting shapes'

    def canvas_click(self, context, point: Point):
        context.model.list(point)
