from abc import ABC, abstractmethod
import sys
from .config_exception import ConfigurationException


class Printer(ABC):
    ERROR = "stderr"
    DEFAULT = "default"

    @property
    @abstractmethod
    def last_line(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def lines_printed(self) -> int:
        pass  # pragma: no cover

    @abstractmethod
    def print(self, string: str) -> None:
        """prints string with a newline. same as print_to(None, string)."""
        pass  # pragma: no cover

    @abstractmethod
    def print_to(self, name: str, string: str) -> None:
        """name is a file, stream, or string collection indicator.
        string is the value to be printed/stored with the addition
        of a newline."""
        pass  # pragma: no cover


class StdOutPrinter(Printer):
    def __init__(self):
        self._last_line = None
        self._count = 0

    @property
    def lines_printed(self) -> int:
        return self._count

    @property
    def last_line(self) -> str:
        return self._last_line

    def print(self, string: str) -> None:
        self.print_to(None, string)

    def print_to(self, name: str, string: str) -> None:
        self._count += 1
        if name == Printer.ERROR:
            print(string, file=sys.stderr)  # pragma: no cover
        elif name:
            print(string, file=name)  # pragma: no cover
        else:
            print(string)
        self._last_line = string


class TestPrinter(Printer):
    __test__ = False

    def __init__(self):
        self.lines = []

    @property
    def lines_printed(self) -> int:
        return len(self.lines)

    @property
    def last_line(self) -> str:
        return self.lines[len(self.lines) - 1] if len(self.lines) > 0 else ""

    def print(self, string: str) -> None:
        self.print_to(None, string)

    def print_to(self, name: str, string: str) -> None:
        self.lines.append(string)


class LogPrinter(StdOutPrinter):
    """logs to info by default"""

    def __init__(self, logger):
        self._logger = logger
        if logger is None:
            raise ConfigurationException("Logger cannot be None")
        super().__init__()

    def print_to(self, name: str, msg: str) -> None:
        self._count += 1
        if name in ["info", None]:
            self._logger.info(msg)
        elif name == "debug":
            self._logger.debug(msg)
        elif name in ["warn", "warning"]:
            self._logger.warning(msg)
        elif name == "error":
            self._logger.error(msg)
        else:
            self._logger.info(msg)

        self._last_line = msg
