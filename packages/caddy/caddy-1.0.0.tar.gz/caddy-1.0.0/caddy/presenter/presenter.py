import sys
from typing import Tuple

from caddy.model.model import Model, ModelObserver
from caddy.presenter.file_writer import FileWriter
from caddy.presenter.tool_context import ToolContext
from caddy.presenter.visitor.drawing_visitor import DrawingVisitor
from caddy.presenter.visitor.persistence_visitor import PersistenceVisitor
from caddy.shared.point import Point
from caddy.view.button_interface import ButtonInterface
from caddy.view.canvas_interface import CanvasInterface
from caddy.view.cli_interface import CLIInterface
from caddy.view.menu_interface import MenuInterface


class Presenter(ModelObserver):
    def __init__(self, model: Model,
                 components: Tuple[MenuInterface, ButtonInterface, CanvasInterface, CLIInterface]) -> None:
        super().__init__()
        self.model: Model = model
        self.main_menu, self.button_menu, self.canvas, self.cli = components
        self.drawing_visitor = DrawingVisitor(self.canvas)
        self.cli_visitor = PersistenceVisitor(self.cli)
        self.context: ToolContext = ToolContext(self.model, self.canvas, self.cli_visitor)

        # Register as a model observer
        model.attach_observer(self)

        # Register itself to button events
        btn_event_handlers = {
            ButtonInterface.ButtonEvents.CURSOR: lambda: self.context.tool_cursor(),
            ButtonInterface.ButtonEvents.MOVE: lambda: self.context.tool_move(),
            ButtonInterface.ButtonEvents.REMOVE: lambda: self.context.tool_remove(),
            ButtonInterface.ButtonEvents.POLYLINE: lambda: self.context.tool_add_line(),
            ButtonInterface.ButtonEvents.RECTANGLE: lambda: self.context.tool_add_rectangle(),
            ButtonInterface.ButtonEvents.CIRCLE: lambda: self.context.tool_add_circle(),
            ButtonInterface.ButtonEvents.LIST: lambda: self.context.tool_list()
        }
        for event, function in btn_event_handlers.items():
            self.button_menu.register_button_handler(event, function)

        # Register itself to main menu events
        menu_event_handlers = {
            MenuInterface.MenuEvents.NEW: lambda: self.on_new_file(),
            MenuInterface.MenuEvents.LOAD: lambda x: print("Clicked on load:", x),
            MenuInterface.MenuEvents.SAVEAS: lambda x: self.on_file_save(x),
            MenuInterface.MenuEvents.EXIT: lambda: sys.exit()
        }
        for event, function in menu_event_handlers.items():
            self.main_menu.register_menu_handler(event, function)

        # Register itself to canvas click events
        self.canvas.register_canvas_click_handler(lambda coord: self.context.canvas_click(Point(coord[0], coord[1])))

        # Register itself to CLI entry events
        self.cli.register_entry_handler(lambda txt: self.cli.add_text_command(txt))

    def on_model_changed(self):
        self.canvas.canvas_clear()
        self.model.accept_visitor(self.drawing_visitor)

    def on_new_file(self):
        self.context.tool_cursor()
        self.model.clear()
        self.cli.cli_clear()

    def on_file_save(self, path: str):
        self.context.file_save(path)
        file_writer = FileWriter(path)
        persistence_visitor = PersistenceVisitor(file_writer)
        self.model.accept_visitor(persistence_visitor)
        file_writer.close()
