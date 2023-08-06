from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class EraserTool(BaseTool):
    INDICATOR = '[Eraser] Click to select intersecting shapes to delete'

    def canvas_click(self, context, point: Point):
        context.model.remove_overlapping_with(point)
