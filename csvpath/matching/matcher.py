from typing import Any, List
import ply.yacc as yacc
from ..util.parser_utility import ParserUtility
from .productions import *
from .functions.function_factory import FunctionFactory
from .functions.function import Function
from .matching_lexer import MatchingLexer
from .util.expression_encoder import ExpressionEncoder
from .util.exceptions import MatchException
from ..util.exceptions import VariableException
from . import LarkParser, LarkTransformer


class Matcher:
    tokens = MatchingLexer.tokens

    def __init__(
        self, *, csvpath=None, data=None, line=None, headers=None, parser_type="lark"
    ):
        if not headers:
            # this could be a dry-run or unit testing
            pass
        if not data:
            raise MatchException(f"need data input: data: {data}")
        self.path = data
        self.csvpath = csvpath
        self._line = line
        self.expressions = []
        self.if_all_match = []
        self.current_expression = None
        self.parser_type = parser_type
        self.skip = False

        if data is not None:
            if parser_type == "lark":
                self.parser = LarkParser()
                tree = self.parser.parse(data)
                transformer = LarkTransformer(self)
                es = transformer.transform(tree)
                expressions = []
                for e in es:
                    expressions.append([e, None])
                self.expressions = expressions
                self.check_valid()
            if parser_type is None or parser_type == "ply":
                self.lexer = MatchingLexer()
                self.parser = yacc.yacc(module=self, start="match_part")
                self.parser.parse(data, lexer=self.lexer.lexer)
                self.check_valid()
        if self.csvpath:
            self.csvpath.logger.info("initialized Matcher")

    def __str__(self):
        return f"""
            line: {self.line}
            csvpath: {self.csvpath}
            parser: {self.parser}
        """

    @property
    def line(self) -> List[List[Any]]:
        return self._line

    @line.setter
    def line(self, line: List[List[Any]]) -> None:
        # self._last_line = LastLineStats(matcher=self, last_line=self._line)
        self._line = line

    """
    @property
    def last_line(self) -> LastLineStats:
        return self._last_line
    """
    """
    @line.setter
    def line(self, line:LastLineStats) -> None:
        self._last_line = line
    """

    def to_json(self, e) -> str:
        return ExpressionEncoder().to_json(e)

    def dump_all_expressions_to_json(self) -> str:
        return ExpressionEncoder().valued_list_to_json(self.expressions)

    def reset(self):
        for expression in self.expressions:
            expression[1] = None
            expression[0].reset()
        self.current_expression = None

    def header_index(self, name: str) -> int:
        return self.csvpath.header_index(name)

    def header_name(self, i: int) -> str:
        if not self.csvpath.headers:
            return None
        if i < 0 or i >= len(self.csvpath.headers):
            return None
        return self.csvpath.headers[i]

    def header_value(self, name: str) -> Any:
        n = self.header_index(name)
        ret = None
        if n is None:
            pass
        else:
            ret = self.line[n]
        return ret

    def _do_lasts(self) -> None:
        for i, et in enumerate(self.expressions):
            e = et[0]
            self._find_and_actvate_lasts(e)

    def _find_and_actvate_lasts(self, e) -> None:
        cs = e.children[:]
        while len(cs) > 0:
            c = cs.pop()
            if (
                isinstance(c, Equality)
                and c.op == "->"
                and c.left
                and isinstance(c.left, Function)
                and c.left.name == "last"
            ):
                c.matches(skip=[])
            elif isinstance(c, Function) and c.name == "last":
                c.matches(skip=[])
            else:
                cs += c.children

    def matches(self, *, syntax_only=False) -> bool:
        #
        # is this a blank last line? if so, we just want to activate any/all
        # last() in the csvpath.
        #
        if self.csvpath.line_monitor.is_last_line_and_empty(self.line):
            self._do_lasts()
            return True

        ret = True
        failed = False
        self.current_expression = None
        for i, et in enumerate(self.expressions):
            if self.csvpath and self.csvpath.stopped:
                #
                # stopped is like a system halt. this csvpath is calling it
                # quits on this CSV file. we don't continue to match the row
                # so we may miss out on some side effects. we just return
                # because the function already let the CsvPath know to stop.
                #
                return False
            elif self.skip is True:
                #
                # skip is like the continue statement in a python loop
                # we're not only not matching, we don't want any side effects
                # we might gain from continuing to check for a match;
                # but we also don't want to stop the run or fail validation
                #
                self.skip = False
                return False
            self.current_expression = et[0]
            if et[1] is True:
                ret = True
            elif et[1] is False:
                ret = False
            elif not et[0].matches(skip=[]) and not syntax_only:
                et[1] = False
                ret = False
            else:
                et[1] = True
                ret = True
            if not ret:
                failed = True
            if failed:
                ret = False
        if ret is True:
            self.do_set_if_all_match()
        else:
            pass
        return ret

    def check_valid(self) -> None:
        for _ in self.expressions:
            _[0].check_valid()

    def do_set_if_all_match(self) -> None:
        for _ in self.if_all_match:
            name = _[0]
            value = _[1]
            tracking = _[2]
            self.set_variable(name, value=value, tracking=tracking)
        self.if_all_match = []

    def set_if_all_match(self, name: str, value: Any, tracking=None) -> None:
        self.if_all_match.append((name, value, tracking))

    def get_variable(self, name: str, *, tracking=None, set_if_none=None) -> Any:
        if self.csvpath is None:
            return None
        else:
            return self.csvpath.get_variable(
                name, tracking=tracking, set_if_none=set_if_none
            )

    def set_variable(self, name: str, *, value: Any, tracking=None) -> None:
        return self.csvpath.set_variable(name, value=value, tracking=tracking)

    def last_header_index(self) -> int:
        if self.line and len(self.line) > 0:
            return len(self.line) - 1
        return None

    def last_header_name(self) -> str:
        if self.csvpath.headers and len(self.csvpath.headers) > 0:
            return self.csvpath.headers[self.last_header_index()]
        return None

    # ===================
    # productions
    # ===================

    def p_error(self, p):
        ParserUtility().error(self.parser, p)
        raise MatchException(
            f"Halting matching for error on {None if p is None else p.type}"
        )

    def p_match_part(self, p):
        """match_part : LEFT_BRACKET expression RIGHT_BRACKET
        | LEFT_BRACKET expressions RIGHT_BRACKET
        """

    def p_expressions(self, p):
        """expressions : expression
        | expression COMMENT
        | expressions expression
        | COMMENT expressions
        | expressions COMMENT
        | COMMENT
        """

    def p_expression(self, p):
        """expression : function
        | assignment_or_equality
        """
        e = Expression(self)
        e.add_child(p[1])
        self.expressions.append([e, None])
        p[0] = e

    def p_function(self, p):
        """function : SIMPLE_NAME OPEN_PAREN CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN equality CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN function CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN term CLOSE_PAREN
        | SIMPLE_NAME OPEN_PAREN var_or_header CLOSE_PAREN
        """
        name = p[1]
        child = p[3] if p and len(p) == 5 else None
        f = FunctionFactory.get_function(self, name=name, child=child)
        p[0] = f

    def p_assignment_or_equality(self, p):
        """assignment_or_equality : equality
        | assignment
        """
        p[0] = p[1]

    def p_equality(self, p):
        """
        equality : function op term
                 | function op function
                 | function op var_or_header
                 | function DO assignment_or_equality
                 | var DO assignment_or_equality
                 | var DO function
                 | function DO function
                 | equality DO assignment_or_equality
                 | equality DO function
                 | var_or_header op function
                 | var_or_header op term
                 | var_or_header op var_or_header
                 | term op var_or_header
                 | term op term
                 | term op function
                 | equality COMMA equality
                 | equality op term
                 | equality op function
                 | equality COMMA var_or_header
                 | equality COMMA term
                 | equality COMMA function
        """
        e = Equality(self)
        e.left = p[1]
        e.set_operation(p[2])
        e.right = p[3]
        p[0] = e

    def p_op(self, p):
        """op : EQUALS
        | COMMA
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : var ASSIGNMENT var
                 | var ASSIGNMENT term
                 | var ASSIGNMENT function
                 | var ASSIGNMENT header
        """
        e = Equality(self)
        e.left = p[1]
        e.set_operation(p[2])
        e.right = p[3]
        p[0] = e

    def p_term(self, p):
        """term : QUOTED
        | QUOTE DATE QUOTE
        | QUOTE NUMBER QUOTE
        | NUMBER
        | REGEX
        """
        if len(p) == 4:
            p[0] = Term(self, value=p[2])
        else:
            p[0] = Term(self, value=p[1])

    def p_var_or_header(self, p):
        """var_or_header : header
        | var
        """
        p[0] = p[1]

    def p_var(self, p):
        """var : VAR_SYM SIMPLE_NAME"""
        v = Variable(self, name=p[2])
        p[0] = v

    def p_header(self, p):
        """header : HEADER_SYM SIMPLE_NAME
        | HEADER_SYM NUMBER
        | HEADER_SYM QUOTED
        """
        h = Header(self, name=p[2])
        p[0] = h
