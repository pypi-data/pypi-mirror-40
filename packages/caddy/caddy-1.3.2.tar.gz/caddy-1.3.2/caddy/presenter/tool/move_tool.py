from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class MoveTool(BaseTool):
    INDICATOR = '[Move] Click to select intersecting shapes to move.'

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.move_stage_tool)


class MoveStageTool(BaseTool):
    INDICATOR = '[Move] Click to move the selection'

    def canvas_click(self, context, point: Point):
        overlapping = context.points[0]
        context.model.move_by(overlapping, point - overlapping)

        context.clear()
        context.set_tool(context.move_tool)
