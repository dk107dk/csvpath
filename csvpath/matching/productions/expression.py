# pylint: disable=C0114
import traceback
import warnings
from csvpath.util.error import ErrorHandler
from . import Matchable


class Expression(Matchable):
    """root of a match component. the match components are expressions,
    even if we think of them as variables, headers, etc. expressions
    live in a list in the matcher. matcher tracks their activation
    status (True/False) to minimize the number of activations during
    onmatch lookups. expressions' most important job is error
    handling. the expression is responsible for catching and
    handling any error in its descendants.
    """

    def matches(self, *, skip=None) -> bool:
        if skip and self in skip:
            return True
        if self.match is None:
            try:
                ret = True
                for child in self.children:
                    if not child.matches(skip=skip):
                        ret = False
                self.match = ret
            except Exception as e:
                e.trace = traceback.format_exc()
                e.source = self
                e.json = self.matcher.to_json(self)
                ErrorHandler(
                    csvpath=self.matcher.csvpath,
                    logger=self.matcher.csvpath.logger,
                    error_collector=self.matcher.csvpath,
                    component="csvpath",
                ).handle_error(e)
        return self.match

    def reset(self) -> None:
        self.value = None
        self.match = None
        super().reset()

    def check_valid(self) -> None:
        warnings.filterwarnings("error")
        try:
            super().check_valid()
        except Exception as e:
            e.trace = traceback.format_exc()
            e.source = self
            e.message = f"Failed csvpath validity check with: {e}"
            e.json = self.matcher.to_json(self)
            ErrorHandler(
                logger=self.matcher.csvpath.logger,
                error_collector=self.matcher.csvpath,
                component="csvpath",
            ).handle_error(e)
            #
            # We always stop if the csvpath itself is found to be invalid
            # before the run starts. The error policy doesn't override that.
            #
            self.matcher.stopped = True
