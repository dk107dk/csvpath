import unittest
from csvpath.matching.functions.function_factory import FunctionFactory
from csvpath.csvpath import CsvPath
from tests.save import Save

PATH = "tests/test_resources/test.csv"
EMPTY = "tests/test_resources/count_physical_lines.csv"


class TestFunctionsCount(unittest.TestCase):
    def test_function_factory_count(self):
        count = FunctionFactory.get_function(None, name="count", child=None)
        assert count

    def test_function_factory_count_empty(self):
        f = FunctionFactory.get_function(None, name="count", child=None)
        assert f.to_value() == 0  # no matcher or csvpath == -1 + eager match 1

    def test_function_count_equality(self):
        path = CsvPath()
        Save._save(path, "test_function_count_equality")
        path.parse(f'${PATH}[*][count(#lastname=="Bat")==7]')
        lines = path.collect()
        print(f"test_function_count_equality: lines: {lines}")
        assert len(lines) == 1
        assert lines[0][0] == "Frog"

    def test_function_count_headers_in(self):
        path = CsvPath()
        Save._save(path, "test_function_count_headers_in")
        path.parse(
            f"""
                ${PATH}
                [*][
                    count.firstname_is_one.onmatch( in(#firstname,"Bug|Bird|Ants") ) == 2
                ]
             """
        )
        lines = path.collect()
        print(f"test_function_count_headers_in: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_count_headers_in: line: {line}")
        print(f"test_function_count_headers_in: path vars: {path.variables}")
        assert len(lines) == 1
        assert "firstname_is_one" in path.variables
        assert path.variables["firstname_is_one"][True] == 3

    def test_function_count_header_in_ever1(self):
        path = CsvPath()
        Save._save(path, "test_function_count_header_in_ever1")
        path.parse(
            f"""
                ${PATH}
                [1*]
                [
                    @x.onmatch = count()
                    in(#firstname,"Bug|Bird|Ants")
                ]
                   """
        )
        lines = path.collect()
        print(f"test_function_count_in: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_count_in: line: {line}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "x" in path.variables
        assert path.variables["x"] == 3
        assert len(lines) == 3

    def test_function_count_lines(self):
        path = CsvPath()
        Save._save(path, "test_function_count_lines")
        path.parse(f'${PATH}[*][ #firstname=="David" @david.onmatch=count_lines() ]')
        lines = path.collect()
        assert len(lines) == 1
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["david"] == 2

    def test_function_count_scans(self):
        path = CsvPath()
        Save._save(path, "test_function_count_scans")
        path.parse(
            f'${PATH}[*][ #firstname=="Frog" @frogs_seen=count() @scanned_for_frogs=count_scans()  ]'
        )
        lines = path.collect()
        assert len(lines) == 2
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["frogs_seen"] == 2
        assert path.variables["scanned_for_frogs"] == 9

    def test_function_count_nocount(self):
        path = CsvPath()
        Save._save(path, "test_function_nocount")
        path.parse(
            f"""
            ${PATH}[*][ @imcounting = count() no()]
            """
        )
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "imcounting" not in path.variables
        assert len(lines) == 0

    def test_function_count_allcount(self):
        path = CsvPath()
        Save._save(path, "test_function_allcount")
        path.parse(
            f"""
            ${PATH}[*][ @imcounting = count() yes()]
            """
        )
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "imcounting" in path.variables
        assert path.variables["imcounting"] == 9
        assert len(lines) == 9

    def test_function_count_linecount1(self):
        path = CsvPath()
        Save._save(path, "test_function_linecount1")
        path.parse(
            f"""
            ${PATH}[*][ @imcounting = count_lines() no()]
            """
        )
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "imcounting" in path.variables
        # lines are zero-based, unlike match counts
        assert path.variables["imcounting"] == 9
        assert len(lines) == 0

    def test_function_count_linecount2(self):
        path = CsvPath()
        Save._save(path, "test_function_linecount2")
        path.parse(
            f"""
            ${PATH}[*][ @imcounting.onmatch = count_lines() no()]
            """
        )
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "imcounting" not in path.variables
        # lines are zero-based, unlike match counts
        # assert path.variables["imcounting"] == 0
        assert len(lines) == 0

    def test_function_count_linecount3(self):
        path = CsvPath()
        Save._save(path, "test_function_linecount2")
        path.parse(
            f"""
            ${EMPTY}[*][
                push( "physical", line_number() )
                push( "data", count_lines())
            ]
            """
        )
        path.fast_forward()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "physical" in path.variables
        assert "data" in path.variables
        assert path.variables["physical"] == [0, 1, 5, 7]
        assert path.variables["data"] == [1, 2, 3, 4]

    """
    # non-deterministic test, but a good example to keep for now
    def test_average_what_the(self):
        path = CsvPath()
        path.parse(
            f""
            ${NUMBERS}[1*]
            [
                @ave = average.test.onmatch(#count3, "line")
                @r = random(0,1)
                @c = count()
                @c2 = count_scans()
                @c3 = count_lines()
                @r == 1
                yes()
                print(count_lines()==1, "match, scan, line, random, average")
                print(yes(), "$.variables.c, $.variables.c2, $.variables.c3, $.variables.r, $.variables.ave")
            ]""
        )
        print("")
        lines = path.collect()
        print(f"test_average_what_the: path vars: {path.variables}")
        #assert path.variables["the_average"] == 2
        #assert len(lines) == 0
        """
