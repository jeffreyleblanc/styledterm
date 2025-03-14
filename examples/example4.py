#! /usr/bin/env python3

# SPDX-FileCopyRightText: Copyright (c) 2025-present Jeffrey LeBlanc
# SPDX-License-Indentifier: MIT
# example4.py

from styledterm import tprint

tprint("Heading 1").h1()
tprint("test1").red().bold()
tprint("test1").cyan().underline()
tprint("test1").white().italic().underline()

tprint("Heading 2").red().h2()
tprint("test2").magenta().lite()

tprint("Heading 3").green().h3()
tprint("test3").yellow().italic().underline()

tprint("Heading 4").h4()
tprint("test4")

tprint("Heading F").hf()
tprint("test5").blink()
