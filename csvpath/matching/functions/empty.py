# pylint: disable=C0114
from .function import Function
from ..productions import Header, Variable
from ..util.expression_utility import ExpressionUtility

# note to self: should be possible to request a check of all
# headers.


class Empty(Function):
    """checks for empty or blank header values in a given line"""

    def check_valid(self) -> None:
        self.validate_one_arg([Header, Variable])
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        self.value = self.matches(skip=skip)

    def matches(self, *, skip=None) -> bool:
        if skip and self in skip:  # pragma: no cover
            return self._noop_match()
        if self.match is None:
            v = self.children[0].to_value()
            ab = self.children[0].asbool
            if ab:
                v = ExpressionUtility.asbool(v)
                self.match = v
            elif v is None:
                self.match = True
            elif isinstance(v, list) and len(v) == 0:
                self.match = True
            elif isinstance(v, dict) and len(dict) == 0:
                self.match = True
            elif isinstance(v, tuple) and len(v) == 0:
                self.match = True
            elif isinstance(v, str) and v.strip() == "":
                self.match = True
            else:
                self.match = False
        return self.match
