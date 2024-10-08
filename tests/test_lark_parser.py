import unittest
from lark import Lark
from lark.tree import Tree
from lark.lexer import Token
import os
from csvpath.matching.lark_parser import LarkParser


class TestLarkParser(unittest.TestCase):
    def test_lark_parser(self):
        dirpath = "tests/grammar/match"
        dlist = os.listdir(dirpath)
        base = dirpath
        i = 0
        e = 0
        for p in dlist:
            try:
                _ = p.lower()
                if _.endswith(".txt"):
                    path = os.path.join(base, p)
                    print(f"file: {path}")
                    with open(path) as f:
                        matchpart = f.read()
                        LarkParser()
                        parser = Lark(
                            LarkParser.GRAMMAR, start="match", ambiguity="explicit"
                        )

                        parser.parse(matchpart)
                        #
                        # lark makes very pretty output, if we want to see it.
                        #
                        # tree = parser.parse(matchpart)
                        # print(f"path {path} is:\n{tree.pretty()}")
                        #
            except Exception as ex:
                print(f"Error on {i}: {ex} at {p}")
                e += 1
                break
        print(f"test_lark_parser: {i} examples parsed correctly")
        assert e == 0
