#! /usr/bin/env python3

# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# example3.py

from styledterm import StyledTerminalPrinter


def main():
    P = StyledTerminalPrinter(default_header_color="green")

    P.H1("Without with")

    with P.S1("With 1"):
        P.p("[blue2]Some stuff")

        with P.S1("With 2"):
            P.p("[red2]Some stuff")

        P.p("finish")

    P.line()
    P.line()
    P.line()

    with P.S("s1"):
        with P.S("s2"):
            with P.S("s3"):
                with P.S("s4"):
                    with P.S("s5"):
                        with P.S("s6"):
                            P.p("bottom")
            with P.S("s3b"):
                P.p("next")
    with P.S("s1b"):
        P.p("Back on top")

if __name__ == "__main__":
    main()
