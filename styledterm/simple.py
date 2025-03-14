# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# simple.py

from os import get_terminal_size

class SimpleTerminalPrinter:
    """
    The purpose of this class is to serve as a template for simple custom dropins
    """

    def __init__(self):
        try:
            s = get_terminal_size()
            self.width = s.columns
        except Exception as e:
            self.width = 80

    def line(self, char="-"):
        return char*self.width

    def p(self, text=''):       print(text)
    def bold(self, text):       print(f"\x1b[1m{text}\x1b[0m")
    def red(self, text):        print(f"\x1b[31m{text}\x1b[0m")
    def yellow(self, text):     print(f"\x1b[93m{text}\x1b[0m")
    def blue(self, text):       print(f"\x1b[38;5;27m{text}\x1b[0m")
    def cyan(self, text):       print(f"\x1b[36m{text}\x1b[0m")
    def green(self, text):      print(f"\x1b[92m{text}\x1b[0m")
    def gray(self, text):       print(f"\x1b[38;5;239m{text}\x1b[0m")
    def redbold(self, text):    print(f"\x1b[31;1m{text}\x1b[0m")

