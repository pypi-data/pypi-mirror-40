from abc import abstractmethod, ABC


class CommandInterface(ABC):

    @abstractmethod
    def add_text_command(self, command: str):
        raise NotImplementedError()

    @abstractmethod
    def add_text(self, text: str):
        raise NotImplementedError()
