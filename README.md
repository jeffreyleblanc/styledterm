# Styled Term

Simple but effective styling for python in the terminal.

This is **not** intended to be as feature rich as something like [Rich](https://github.com/Textualize/rich),
but is intentionally designed for supporting easier to read output from python programs that produce a
"stream" of output on the command line.

A motivation for this library is to support easier to read output from scripts with multiple
and nested steps.


## 1. Installation

The [Releases Page](https://github.com/jeffreyleblanc/styledterm/releases) contains:

* `.deb` files ( `dpkg -i NAME.deb` )
* `sdist` and `whl` python packages

sytledterm currently has no dependencies outside the python standard library.


## 2. Simple Example

To try the examples, from top directory:

```sh
$ PYTHONPATH=. examples/example5.py
```

The following show *some* of the functionality:

```python
from styledterm import StyledTerminalPrinter

P = StyledTerminalPrinter(default_header_color={"H1":"blue2","H4":"blue"})
P.default_header_center = False
P.curr_auto_indent_level = 1

P.H1("Example Set One")

P.H4("Using .p with a leading style block")
P.p("Plain text")
P.p("[red]Some red text")
P.p("[magenta2 reverse italic]Some fancy magenta2 text")

P.H4("Using .p with kwargs")
P.p("Some red text",color="red")
P.p("Some fancy magenta2 text",color="magenta2",styles=["reverse","italic"])
P.p("printing a json object:")
P.pjson({"a":123,"b":456,"c":{"d":1,"e":2}},color="cyan2")

P.H4("Using .pp for sophisticated text")
text = "Colors like [yellow]yellow[/] and [yellow2][bold]YELLOW2[/] are [cyan][italic]easy[/]"
P.pp(text)

P.H4("Using direct color name shortcuts")
P.red("red shortcut!")
P.nl()
P.magenta2("magenta2 shortcut!")
P.nl()
P.cyan2("cyan2 shortcut BOLD!",bold=True)
P.nl()
```

![Image of the above code in the terminal](./images/example1-screenshot.png)

See the example files for additonal usage.


## 3. Usage API

Constructor options for `StyledTerminalPrinter`:

```python
force_width = None | int    # Forces the width of the printer
use_styles = bool           # Default True, if False will print with no styling
autonewlines = True,        # Default True, if True puts newlines around P.Hx statements
default_header_color = None
    # Or any other color string
    "blue"
    # A dictionary with keys for the headers
    # "H" is a default for all headers, to make a specific entry "H2", "H3", etc..
    { "H": "blue", "H2": "red" }
```

Colors and Styles:

```python
# Default colors
black
red
green
yellow
blue
magenta
cyan
white
# For each color you can implement the 'bright' color with 2, e.g.
red2

# Styles
bold
lite
italic
underline
blink
reverse
```

Methods:

```python
# Insert a newline
nl()

# Basic print
p("text",color="COLOR",styles=["STYLE1",...])
p("[COLOR STYLE1...]text")

# Print annotated string
pp("[red][bold]text[/]")
# Each color and style is within [], and can close a style with [/]
# If no closing [/], styles to the end of the string

# Headers
P.H1
P.H2
P.H3
P.H4
P.HF    # This uses reverse text

# Sections that can be used with `with`, e.g.
with P.S1("This is the top section"):
    P.p("hello")
    with P.S4("Here is a sub section"):
        P.p("hi again")

# Print horizontal line
P.line

# Printing json or pure object
pjson(obj)
pobj(obj)   # uses pprint.pformat

# Input line with annotated string
P.ppinput
```
