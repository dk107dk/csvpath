import unittest
from csvpath import CsvPath
from csvpath import CsvPaths
from tests.save import Save

PATH = "tests/test_resources/test.csv"


class TestFunctionsMetaphone(unittest.TestCase):
    def test_function_metaphone1(self):
        path = CsvPath()
        Save._save(path, "test_function_metaphone1")
        path.parse(
            f"""
                        ${PATH}[*][
                            @z1 = metaphone("zach")
                            @z2 = metaphone("zack")
                            @z = equals(@z1, @z2)

                            @s1 = metaphone("Sacks")
                            @s2 = metaphone("Sax")
                            @s = equals(@s1, @s2)
                        ]
                   """
        )
        path.fast_forward()
        print(f"test_function_metaphone1: {path.variables}")
        assert path.variables["z"] is False
        assert path.variables["s"] is True

    def test_function_metaphone2(self):
        print("")
        # load the lookup table
        paths = CsvPaths()
        paths.file_manager.add_named_file(
            name="lookups", path="tests/test_resources/named_files/lookup_names.csv"
        )
        paths.paths_manager.add_named_paths_from_file(
            name="meta",
            file_path="tests/test_resources/named_paths/metaphone_lookup.csvpaths",
        )
        paths.fast_forward_paths(pathsname="meta", filename="lookups")
        results = paths.results_manager.get_named_results("meta")
        r = results[0]
        c = r.csvpath
        print(f"test_function_metaphone2: c.vars: {c.variables}")
        print("")

        # test the lookup
        path = paths.csvpath()
        Save._save(path, "test_function_metaphone1")
        path.parse(
            f"""
                ${PATH}[*][
                    @z1 = metaphone("zach", $meta.variables.meta)
                    @z2 = metaphone("zack", $meta.variables.meta)
                    @z = equals(@z1, @z2)

                    @s1 = metaphone("Sacks", $meta.variables.meta)
                    @s2 = metaphone("Sax", $meta.variables.meta)
                    @s = equals(@s1, @s2)

                    @i1 = metaphone("IBM", $meta.variables.meta)
                    @i2 = metaphone("I.B.M", $meta.variables.meta)
                    @i = equals(@i1, @i2)

                    @a1 = metaphone("Add", $meta.variables.meta)
                    @a2 = metaphone("Ad", $meta.variables.meta)
                    @a = equals(@a1, @a2)

                    @s21 = metaphone("Smithson", $meta.variables.meta)
                    @s22 = metaphone("Smithsun", $meta.variables.meta)
                    @s2_ = equals(@s21, @s22)
                ]
            """
        )
        path.fast_forward()
        print(f"test_function_metaphone2: {path.variables}")
        # zach and zack are not alike, even though they probably should be
        assert path.variables["z"] is False
        assert path.variables["s"] is True
        assert path.variables["i"] is True
        assert path.variables["a"] is True
        assert path.variables["s2_"] is True
