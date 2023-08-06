from caddy.cli.lang.points import AbsolutePoint, RelativePoint
import caddy.cli.parsing.parsers as parsers
from caddy.cli.parsing.parsers import ws_after

# Essentially a rewrite of the grammar specified in the sample repo

String = parsers.Regex("[^ ]+")
Whitespace = parsers.Regex("\\s+")
Natural = parsers.Regex("\\d+").map(int)
Integer = parsers.Regex("[+-]\\d+").map(int)

AbsPoint = ((Natural << parsers.String(",")) + Natural).map(lambda coords: AbsolutePoint(coords[0], coords[1]))
RelPoint = ((Integer << parsers.String(",")) + Integer).map(lambda coords: RelativePoint(coords[0], coords[1]))
Point = AbsPoint | RelPoint

PointPair = (ws_after(Point) + Point).map(lambda points: (points[0], points[1]))

Line = (ws_after(parsers.String("line")) + ws_after(Point) + ws_after(Point) + Point.iterate(Whitespace)) |\
       (ws_after(parsers.String("line")) + ws_after(Point) + Point)

Rect = (ws_after(parsers.String("rect")) + PointPair) |\
       (ws_after(parsers.String("rect")) + ws_after(Point) + ws_after(Natural) + Natural)

Circle = (ws_after(parsers.String("circle")) + PointPair) |\
         (ws_after(parsers.String("circle")) + ws_after(Point) + Natural)

Save = ws_after(parsers.String("save")) + String
Load = ws_after(parsers.String("load")) + String

Remove = ws_after(parsers.String("remove")) + Point
Move = ws_after(parsers.String("move")) + PointPair

Ls = (ws_after(parsers.String("ls")) + AbsPoint) |\
      parsers.String("ls").map(lambda _: ["ls"])

Clear = parsers.String("clear").map(lambda _: ["clear"])
Quit = parsers.String("quit").map(lambda _: ["quit"])

Action = Line |\
         Rect |\
         Circle |\
         Save |\
         Load |\
         Remove |\
         Move |\
         Ls |\
         Clear |\
         Quit
