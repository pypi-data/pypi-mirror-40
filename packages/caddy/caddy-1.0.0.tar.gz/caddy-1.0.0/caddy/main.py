import tkinter as tk

from caddy.model.model import Model
from caddy.presenter.presenter import Presenter
from caddy.view.application import Application


def main():
    root = tk.Tk()
    app = Application(master=root)

    model = Model()
    Presenter(model, app.get_components())

    app.mainloop()


if __name__ == '__main__':  # pragma: no cover
    main()
