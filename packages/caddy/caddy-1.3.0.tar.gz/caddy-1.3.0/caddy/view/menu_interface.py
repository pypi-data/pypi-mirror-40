from typing import Callable
from abc import abstractmethod, ABC
from enum import Enum


class MenuInterface(ABC):
    class MenuEvents(Enum):
        NEW = "new"
        LOAD = "load"
        SAVEAS = "save as"
        EXIT = "exit"

    @abstractmethod
    def register_menu_handler(self, menu_event: MenuEvents, command: Callable):
        raise NotImplementedError()
