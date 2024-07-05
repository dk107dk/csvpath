import unittest
from csvpath.matching.matcher import Matcher
from csvpath.matching.functions.count import Count
from csvpath.matching.functions.function_factory import FunctionFactory
from csvpath.csvpath import CsvPath

PATH = "tests/test_resources/test.csv"

class TestFunctions(unittest.TestCase):

#============= count ================

    def test_function_factory(self):
        count = FunctionFactory.get_function(None, name="count", child=None)
        assert count

    def test_function_count_empty(self):
        f = FunctionFactory.get_function(None, name="count", child=None)
        assert f.to_value() == 0 # no matcher or csvpath == -1 + eager match 1

    def test_function_count_equality(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][count(#lastname="Bat")=7]')
        lines = path.collect()
        print(f"test_function_count_equality: lines: {lines}")
        assert len(lines) == 1
        assert lines[0][0] == "Frog"

    def test_function_header_in(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][in(#firstname,"Bug|Bird|Ants")]')
        lines = path.collect()
        print(f"test_function_count_in: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_count_in: line: {line}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert len(lines) == 3

    def test_function_count_header_in(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][count(in(#firstname,"Bug|Bird|Ants"))=2]')
        lines = path.collect()
        print(f"test_function_count_in: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_count_in: line: {line}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert len(lines) == 1

    def test_function_percent(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][@p = percent("match") #lastname="Bat"]')
        lines = path.collect()
        print(f"test_function_count_in: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_count_in: line: {line}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert len(lines) == 7
        assert path.variables["p"] == .75


    def test_function_below_percent(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][@p = percent("match")  below(@p,.35) #lastname="Bat"]')
        lines = path.collect()
        print(f"test_function_below_percent: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_below_percent: line: {line}")
        print(f"test_function_below_percent: path vars: {path.variables}")
        assert len(lines) == 3
        assert path.variables["p"] == .375


    def test_function_first(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][first(#lastname)]')
        lines = path.collect()
        print(f"test_function_first: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_first: line: {line}")
        print(f"test_function_first: path vars: {path.variables}")
        assert len(lines) == 3

        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][first(#firstname)]')
        lines = path.collect()
        print(f"test_function_first: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_first: line: {line}")
        print(f"test_function_first: path vars: {path.variables}")
        assert len(lines) == 8

        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][first(#firstname, #lastname)]')
        lines = path.collect()
        print(f"test_function_first: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_first: line: {line}")
        print(f"test_function_first: path vars: {path.variables}")
        assert len(lines) == 8


    def test_function_above_percent(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][@p = percent("line")  above(@p,.35) #lastname="Bat"]')
        lines = path.collect()
        print(f"test_function_above_percent: lines: {len(lines)}")
        for line in lines:
            print(f"test_function_above_percent: line: {line}")
        print(f"test_function_above_percent: path vars: {path.variables}")
        assert len(lines) == 6
        assert path.variables["p"] == 1


    def test_function_upper_and_lower(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ @upper = upper(#firstname) @lower = lower(#firstname) ]')
        lines = path.collect()
        print(f"test_function_count_in: lines: {len(lines)}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert "upper" in path.variables
        assert "lower" in path.variables
        assert path.variables["lower"] == "frog"
        assert path.variables["upper"] == "FROG"

    def test_function_count_lines(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ #firstname="David" @david=count_lines() ]')
        lines = path.collect()
        assert len(lines) == 1
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["david"] == 1

    def test_function_count_scans(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ #firstname="Frog" @frogs_seen=count() @scanned_for_frogs=count_scans()  ]')
        lines = path.collect()
        assert len(lines) == 2
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["frogs_seen"] == 2
        assert path.variables["scanned_for_frogs"] == 9


    """
    TODO: need a way to only count complete path matches
    """
    def test_function_first_two_lines(self):
        path = CsvPath()
        # this returns the first two lines because first collects
        # the first instance of every value matched, so 0 and 1 for False and True
        scanner = path.parse(f'${PATH}[*][ first(count()=1)]')
        lines = path.collect()
        print(f"test_function_first_two_lines: path vars: {path.variables}")
        assert len(lines) == 2


    def test_function_first_line(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                count(#firstname="Frog")=1
                @say=#say
                @line=count_lines()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: lines: {lines}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert len(lines) == 1
        assert path.variables["say"] == 'ribbit...'
        assert path.variables["line"] == 3

    def test_function_any_match(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                or(#firstname="Fish", #lastname="Kermit", #say="oozeeee...")
                @say=#say
                @line=count_lines()

            ]''')
        lines = path.collect()
        print(f"test_function_count_in: lines: {lines}")
        print(f"test_function_count_in: path vars: {path.variables}")
        assert len(lines) == 3
        assert path.variables["say"] == 'oozeeee...'
        assert path.variables["line"] == 7

    # set a var without matching the lines
    def test_function_count_any_match(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @interesting = count(
                    or(#firstname="Fish", #lastname="Kermit", #say="oozeeee...")
                )
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["interesting"] == 3
        assert len(lines) == 0

    def test_function_end(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @end = end()
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["end"] == "growl"
        assert len(lines) == 0


    def test_function_max(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @the_max = max(#firstname)
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_max"] == "Slug"
        assert len(lines) == 0

        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @the_max = max(#0)
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_max"] == "firstname"
        assert len(lines) == 0


    def test_function_min(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @the_min = min(#firstname)
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_min"] == "Ants"
        assert len(lines) == 0

        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[3-5]
            [
                @the_min = min(#firstname, "scan")
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_min"] == "Bird"
        assert len(lines) == 0

        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[3-5]
            [
                @the_min = min(#firstname, "match")
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_min: path vars: {path.variables}")
        assert path.variables["the_min"] == None
        assert len(lines) == 0

    def test_function_average(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[3-5]
            [
                @the_average = average(count(), "match")
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_average"] == None
        assert len(lines) == 0

        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[3-5]
            [
                @the_average = average(count(#lastname), "scan")
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_average"] == 2
        assert len(lines) == 0

    def test_function_median(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @the_median = median(count(#lastname), "line")
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["the_median"] == 3
        assert len(lines) == 0

    def test_function_random(self):
        path = CsvPath()
        scanner = path.parse(
        f'''
            ${PATH}[*]
            [
                @r = random(0, 1)
                no()
            ]''')
        lines = path.collect()
        print(f"test_function_count_in: path vars: {path.variables}")
        assert path.variables["r"] == 1 or path.variables["r"] == 0
        assert len(lines) == 0


    def test_function_isinstance(self):
        path = CsvPath()
        print("checking ints")
        scanner = path.parse(f'${PATH}[*][ isinstance(count(), "int") ]')
        lines = path.collect()
        assert len(lines) == 9
        print(f"test_function_length: lines: {lines}")
        print("checking dates")
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("11-23-2024", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 9
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("2024-11-23", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 9
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("2024-1-3", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 9
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("2024-59-23", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 0
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("1000-1-1", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 9
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("1/12/2024", "datetime") ]')
        lines = path.collect()
        assert len(lines) == 9
        print("checking $$$")
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("$1000.59", "usd") ]')
        lines = path.collect()
        assert len(lines) == 9
        print("checking float")
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("11.59", "float") ]')
        lines = path.collect()
        assert len(lines) == 9
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("11.59", "int") ]')
        lines = path.collect()
        assert len(lines) == 0
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ isinstance("11.59", "usd") ]')
        lines = path.collect()
        assert len(lines) == 0


    def test_function_length(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][length(#lastname)=3]')
        lines = path.collect()
        print(f"test_function_length: lines: {len(lines)}")
        assert len(lines) == 7

    def test_function_not(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][not(length(#lastname)=3)]')
        lines = path.collect()
        print(f"test_function_not: lines: {len(lines)}")
        assert len(lines) == 2

    def test_function_now(self):
        path = CsvPath()
        # obviously this will break and need updating 1x a year
        scanner = path.parse(f'${PATH}[*][now("%Y") = "2024"]')
        lines = path.collect()
        print(f"test_function_now: lines: {len(lines)}")
        assert len(lines) == 9

    def test_function_in(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][in( #0 , "Bug|Bird|Ants" )]')
        lines = path.collect()
        print(f"test_function_in: lines: {len(lines)}")
        assert len(lines) == 3

    def test_function_concat(self):
        path = CsvPath()
        scanner = path.parse(f'${PATH}[*][ #0 = concat("B" , "ird") ]')
        lines = path.collect()
        print(f"test_function_concat: lines: {len(lines)}")
        assert len(lines) == 1


