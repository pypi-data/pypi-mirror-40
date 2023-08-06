from caddy.shared.command_interface import CommandInterface


class WriteError(Exception):
    pass


class FileWriter(CommandInterface):

    def __init__(self, path) -> None:
        try:
            self.stream = open(path, 'w')
        except IOError:
            raise WriteError('Unable to write to file "%s"' % path)

    def add_text_command(self, command: str):
        self.stream.write(command + '\n')

    def add_text(self, text: str):
        pass

    def close(self):
        self.stream.close()
