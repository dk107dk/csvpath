import csv
from typing import List
from collections.abc import Iterator
from csvpath.matching.matcher import Matcher
from csvpath.scanning.scanner import Scanner

class NoFileException(Exception):
    pass

class CsvPath:

    def __init__(self, *, filename=None):
        self.filename = filename
        self.scanner = None
        self.value = None
        self.scan = None
        self.match = None
        self.modify = None
        self.headers = None
        self.line_number = 0
        self.scan_count = 0
        self.match_count = 0

    def parse(self, data):
        self.scanner = Scanner()
        s, mat, mod = self._find_scan_match_modify(data)
        self.scan = s
        self.match = mat
        self.modify = mod
        self.scanner.parse(s)
        return self.scanner

    def _find_scan_match_modify(self, data):
        scan = ""
        matches = ""
        modify = ""
        p = 0
        for i, c in enumerate(data):
            if p == 0:
                scan = scan + c
            elif p == 1:
                matches = matches + c
            else:
                modify = modify + c
            if c == "]":
                p = p+1
        scan = scan.strip()
        matches = matches.strip()
        modify = modify.strip()
        return scan if len(scan) > 0 else None, matches if len(matches) > 0 else None, modify if len(modify) > 0 else None


    def __str__(self):
        return f"""
            path: {self.scanner.path}
            filename: {self.filename}
            parser: {self.scanner}
            from_line: {self.scanner.from_line}
            to_line: {self.scanner.to_line}
            all_lines: {self.scanner.all_lines}
            these: {self.scanner.these}
        """

    @property
    def from_line(self):
        return self.scanner.from_line

    @property
    def to_line(self):
        return self.scanner.to_line

    @property
    def all_lines(self):
        return self.scanner.all_lines

    @property
    def path(self):
        return self.scanner.path

    @property
    def these(self):
        return self.scanner.these

    @property
    def filename(self):
        return self.file_name

    @filename.setter
    def filename(self, f):
        self.file_name = f

    def next(self):
        if self.scanner.filename is None:
            raise NoFileException("there is no filename")
        with open(self.scanner.filename) as file:
            reader = csv.reader(file, delimiter=' ', quotechar='|')
            for line in reader:
                if self.line_number == 0:
                    self.headers = line
                if self.includes(self.line_number):
                    self.scan_count = self.scan_count + 1
                    if self.matches(line):
                        self.match_count = self.match_count + 1
                        yield line
                self.line_number = self.line_number + 1

    def current_line_number(self) -> int:
        return self.line_number

    def current_scan_count(self) -> int:
        return self.scan_count

    def current_match_count(self) -> int:
        return self.match_count

    def matches(self, line) -> bool:
        if not self.match:
            return True
        matcher = Matcher(csvpath=self, data=self.match, line=line, headers=self.headers)
        return matcher.matches()

    def get_variable(self, name):
        if name not in self.variables:
            self.variables[name] = None
        return self.variables[name]

    def set_variable(self, name, value):
        self.variables[name] = value

    def includes(self, line:int) -> bool:
        from_line = self.scanner.from_line
        to_line = self.scanner.to_line
        all_lines = self.scanner.all_lines
        these = self.scanner.these
        return self._includes(line, from_line=from_line, to_line=to_line, all_lines=all_lines, these=these)

    def _includes(self, line:int, *, from_line:int=None,
                  to_line:int=None, all_lines:bool=None, these:List[int]=[] ) -> bool:
        if line is None:
            return False
        if from_line is None and all_lines:
            return True
        if from_line is not None and all_lines:
            return line >= from_line
        if from_line == line:
            return True
        if from_line is not None and to_line is not None and from_line > to_line:
            return line >= to_line and line <= from_line
        if from_line is not None and to_line is not None:
            return line >= from_line and line <= to_line
        if line in these:
            return True
        if to_line is not None:
            return line < to_line
        return False

    def line_numbers(self) -> Iterator[int|str]:
        these = self.scanner.these
        from_line = self.scanner.from_line
        to_line = self.scanner.to_line
        all_lines = self.scanner.all_lines
        return self._line_numbers(these=these, from_line=from_line, to_line=to_line, all_lines=all_lines )

    def _line_numbers(self, *, these:List[int]=[],
                      from_line:int=None, to_line:int=None,
                      all_lines:bool=None) -> Iterator[int|str]:
        if len(these) > 0:
            for i in these:
                yield i
        else:
            if from_line is not None and to_line is not None and from_line > to_line:
                for i in range(to_line, from_line+1):
                    yield i
            elif from_line is not None and to_line is not None:
                for i in range(from_line, to_line+1):
                    yield i
            elif from_line is not None:
                if all_lines:
                    yield f"{from_line}..."
                else:
                    yield from_line
            elif to_line is not None:
                yield f"0..{to_line}"

    def collect_line_numbers(self) -> List[int|str]:
        these = self.scanner.these
        from_line = self.scanner.from_line
        to_line = self.scanner.to_line
        all_lines = self.scanner.all_lines
        return _collect_line_numbers(these=these, from_line=from_line, to_line=to_line, all_lines=all_lines)

    def _collect_line_numbers(self, *, these:List[int]=[],
                      from_line:int=None, to_line:int=None,
                      all_lines:bool=None )-> List[int|str]:
        collect = []
        for i in self._line_numbers(these=these, from_line=from_line, to_line=to_line, all_lines=all_lines):
            collect.append(i)
        return collect


