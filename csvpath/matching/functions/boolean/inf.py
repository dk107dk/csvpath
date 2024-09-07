# pylint: disable=C0114
from ..function_focus import MatchDecider


class In(MatchDecider):
    """checks if the component value is in a delimited string of values"""

    def check_valid(self) -> None:
        self.validate_two_args()
        super().check_valid()

    def _produce_value(self, skip=None) -> None:
        #
        # TODO: make do in on match components, not just string
        #
        vchild = self.children[0].children[0]
        lchild = self.children[0].children[1]
        mylist = []
        liststr = lchild.to_value(skip=skip)
        mylist = liststr.split("|")
        v = vchild.to_value(skip=skip)
        ret = None
        if v in mylist:
            ret = True
        elif v.__class__ != str and f"{v}" in mylist:
            ret = True
        else:
            ret = False
        self.value = ret

    def _decide_match(self, skip=None) -> None:
        self.match = self.to_value(skip=skip)
