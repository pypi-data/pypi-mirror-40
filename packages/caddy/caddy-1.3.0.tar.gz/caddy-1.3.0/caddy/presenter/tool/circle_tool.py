from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class CircleTool(BaseTool):
    INDICATOR = '[Circle] Click to specify the center of a circle'

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.circle_stage_tool)


class CircleStageTool(BaseTool):
    INDICATOR = '[Circle] Click to specify the radius of the circle'

    def canvas_click(self, context, point: Point):
        center = context.points[0]
        radius = round((center.dist_from(point)))
        context.model.add_circle(center, radius)

        context.clear()
        context.set_tool(context.circle_tool)
