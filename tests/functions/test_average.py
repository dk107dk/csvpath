import unittest
from csvpath.csvpath import CsvPath
from tests.save import Save

PATH = "tests/test_resources/test.csv"
NUMBERS = "tests/test_resources/numbers.csv"


class TestFunctionsAverage(unittest.TestCase):
    def test_function_average1(self):
        path = CsvPath()
        Save._save(path, "test_function_average1")
        path.parse(
            f"""
            ${PATH}[3-5]
            [
                @the_average = average(count(), "match")
                no()
            ]"""
        )
        lines = path.collect()
        print(f"\ntest_function_count_in: path vars: {path.variables}")
        assert path.variables["the_average"] is None
        assert len(lines) == 0

    def test_function_average2(self):
        path = CsvPath()
        Save._save(path, "test_function_average2")
        path.parse(
            f"""
            ${PATH}[3-5]
            [
                @the_average = average(count(#lastname), "scan")
                no()
            ]"""
        )
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_average"] == 2
        assert len(lines) == 0

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
