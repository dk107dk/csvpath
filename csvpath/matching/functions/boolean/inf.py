# pylint: disable=C0114
from typing import Any
from ..function_focus import MatchDecider
from csvpath.matching.productions import Term, Variable, Header, Reference
from ..function import Function
from ..args import Args


class In(MatchDecider):
    """checks if the component value is in the values of the other N arguments.
    terms are treated as | delimited strings of values"""

    def check_valid(self) -> None:
        self.args = Args(matchable=self)
        a = self.args.argset()
        a.arg(types=[Term, Variable, Header, Function, Reference], actuals=[Any])
        a.arg(types=[Term, Variable, Header, Function, Reference], actuals=[Any])
        self.args.validate(self.siblings())
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        self.value = self.matches(skip=skip)

    def _decide_match(self, skip=None) -> None:
        siblings = self.children[0].commas_to_list()
        t = siblings[0].to_value(skip=skip)
        inf = []
        for s in siblings[1:]:
            v = s.to_value(skip=skip)
            if isinstance(s, Term):
                vs = f"{v}".split("|")
                inf += vs
            else:
                # tuple would mean vars were frozen. this would not be
                # surprising from a reference
                if isinstance(v, list) or isinstance(v, tuple):
                    for _ in v:
                        inf.append(_)
                elif isinstance(v, dict):
                    for k in v:
                        inf.append(k)
                else:
                    inf.append(v)
        self.match = t in inf
