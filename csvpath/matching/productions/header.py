from typing import Any
from .matchable import Matchable
from ..util.expression_utility import ExpressionUtility


class Header(Matchable):
    NEVER = -9999999999

    def __str__(self) -> str:
        return f"""{self._simple_class_name()}({self.name}) """

    def __init__(self, matcher, *, value: Any = None, name: str = None) -> None:
        # header names can be quoted like "Last Year Number"
        if isinstance(name, str):
            name = name.strip()
            if name[0] == '"' and name[len(name) - 1] == '"':
                name = name[1 : len(name) - 1]
        super().__init__(matcher, value=Header.NEVER, name=name)

    def reset(self) -> None:
        self.value = Header.NEVER
        self.match = None
        super().reset()

    def to_value(self, *, skip=[]) -> Any:
        if self in skip:
            return self.value
        if self.value == Header.NEVER:
            ret = Header.NEVER
            if isinstance(self.name, int) or self.name.isdecimal():
                if int(self.name) >= len(self.matcher.line):
                    ret = None
                else:
                    ret = self.matcher.line[int(self.name)]
            else:
                n = self.matcher.header_index(self.name)
                if n is None:
                    ret = None
                elif self.matcher.line and len(self.matcher.line) > n:
                    ret = self.matcher.line[n]
                else:
                    self.matcher.csvpath.logger.debug(
                        f"Header.to_value: miss because n >= {len(self.matcher.line)}"
                    )
            if self.asbool:
                self.value = ExpressionUtility.asbool(ret)
            else:
                self.value = ret
        return self.value

    def matches(self, *, skip=[]) -> bool:
        if self.match is None:
            v = self.to_value(skip=skip)
            if self.asbool:
                v = self.to_value(skip=skip)
                self.match = ExpressionUtility.asbool(v)
            else:
                self.match = v is not None
        return self.match
