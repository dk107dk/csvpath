from typing import Any
from .function import Function
from ..productions import ChildrenException


class Concat(Function):
    def check_valid(self) -> None:
        self.validate_two_or_more_args()
        super().check_valid()

    def to_value(self, *, skip=[]) -> Any:
        if self in skip:  # pragma: no cover
            return self._noop_value()
        if self.value is None:
            child = self.children[0]
            siblings = child.commas_to_list()
            v = ""
            for s in siblings:
                v = f"{v}{s.to_value(skip=skip)}"
            self.value = v
        return self.value

    def matches(self, *, skip=[]) -> bool:
        self.to_value(skip=skip)  # pragma: no cover
        return self._noop_match()
