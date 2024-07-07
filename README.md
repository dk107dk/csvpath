
# CsvPath

CsvPath defines a declarative syntax for inspecting and updating CSV files. Though much simpler, it is similar to:
- XPath: CsvPath is to a CSV file like XPath is to an XML file
- Schematron: Schematron is basically XPath rules applied using XSLT. CsvPath paths can be used as validation rules.
- CSS selectors: CsvPath picks out structured data in a similar way to how CSS selectors pick out HTML structures.

CsvPath is intended to fit with other DataOps and data quality tools. Files are streamed. The interface is simple. Custom functions can be added.

# Usage
CsvPath paths have two parts, scanning and matching. For usage, see the unit tests in [tests/test_scanner.py](tests/test_scanner.py), [tests/test_matcher.py](tests/test_matcher.py) and [tests/test_functions.py](tests/test_functions.py).

    path = CsvPath(delimiter=",")
    path.parse("$test.csv[5-25][#0="Frog" #lastname="Bats" count()=2]")
    for i, line in enumerate( path.next() ):
        print(f"{i}: {line}")

    print(f"path vars: {path.variables}")

This scanning and matching path says:
- open test.csv
- scan lines 5 through 25
- match the second time we see a line where the first column equals "Frog" and the column called  "lastname" equals "Bats"

# Scanning
The scanner enumerates lines. For each line returned, the line number, the scanned line count, and the match count are available. The set of line numbers scanned is also available.

The scan part of the path starts with '$' to indicate the root, meaning the file from the top. After the '$' comes the file path. The scanning instructions are in a bracket. The rules are:
- `[*]` means all
- `[3*]` means starting from line 3 and going to the end of the file
- `[3]` by itself means just line 3
- `[1-3]` means lines 1 through 3
- `[1+3]` means lines 1 and line 3
- `[1+3-8]` means line 1 and lines 3 through eight

# Matching
The match part is also bracketed. Matches have space separated
components that are ANDed together. A match component is one of several types:
<table>
<tr>
<td>Type</td>
<td>Returns</td>
<td>Matches</td>
<td>Description</td>
<td>Examples</td>
</tr>
    <tr>
        <td>Term </td><td> Value </td><td> True </td>
        <td>A quoted string or date, optionally quoted number, or
        regex. Regex features are limited. A regex is wrapped  in "/" characters.</td>
        <td>
            <li/> "Massachusetts"
            <li/> 89.7
            <li/> /[0-9a-zA-Z]+!/
        </td>
    </tr>
    <tr>
        <td>Function </td><td> Calculated   </td><td> Calculated </td>
        <td>A function name followed by parentheses. Functions can
contain terms, variables, headers and other  functions. Some functions
take a specific or  unlimited number of types as arguments.     </td>
        <td>
            <li/> not(count()=2)
        </td>
    </tr>
    <tr>
        <td>Variable </td>
        <td>Value when tested, True when set, True/False when used alone    </td>
        <td>True/False when value tested. True when set, True/False existence when used alone</td>
        <td>An @ followed by a name. A variable is
            set or tested depending on the usage. By itself, it is an existence test. When used as
            the left hand side of an equality not contained by another type its value is set.
            When it is used on the right hand side of an "=" it is an equality test. A function
            may handle variables in different ways, but usually they are an argument that supplies an
            input to the function.
        <td>
            <li/> @weather="cloudy"
            <li/> count(@weather="sunny")
            <li/> @weather
            <li/> #summer=@weather

#1 is an assignment that sets the variable and returns True. #2 is an argument used as a test in a way that is specific to the function. #3 is an existence test. #4 is a test.
        </td>
    </tr>
    <tr>
        <td>Header   </td>
        <td>Value     </td>
        <td>Existence    </td>
        <td>A # followed by a name or integer. The name references a value in line 0, the header
 row. A number references a column by the 0-based column order.   </td>
        <td>
            <li/> #firstname
            </li> #3
        </td>
    </tr>
    <tr>
        <td>Equality</td>
        <td>Calculated when inside another type, otherwise True at assignment </td>
        <td>True at assignment, otherwise calculated   </td>
        <td>Two of the other types joined with an "=".</td>
        <td>
            @type_of_tree="Oak"
        </td>
    </tr>
<table>

    [ #common_name #0="field" @tail=end() not(in(@tail, 'short|medium')) ]

In the path above, the rules applied are:
- `#common_name` indicates a header named "common_name". Headers are the values in the 0th line.
- `#2` means the 3rd column, counting from 0
- A column reference with no equals or function is an existence test
- Functions and column references are ANDed together
- `@tail` creates a variable named "tail" and sets it to the value of the last column
- Functions can contain functions, equality tests, and/or literals

Most of the work of matching is done in functions. The match functions are:

| Function                      | What it does                                              |Done|
|-------------------------------|-----------------------------------------------------------|----|
| add(value, value, ...)        | adds numbers                                              | X  |
| after(value)                  | finds things after a date, number, string                 | X  |
| average(number, type)         | returns the average up to current "line", "scan", "match" | X  |
| before(value)                 | finds things before a date, number, string                | X  |
| concat(value, value)          | counts the number of matches                              | X  |
| count()                       | counts the number of matches                              | X  |
| count(value)                  | count matches of value                                    | X  |
| count_lines()                 | count lines to this point in the file                     | X  |
| count_scans()                 | count lines we checked for match                          | X  |
| divide(value, value, ...)     | divides numbers                                           | X  |
| end()                         | returns the value of the last column                      | X  |
| every(number, value)          | match every Nth time a value is seen                      |    |
| first(value)                  | match the first occurrence and capture line               | X  |
| in(value, list)               | match in a list                                           | X  |
| increment(value, n)           | increments a variable by n each time seen                 |    |
| isinstance(value, typestr)    | tests for "int","float","complex","bool","usd"            | X  |
| length(value)                 | returns the length of the value                           | X  |
| lower(value)                  | makes value lowercase                                     | X  |
| max(value, type)              | largest value seen up to current "line", "scan", "match"  | X  |
| median(value, type)           | median value up to current "line", "scan", "match"        | X  |
| min(value, type)              | smallest value seen up to current "line", "scan", "match" | X  |
| multiply(value, value, ...)   | multiplies numbers                                        | X  |
| no(value)                     | always false                                              | X  |
| not(value)                    | negates a value                                           | X  |
| now(format)                   | a datetime, optionally formatted                          | X  |
| or(value, value,...)          | match any one                                             | X  |
| percent(type)                 | % of total lines for "scan", "match", "line"              | X  |
| random(list)                  | pick from a list                                          |    |
| random(starting, ending)      | generates a random int from starting to ending            | X  |
| regex(regex-string)           | match on a regular expression                             | X  |
| subtract(value, value, ...)   | subtracts numbers                                         | X  |
| tally(value, value, ...)      | counts times values are seen, including as a set          | X  |
| then(y,m,d,hh,mm,ss,format)   | a datetime, optionally formatted                          |    |
| upper(value)                  | makes value uppercase                                     | X  |

# Not Ready For Production
Anything could change. This project is a hobby.













