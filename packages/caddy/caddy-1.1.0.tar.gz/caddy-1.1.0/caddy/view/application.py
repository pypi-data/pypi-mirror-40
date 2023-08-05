import tkinter as tk

from caddy.view.canvas import CanvasFrame
from caddy.view.cli import CLIFrame
from caddy.view.buttons import ButtonFrame
from caddy.view.menu import Menu

from caddy.view.application_interface import ApplicationInterface


class Application(tk.Frame, ApplicationInterface):

    def __init__(self, master=None, canvas_width: int = 740, canvas_height: int = 380):
        super().__init__(master)

        self.canvas = None
        self.cli = None
        self.button_menu = None
        self.main_menu = None
        self._title = "Caddy"
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self._geometry = str(self.canvas_width + 60) + "x" + str(self.canvas_height + 230)

        self.master = master
        self.application_main_config()
        self.application_widgets_config()

        # Handle window close event
        master.protocol("WM_DELETE_WINDOW", self.main_menu.handle_menu_click_exit)

    # ----- VIEW SETUP  ------------------------------------------------------------------------------------------------

    def application_main_config(self):
        self.master.title(self._title)
        self.master.geometry(self._geometry)
        self.master.resizable(width=False, height=False)
        self.pack()

    def application_widgets_config(self):
        main_menu = tk.Menu(self.master, relief=tk.FLAT)
        self.main_menu = Menu(main_menu)
        self.master.config(menu=main_menu)
        main_menu.bind('<Button-1>', self.entry_unfocus)

        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        button_frame.bind('<Button-1>', self.entry_unfocus)
        self.button_menu = ButtonFrame(button_frame)

        layout_frame = tk.Frame(self.master)
        layout_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        canvas_frame = tk.Frame(layout_frame)
        canvas_frame.pack(side=tk.TOP)
        self.canvas = CanvasFrame(canvas_frame, canvas_width=self.canvas_width, canvas_height=self.canvas_height)

        cli_frame = tk.Frame(layout_frame)
        cli_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.cli = CLIFrame(cli_frame)

    # ----- CLICKS AND EVENTS HANDLERS ---------------------------------------------------------------------------------

    def entry_unfocus(self, _=None):
        self.master.focus()

    # ----- APPLICATION MANIPULATION -----------------------------------------------------------------------------------

    def close_app(self):
        self.master.quit()

    def get_components(self):
        return self.main_menu, self.button_menu, self.canvas, self.cli
