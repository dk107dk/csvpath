import unittest
from csvpath.csvpath import CsvPath
from tests.save import Save

PATH = "tests/test_resources/test.csv"


class TestFunctionsEnd(unittest.TestCase):
    def test_function_end1(self):
        path = CsvPath()
        Save._save(path, "test_function_end1")
        path.parse(
            f"""
            ${PATH}[*]
            [
                @end = end()
                no()
            ]"""
        )
        lines = path.collect()
        print(f"test_function_end1: path vars: {path.variables}")
        assert path.variables["end"] == "growl"
        assert len(lines) == 0

    def test_function_end2(self):
        path = CsvPath()
        Save._save(path, "test_function_end2")
        path.parse(
            f"""
            ${PATH}[*]
            [
                @end = end(2)
                no()
            ]"""
        )
        lines = path.collect()
        print(f"test_function_end2: path vars: {path.variables}")
        assert path.variables["end"] == "Frog"
        assert len(lines) == 0
