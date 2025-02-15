#! /usr/bin/env python3

# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# example2.py

from styledterm import StyledTerminalPrinter


def main():
    P = StyledTerminalPrinter(default_header_color="green")

    for center in (True,False):
        P.default_header_center = center
        if center is False:
            P.default_header_color = {
                "H": "blue2",
                "H2":"magenta2",
                "H3":"black2",
                "H4":"yellow2",
                "HF": "cyan2"
            }

        P.H1("Example Set One")
        P.H2("Example Set One")
        P.H3("Example Set One")
        P.H4("Example Set One")
        P.HF("Example Set One")

if __name__ == "__main__":
    main()
