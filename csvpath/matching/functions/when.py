from typing import Any
from csvpath.matching.functions.function import Function, ChildrenException
from csvpath.matching.productions.equality import Equality


class When(Function):
    def to_value(self, *, skip=[]) -> Any:
        return True

    def matches(self, *, skip=[]) -> bool:
        if self in skip:
            return True
        if len(self.children) != 1:
            raise ChildrenException("must be 1 equality child")
        if not isinstance(self.children[0], Equality):
            raise ChildrenException(
                "must be 1 equality child with a match and an action"
            )
        if self.match is None:
            if self.children[0].left.matches(skip=skip):
                self.children[0].right.matches(
                    skip=skip
                )  # we activate this side, but do nothing with it.
            self.match = True
        return self.match
