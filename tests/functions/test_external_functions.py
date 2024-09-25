import unittest
from csvpath.csvpath import CsvPath
from csvpath.matching.functions.function_finder import FunctionFinder
from csvpath.matching.functions.function_factory import FunctionFactory

PATH = "tests/test_resources/test.csv"


class TestFunctionsExternals(unittest.TestCase):
    def test_function_externals1(self):
        print("")
        path = CsvPath()
        FunctionFinder._add_function(
            path.matcher,
            FunctionFactory,
            "from csvpath.matching.functions.boolean.yes import Yes as sure",
        )
        path.parse(
            f"""
            ${PATH}[*]
            [
                @a = sure()
            ]"""
        )
        path.fast_forward()
        print(f"test_function_externals: path vars: {path.variables}")
        assert "a" in path.variables
        assert path.variables["a"] is True
        assert len(FunctionFactory.NOT_MY_FUNCTION) == 2
        assert FunctionFinder.EXTERNALS in FunctionFactory.NOT_MY_FUNCTION

    def test_function_externals2(self):
        print("")
        path = CsvPath()
        path.config.configpath = "tests/test_resources/config.ini"
        path.config.reload()
        assert path.config.function_imports is not None
        assert path.config.function_imports == "tests/test_resources/function.imports"
