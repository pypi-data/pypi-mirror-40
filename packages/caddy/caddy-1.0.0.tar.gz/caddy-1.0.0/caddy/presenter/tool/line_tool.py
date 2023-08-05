from caddy.presenter.tool.base_tool import BaseTool
from caddy.shared.point import Point


class LineTool(BaseTool):
    INDICATOR = '[Polyline] Click to specify the starting point of a polyline'

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.set_tool(context.line_stage_tool)


class LineStageTool(BaseTool):
    INDICATOR = '[Polyline] Click to draw the first line segment'

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.recent_object = context.model.add_polyline(context.points)
        context.set_tool(context.line_segment_tool)


class LineSegmentTool(BaseTool):
    INDICATOR = '[Polyline] Click to draw another line segment'

    def tool_cursor(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_cursor(context)

    def tool_move(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_move(context)

    def tool_remove(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_remove(context)

    def tool_add_line(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_add_line(context)

    def tool_add_rectangle(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_add_rectangle(context)

    def tool_add_circle(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_add_circle(context)

    def tool_list(self, context):
        context.recent_object.accept_visitor(context.visitor)
        super().tool_list(context)

    def canvas_click(self, context, point: Point):
        context.points.append(point)
        context.model.remove_by_id(context.recent_object.shape_id)
        context.recent_object = context.model.add_polyline(context.points)
