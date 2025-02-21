# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# terminalprinter.py


import textwrap
from os import get_terminal_size
from math import floor,ceil
import pprint
import re
from functools import partial, wraps
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class StyledTerminalPrinter:

    def __init__(self, force_width=None, use_styles=True, autonewlines=True, default_header_color=None):
        # Determine the width of the terminal
        try:
            """
            If you pipe to less for example, you get an error.
            For now, we just set a default width in that case.
            """
            s = get_terminal_size()
            self.width = s.columns
        except Exception as e:
            self.width = 80

        if force_width is not None:
            self.width = force_width

        # Set if we should actually print with styles
        self.use_styles = use_styles

        # Enable auto newlines around headers etc
        self.autonewlines = autonewlines
        self.last_had_newline = False

        # Default Header Color
        self.default_header_color = default_header_color
        self.default_header_center = False

        # Setup ANSI codes and method shortcuts
        self._setup_ansi_codes()
        self._setup_direct_color_methods()

        self.supress_auto_indent = False
        self.curr_auto_indent_level = 0


    #-- Setup Methods --------------------------------------------------------#

    def _setup_ansi_codes(self):
        # https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
        self.BASE_COLORS = dict(
            black = 0,
            red = 1,
            green = 2,
            yellow = 3,
            blue = 4,
            magenta = 5,
            cyan = 6,
            white = 7
        )
        self.COLORS = {}
        for k,v in self.BASE_COLORS.items():
            self.COLORS[k] = f"3{v}"
            self.COLORS[k+"2"] = f"9{v}"

        self.STYLES = dict(
            bold = "1",
            lite = "2",
            italic = "3",
            underline = "4",
            blink = "5",
            reverse = "7"
        )

    def _setup_direct_color_methods(self):
        # Sets up `P.red("hello")`, `P.cyan2("hello")`, etc...
        for color in self.COLORS.keys():
            setattr(self,color,partial(self.p,color=color))


    #-- Core Printing API ----------------------------------------------------------------#

    #==> set_global_indent?

    def autonewlinewrapper(meth):
        @wraps(meth)
        def wrapper(self, *args, **kwargs ):
            if self.autonewlines and not self.last_had_newline:
                print("")
            # Apply default color for headers
            meth_name = meth.__name__
            if (
                meth_name.startswith("H") and
                ( "color" not in kwargs or kwargs["color"] is None )
            ):
                if isinstance(self.default_header_color,str):
                    kwargs["color"] = self.default_header_color
                elif isinstance(self.default_header_color,dict):
                    meth_frag = meth_name[:2]
                    if meth_frag in self.default_header_color:
                        kwargs["color"] = self.default_header_color[meth_frag]
                    elif "H" in self.default_header_color:
                        kwargs["color"] = self.default_header_color["H"]

            if meth_name.startswith("H"):
                self.supress_auto_indent = True
            meth(self,*args,**kwargs)
            if meth_name.startswith("H"):
                self.supress_auto_indent = False

            if self.autonewlines:
                print("")
            self.last_had_newline = True
        return wrapper

    def nl(self):
        print("")

    def p(self, text, color=None, styles=None, bold=False):
        # If no styles in the kwargs, check if starts with a style tag
        if color is None and styles is None:
            if text.startswith("["):
                idx = text.find("]")
                if idx > -1:
                    _style = text[1:idx]
                    text = text[idx+1:]
                    parts = _style.split(" ")
                    for part in parts:
                        if part in self.COLORS:
                            color = part
                        if part in self.STYLES:
                            if styles is None: styles = []
                            styles.append(part)
        # Set for bold
        if bold:
            if styles is None:
                styles = ["bold"]
            elif "bold" not in styles:
                styles.append("bold")

        # Style and print
        if self.use_styles:
            text = self.wrap_in_style(text=text,color=color,styles=styles)
            if not self.supress_auto_indent and self.curr_auto_indent_level > 0:
                text = self.txt_indent(text,indent=(4*self.curr_auto_indent_level))
        print(text)
        self.last_had_newline = False


    def pp(self, annotated_text):
        """
        Support for:
            "From [green]here[/] to [red]there[/] we go"
            "[red][bold]Pay Attention!"
        Styled text
        """

        # Make a regex to find the `[COLOR][STYLE]` and `[/]` markers
        markers = list(self.BASE_COLORS.keys()) + list(self.STYLES.keys()) + ["/"]
        pattern = rf"(\[(?:{'|'.join(markers)})2?\])"

        # Split the text by regex matches
        parts = re.split(pattern,annotated_text)

        # Walk the split text assembling the final string
        text = ""
        curr_text = None
        curr_color = None
        curr_styles = []
        for part in parts:
            if part == "":
                continue

            if part.startswith("[") and part.endswith("]"):
                code = part[1:-1]
                if code == "/":
                    text += self.wrap_in_style(text=curr_text,color=curr_color,styles=curr_styles)
                    curr_color = None
                    curr_text = None
                    curr_styles = []
                elif code in self.COLORS:
                    curr_color = code
                elif code in self.STYLES:
                    curr_styles.append(code)
                else:
                    raise Exception(f"Unknown formatting code: '{code}'")
            else:
                if curr_color is None:
                    text += part
                else:
                    curr_text = part
        if curr_text is not None:
            # Allows us to not need to end with [/], can be implied
            text += self.wrap_in_style(text=curr_text,color=curr_color,styles=curr_styles)

        if not self.supress_auto_indent and self.curr_auto_indent_level > 0:
            text = self.txt_indent(text,indent=(4*self.curr_auto_indent_level))

        print(text)
        self.last_had_newline = False


    #-- Shortcuts ----------------------------------------------------------------#

    def _default_center(self, center):
        return center if center is not None else self.default_header_center

    @autonewlinewrapper
    def H1(self, text, center=None, color=None, bold=True):
        center = self._default_center(center)
        self.p(self.txt_head(text,center=center),color=color,bold=bold)

    @autonewlinewrapper
    def H2(self, text, center=None, color=None, bold=True):
        center = self._default_center(center)
        self.p(self.txt_head(text,center=center,char="-"),color=color,bold=bold)

    @autonewlinewrapper
    def H3(self, text, center=None, color=None, bold=True):
        center = self._default_center(center)
        meth = self.txt_center_pad if center else self.txt_left_offset_pad
        self.p(meth(text,char="="),color=color,bold=bold)

    @autonewlinewrapper
    def H4(self, text, center=None, color=None, bold=True):
        center = self._default_center(center)
        meth = self.txt_center_pad if center else self.txt_left_offset_pad
        self.p(meth(text,char="-"),color=color,bold=bold)

    @autonewlinewrapper
    def HF(self, text, center=None, color="black2"):
        center = self._default_center(center)
        t = self.txt_center(text) if center else self.txt_left_offset_pad(text,char=" ")
        self.p(t,color=color,styles=["reverse"])

    # line and object printer helpers

    @autonewlinewrapper
    def line(self, char="-", color=None, bold=None):
        self.p(self.txt_hr(char=char),color=color,bold=bold)

    @autonewlinewrapper
    def pobj(self, obj, obj_indent=4, color=None):
        s = self.txt_object(obj,indent=obj_indent)
        self.p(s,color=color)

    @autonewlinewrapper
    def pjson(self, obj, obj_indent=4, color=None):
        s = json.dumps(obj,indent=obj_indent)
        self.p(s,color=color)

    #-- Color/Style Tools ---------------------------------------------------------#

    def wrap_in_style(self, text=None, color=None, styles=None):
        if not self.use_styles:
            return text

        if color is None and ( styles is None or len(styles)==0 ):
            return text
        else:
            code = ""
            if color is not None:
                code += self.COLORS[color]
            if styles is not None and len(styles)>0:
                code += f";{';'.join([self.STYLES[s] for s in styles])}"
            return f"\x1b[{code}m{text}\x1b[0m"


    #-- Text Formating Tools ------------------------------------------------#

    def txt_indent(self, text, indent=4):
        return textwrap.indent(text, prefix=" "*indent)

    def txt_hr(self, char="="):
        return char*self.width

    def txt_center(self, text):
        tl = len(text)
        n = 0.5 * ( self.width - tl )
        if n < 0: n = 0
        return f"{' '*floor(n)}{text}{' '*ceil(n)}"

    def txt_center_pad(self, text, char="-"):
        tl = len(text)
        n = 0.5 * ( self.width - tl )
        n -= 1
        if n < 0: n = 0
        return f"{char*floor(n)} {text} {char*ceil(n)}"

    def txt_left_offset_pad(self, text, offset=2, char="-"):
        tl = len(text)
        n = self.width - (tl + offset + 2)
        if n < 0: n = 0
        line = f"{char*offset} {text} {char*ceil(n)}"
        return line

    def txt_head(self, text, char="=", center=False):
        hr = self.txt_hr(char=char)
        if center:
            return f"{hr}\n{self.txt_center(text)}\n{hr}"
        else:
            return f"{hr}\n   {text}\n{hr}"

    def txt_object(self, object, indent=4):
        return pprint.pformat(object,indent=indent)


class tprint(StyledTerminalPrinter):
    """
    Provides a subset of functionality from :class:`SimpleTerminalPrinter`,
    but adds function chaining.

    Intended as a short-lifetime object that internally handles formatting
    and prints when :meth:`tprint.__del__` is called automatically.
    """
    def __init__(self, /, line=None, *, auto_print=True, **kwargs):
        super().__init__(**kwargs)
        logging.debug("init super done")
        self.auto_print = auto_print
        self.line = line
        self.color = None
        self.styles = []

        for color in self.COLORS.keys():
            setattr(self, color, partial(self._inner, "color", color))
        for style in self.STYLES.keys():
            setattr(self, style, partial(self._inner, "style", style))

        logging.debug("init tprint done")

    def __del__(self):
        if self.auto_print:
            self.p(self.line, self.color, self.styles)
        logging.debug("tprint destroyed")

    def _inner(self, stype, name):
        if stype == "color":
            if self.color:
                raise ValueError("Color is already set")
            self.color = name
        elif stype == "style":
            self.styles.append(name)
        return self

    def print(self):
        print(self.line)
