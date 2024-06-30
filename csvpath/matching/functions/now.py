from typing import Any
from csvpath.matching.functions.function import Function, ChildrenException
import datetime

class Now(Function):

    def to_value(self) -> Any:
        if len(self.children) > 1:
            self.matcher.print(f"Now.to_value: should be 0 or 1 children: {self.children}")
            ChildrenException("now function may have only a single child that gives a format")
        format = None
        if self.children and len(self.children) == 1:
            format = self.children[0].to_value()
            self.matcher.print(f"Now.to_value: format: {format}")
        x = datetime.datetime.now()
        self.matcher.print(f"Now.to_value: x: {x}")
        xs = None
        if format:
            xs = x.strftime(format)
            self.matcher.print(f"Now.to_value: format: {format}, xs: {xs}")
        else:
            xs = f"{x}"
        self.matcher.print(f"Now.to_value: returning: {xs}")
        return xs

    def matches(self) -> bool:
        return True # always matches because not internally matchable




