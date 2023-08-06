import sys
from typing import Tuple

from caddy.cli.lang.parser import Action
from caddy.cli.processor import Processor, ProcessorEvent
from caddy.model.actions import ActionInterface
from caddy.model.model import ModelObserver
from caddy.model.model_interface import ModelInterface
from caddy.model.shape import Shape
from caddy.presenter.file_reader import FileReader, ParseError
from caddy.presenter.file_writer import FileWriter, WriteError
from caddy.presenter.tool_context import ToolContext
from caddy.presenter.visitor.drawing_visitor import DrawingVisitor
from caddy.presenter.visitor.persistence_visitor import PersistenceVisitor
from caddy.shared.point import Point
from caddy.view.button_interface import ButtonInterface
from caddy.view.canvas_interface import CanvasInterface
from caddy.view.cli_interface import CLIInterface
from caddy.view.menu_interface import MenuInterface


class Presenter(ModelObserver):
    def __init__(self, model: ModelInterface,
                 components: Tuple[MenuInterface, ButtonInterface, CanvasInterface, CLIInterface]) -> None:
        super().__init__()
        self.model = model
        self.cli_processor = Processor(model)
        self.main_menu, self.button_menu, self.canvas, self.cli = components
        self.drawing_visitor = DrawingVisitor(self.canvas)
        self.cli_visitor = PersistenceVisitor(self.cli)
        self.context: ToolContext = ToolContext(self.model, self.canvas)

        # Register as a model observer
        model.attach_observer(self)

        # Register itself to button events
        btn_event_handlers = {
            ButtonInterface.ButtonEvents.CURSOR: self.context.tool_cursor,
            ButtonInterface.ButtonEvents.MOVE: self.context.tool_move,
            ButtonInterface.ButtonEvents.REMOVE: self.context.tool_remove,
            ButtonInterface.ButtonEvents.POLYLINE: self.context.tool_add_line,
            ButtonInterface.ButtonEvents.RECTANGLE: self.context.tool_add_rectangle,
            ButtonInterface.ButtonEvents.CIRCLE: self.context.tool_add_circle,
            ButtonInterface.ButtonEvents.LIST: self.context.tool_list
        }
        for event, function in btn_event_handlers.items():
            self.button_menu.register_button_handler(event, function)

        # Register itself to main menu events
        menu_event_handlers = {
            MenuInterface.MenuEvents.NEW: self.on_new_file,
            MenuInterface.MenuEvents.LOAD: self.on_file_load,
            MenuInterface.MenuEvents.SAVEAS: self.on_file_save,
            MenuInterface.MenuEvents.EXIT: sys.exit
        }
        for event, function in menu_event_handlers.items():
            self.main_menu.register_menu_handler(event, function)

        processor_event_handlers = {
            ProcessorEvent.SAVE: self.on_file_save,
            ProcessorEvent.LOAD: self.on_file_load,
            ProcessorEvent.QUIT: lambda _: sys.exit(),
            ProcessorEvent.CLEAR: lambda _: self.on_new_file()
        }
        for event, function in processor_event_handlers.items():
            self.cli_processor.register_handler(event, function)

        # Register itself to canvas click events
        self.canvas.register_canvas_click_handler(lambda coord: self.context.canvas_click(Point(coord[0], coord[1])))

        # Register itself to CLI entry events
        self.cli.register_entry_handler(self.on_cli_command)

    def on_model_changed(self):
        self.canvas.canvas_clear()
        self.model.accept_visitor(self.drawing_visitor)

    def on_shape_added(self, shape: Shape, effective: bool):
        self.on_model_changed()
        effective and shape.accept_visitor(self.cli_visitor)

    def on_action(self, action: ActionInterface, visible: bool):
        visible and self.on_model_changed()
        action.accept_visitor(self.cli_visitor)

    def on_new_file(self):
        self.context.tool_cursor()
        self.cli.cli_clear()
        self.model.clear()

    def on_file_save(self, path: str):
        self.cli.add_text_command('save ' + path)
        try:
            file_writer = FileWriter(path)
        except WriteError as e:
            self.cli.add_text(e.args[0])
            return
        self.context.file_save(path)
        persistence_visitor = PersistenceVisitor(file_writer)
        self.model.accept_visitor(persistence_visitor)
        file_writer.close()

    def on_file_load(self, path: str):
        self.model.clear()
        self.cli.cli_clear()
        self.cli.add_text_command('load ' + path)
        reader = FileReader(path, self.cli_processor)
        try:
            reader.validate()
        except ParseError as e:
            self.cli.add_text(e.args[0])
            return
        self.context.file_load(path)
        reader.load()

    def on_cli_command(self, command: str):
        parse_result = Action(command)
        if not parse_result.is_accepted():
            self.cli.add_text_command(command)
            self.cli.add_text("Syntax Error, please try again")
            return
        self.cli_processor.process_command(parse_result.result())
