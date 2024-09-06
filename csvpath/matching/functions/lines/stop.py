# pylint: disable=C0114
from typing import Any
from ..function_focus import SideEffect


class Stop(SideEffect):
    """when called halts the scan. the current row will be returned."""

    def check_valid(self) -> None:
        self.validate_zero_or_more_args()
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        self.value = self.matches(skip=skip)

    def matches(self, *, skip=None) -> bool:
        if skip and self in skip:  # pragma: no cover
            return False
        if self.match is None:
            self.match = True
            stopped = False
            if len(self.children) == 1:
                b = self.children[0].matches(skip=skip)
                if b is True:
                    self.matcher.csvpath.stop()
                    pln = self.matcher.csvpath.line_monitor.physical_line_number
                    self.matcher.csvpath.logger.info(
                        f"stopping at {pln}. contained child matches."
                    )
                    stopped = True
            else:
                self.matcher.csvpath.stop()
                pln = self.matcher.csvpath.line_monitor.physical_line_number
                self.matcher.csvpath.logger.info(f"stopping at {pln}")
                stopped = True
            if stopped and self.name == "fail_and_stop":
                self.matcher.csvpath.logger.info("setting invalid")
                self.matcher.csvpath.is_valid = False
        return self.match


class Skip(SideEffect):
    """skips to the next line. will probably leave later match components
    unconsidered; although, there is not certainty that will happen."""

    def check_valid(self) -> None:
        self.validate_zero_or_more_args()
        super().check_valid()

    def to_value(self, *, skip=None) -> Any:
        return self.matches(skip=skip)

    def matches(self, *, skip=None) -> bool:  # pylint: disable=R1702
        # re: R1702: we need to rethink matches() along the lines
        # of _produce_value(). this gets fixed then.
        if skip and self in skip:  # pragma: no cover
            return False
        if self.match is None:  # pylint: disable=R1702
            if self.do_onmatch():
                if self.do_once():
                    if len(self.children) == 1:
                        b = self.children[0].matches(skip=skip)
                        if b is True:
                            self.matcher.skip = True
                            if self.once:
                                self._set_has_happened()
                            pln = self.matcher.csvpath.line_monitor.physical_line_number
                            self.matcher.csvpath.logger.info(
                                f"skipping physical line {pln}. contained child matches."
                            )
                    else:
                        self.matcher.skip = True
                        if self.once:
                            self._set_has_happened()
                        pln = self.matcher.csvpath.line_monitor.physical_line_number
                        self.matcher.csvpath.logger.info(f"skipping line {pln}")
            self.match = True
        return self.match
