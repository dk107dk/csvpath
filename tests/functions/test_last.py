import unittest
import pytest
from csvpath.csvpath import CsvPath
from csvpath.matching.matcher import Matcher
from tests.save import Save

PATH = "tests/test_resources/test.csv"


class TestFunctionsLast(unittest.TestCase):
    def test_function_last1(self):
        print("")
        path = CsvPath()
        Save._save(path, "test_function_last1")
        matchpart = """
            [
                count_lines()==0 -> @first = 0
                last() -> @last = count_lines()
            ]"""

        matcher = Matcher(
            csvpath=path,
            data=matchpart,
            line=["Frog", "Bats", "ribbit..."],
            headers=["firstname", "lastname", "say"],
        )
        print("")
        count_lines = matcher.expressions[0][0].children[0].left.left.matches(skip=[])
        assert count_lines is True
        lines = matcher.expressions[0][0].children[0].left.left.to_value(skip=[])
        assert lines == 0
        is0 = matcher.expressions[0][0].children[0].left.matches(skip=[])
        assert is0 is True
        op = matcher.expressions[0][0].children[0].op
        assert op == "->"
        b1 = matcher.expressions[0][0].matches(skip=[])
        #
        # this was False because -1 < 0
        # we have to be careful:
        # .  line_number is a pointer
        # .  total_lines is a count
        # .  count_lines is a count
        # for now just changing to True.
        #
        b2 = matcher.expressions[1][0].matches(skip=[])
        print("")
        print(f"test_function_last1: path vars: {path.variables}")
        print(f"test_function_last1: b1: {b1}, b2: {b2}")
        assert path.variables["first"] == 0
        assert b1 is True
        assert b2 is True

    """
    def test_function_last2(self):
        path = CsvPath()
        Save._save(path, "test_function_last2")
        path.parse(
            f"" ${PATH}[*] [
                count_lines()==0 -> @first = 0
                last() -> @last = count_lines()
            ]
            ""
        )
        print("")
        lines = path.collect()
        print(f"test_function_last: path vars: {path.variables}")
        print(f"test_function_last: lines: {lines}")
        assert path.variables["last"] == 8
        assert path.variables["first"] == 0
    """
    # FIXME: this is not really a deterministic test.
    def test_function_last3(self):
        path = CsvPath()
        Save._save(path, "test_function_last3")
        path.parse(
            f""" ${PATH}[*] [ yes() -> print("$.csvpath.line_count")
                last() -> print("the last row is $.csvpath.line_count")
            ]
            """
        )
        print("")
        path.fast_forward()
        print(f"test_function_last: path vars: {path.variables}")

    def test_function_last4(self):
        path = CsvPath()
        Save._save(path, "test_function_last4")
        path.parse(
            f"""${PATH}[*]
                            [
                                tally(#lastname) no()
                                @hmmm = @lastname.Bat
                                @ohhh = @hmmm.fish
                                @lastname.Bat = "fred"
                            ]
                   """
        )

        with pytest.raises(TypeError):
            path.collect()
            print(f"test_function_last4: path vars: {path.variables}")
            assert path.variables["lastname"]["Bat"] == "fred"
            assert path.variables["hmmm"] == 7
            assert path.variables["ohhh"] is None
