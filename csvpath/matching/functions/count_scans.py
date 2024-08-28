from typing import Any
from .function import Function


class CountScans(Function):
    def check_valid(self) -> None:
        self.validate_zero_args()
        super().check_valid()

    def to_value(self, *, skip=[]) -> Any:
        if self in skip:
            return self._noop_value()
        return self.matcher.csvpath.current_scan_count
