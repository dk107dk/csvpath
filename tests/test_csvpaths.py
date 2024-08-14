import unittest
from csvpath.csvpaths import CsvPaths

PATH = "tests/test_resources/test.csv"
LOOKUP = "tests/test_resources/lookup.csv"
NUMBERS = "tests/test_resources/numbers.csv"
FOOD = "tests/test_resources/food.csv"
JSON = "tests/test_resources/named_files.json"
DIR = "tests/test_resources"
DIR2 = "tests/test_resources/"


class TestCsvPaths(unittest.TestCase):
    """
    def test_lookup(self):
        print("")
        nfiles = {"test": PATH, "numbers": NUMBERS, "food": FOOD}
        npaths = {"lookup": f" ""${LOOKUP}[*][yes()] " ""}
        paths = CsvPaths(named_files=nfiles, named_paths=npaths)

        path = paths.csvpath()
        #
        # name of collection
        # value to look_up
        # column index to look to
        # column index with the new value, if found
        #
        thepath = "" "$food[1*][
            @t = lookup("lookup", #1, 0, 1)
            print("t is $.variables.t")
        ]" ""
        path.parse(thepath)
        lines = path.collect()
        print(f"\ntest_lookup: lines: {lines} ")
        print(f"\ntest_lookup: variables: {path.variables} ")
        assert lines is not None
        assert path.variables["t"] == "Sweets"
    """

    """
    def test_dict(self):
        print("")
        d = {"test": PATH, "numbers": NUMBERS}
        paths = CsvPaths(named_files=d)
        path = paths.csvpath()
        filepath = "$test[*][yes()]"
        filepath2 = path._update_file_path(filepath)
        print(f"\ntest_dict: path: {filepath} ~= {filepath2}")
        assert filepath2 is not None
        assert filepath2 == f"${PATH}[*][yes()]"

    def test_json(self):
        print("")
        paths = CsvPaths(filename=JSON)
        path = paths.csvpath()
        filepath = "$test[*][yes()]"
        filepath2 = path._update_file_path(filepath)
        print(f"\ntest_dict: path: {filepath} ~= {filepath2}")
        assert filepath2 is not None
        assert filepath2 == f"${PATH}[*][yes()]"

    def test_file(self):
        print("")
        paths = CsvPaths(filename=PATH)
        path = paths.csvpath()
        filepath = "$test[*][yes()]"
        filepath2 = path._update_file_path(filepath)
        print(f"\ntest_dict: path: {filepath} ~= {filepath2}")
        assert filepath2 is not None
        assert filepath2 == f"${PATH}[*][yes()]"


    def test_no_named_file_match(self):
        print("")
        paths = CsvPaths()
        path = paths.csvpath()
        filepath = f"${PATH}[*][yes()]"
        filepath2 = path._update_file_path(filepath)
        print(f"\ntest_dict: path: {filepath} ~= {filepath2}")
        assert filepath2 is not None
        assert filepath2 == filepath

    def test_no_file_name(self):
        print("")
        paths = CsvPaths()
        path = paths.csvpath()
        filepath = f"$[*][yes()]"
        scanner = path.parse(filepath)
        print(f"\ngot here! {scanner}")
        assert scanner

    def test_multi_paths1(self):
        print("")
        paths = CsvPaths()
        paths.add_named_paths_from_dir(dir_path="tests/test_resources/named_paths")
        print(f"named paths: {paths.named_paths}")
        assert paths.named_paths
        assert len( paths.named_paths) == 1
        assert "many" in paths.named_paths
        assert isinstance( paths.named_paths["many"], list )
        assert len( paths.named_paths["many"]) == 2

    def test_multi_paths2(self):
        print("")
        paths = CsvPaths()
        paths.add_named_paths_from_dir(dir_path="tests/test_resources/named_paths")
        print(f"named paths: {paths.named_paths}")
        paths.apply_csvpaths_to_csv_file( "many", PATH )
        lines = paths.collect()
        assert lines
        assert len(lines) == 9
        assert paths.variables
        assert len(paths.variables) == 2
        assert "one" in paths.variables
        assert "two" in paths.variables
        assert paths.variables["one"] == 9
        assert paths.variables["two"] == 9

    """
