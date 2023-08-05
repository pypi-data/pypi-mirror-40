from abc import abstractmethod, ABC


class CommandInterface(ABC):

    @abstractmethod
    def add_text_command(self, command: str, command_result: str = ""):
        raise NotImplementedError()
