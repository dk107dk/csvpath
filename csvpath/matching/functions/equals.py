# pylint: disable=C0114
from typing import Any
from .function import Function


class Equals(Function):
    """tests the equality of two values"""

    def check_valid(self) -> None:
        self.validate_two_args()
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        child = self.children[0]
        ret = False
        left = child.left.to_value()
        right = child.right.to_value()
        if (left and not right) or (right and not left):
            ret = False
        elif left is None and right is None:
            ret = True
        elif self._is_float(left) and self._is_float(right):
            ret = float(left) == float(right)
        elif f"{left}" == f"{right}":
            ret = True
        else:
            ret = False
        self.value = ret

    def matches(self, *, skip=None) -> bool:
        return self._noop_match()  # pragma: no cover

    def _is_float(self, fs) -> bool:
        try:
            float(fs)
        except (OverflowError, ValueError):
            return False
        return True
