from caddy.shared.command_interface import CommandInterface


class FileWriter(CommandInterface):

    def __init__(self, path) -> None:
        self.stream = open(path, 'w')

    def add_text_command(self, command: str, command_result: str = ""):
        self.stream.write(command + '\n')

    def close(self):
        self.stream.close()
