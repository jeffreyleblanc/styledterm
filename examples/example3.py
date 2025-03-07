#! /usr/bin/env python3

# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# example3.py

from styledterm import StyledTerminalPrinter


def main():
    P = StyledTerminalPrinter(default_header_color="green")

    # Example of using fragmentary output
    P.v(P.s("[yellow2 bold]Part1"),P.a("white [green]=>[/] [blue]blue[/]"),"plain")

if __name__ == "__main__":
    main()
