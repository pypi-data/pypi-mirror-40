from caddy.cli.lang.parser import Action
from caddy.cli.processor import Processor


class ParseError(Exception):
    pass


class FileReader:
    def __init__(self, path: str, processor: Processor):
        self.processor = processor
        self.path = path
        self.lines = None
        self.results = None

    def load(self):
        self.validate()
        for result in self.results:
            self.processor.process_command(result.result())

    def validate(self):
        if self.lines is None:
            self.read_lines()
        self.results = list(map(Action, self.lines))
        for line, result in enumerate(self.results):
            if not result.is_accepted():
                raise ParseError(f"Syntax error on line {line + 1}")
        return True

    def read_lines(self):
        try:
            with open(self.path, "r") as f:
                self.lines = list(map(lambda s: s.strip(), f.readlines()))
        except FileNotFoundError:
            raise ParseError('File "%s" does not exist' % self.path)
        except PermissionError:
            raise ParseError('Permission denied')
