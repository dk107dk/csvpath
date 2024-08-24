import unittest
from csvpath.csvpath import CsvPath
from tests.save import Save

PATH = "tests/test_resources/test.csv"


class TestFunctionStop(unittest.TestCase):
    def test_function_stop(self):
        path = CsvPath()
        Save._save(path, "test_function_stop")
        path.parse(
            f"""
            ${PATH}[*]
            [
                @i = concat( #firstname, #lastname)
                @c = count_lines()
                yes()
                stop(@i == "FishBat")
            ]"""
        )
        lines = path.collect()
        print(f"test_function_stop: path vars: {path.variables}")
        print(f"test_function_stop: lines: {lines}")
        assert path.stopped is True
        assert path.variables["i"] == "FishBat"
        assert path.variables["c"] == 2
        assert len(lines) == 3

    def test_function_skip1(self):
        path = CsvPath()
        Save._save(path, "test_function_skip1")
        path.parse(
            f"""
            ${PATH}[1*]
            [
                @name = concat( #firstname, #lastname)
                skip(@name == "FishBat")
                push( "not_skipped", count_lines() )
                print("not skipped!")
            ]"""
        )
        lines = path.collect()
        print(f"test_function_skip1: path vars: {path.variables}")
        print(f"test_function_skip1: lines: {lines}")
        # assert path.variables["name"] == "FishBat"
        assert len(lines) == 7
        assert path.variables["not_skipped"] == [1, 3, 4, 5, 6, 7, 8]
