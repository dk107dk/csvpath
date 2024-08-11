from ply.yacc import YaccProduction


class ParserUtility:
    def __init__(self, quiet=False):  # pragma: no cover
        self._quiet = quiet

    def error(self, parser, p: YaccProduction) -> None:
        if self._quiet and False:  # pragma: no cover
            return
        if p:
            print(
                f"syntax error at token {p.type}, line {p.lineno}, position {p.lexpos}"
            )
            print(f"unexpected token: {p.value}")
            print("symbol stack: ")
            stack = parser.symstack

            import inspect

            for _ in stack:
                print(f"  {_}")
            print("")
        else:
            print("syntax error at EOF")

    def print_production(
        self, p: YaccProduction, label: str = None, override=True
    ) -> None:
        if self._quiet and not override:
            return
        if label:
            label = f" at {label}"
        print(f"production array {label} is:")
        for _ in p:
            print(f"\t{_} \t-> {_.__class__}")

    @classmethod
    def enumerate_p(self, message, p, quiet=True):
        if quiet:
            return
        print(f"Enumerate {p}: {message}:")
        for i, _ in enumerate(p):
            print(f"   p[{i}]: {_}")
