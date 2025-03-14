import sys
from styledterm import StyledTerminalPrinter

P = StyledTerminalPrinter()

sys.stdout.write("Hello")
sys.stdout.write(P.s("[red]red"))
sys.stdout.write(P.s("[blue]blue"))

# Fails: Only one argument is taken
# sys.stdout.write("Hello","Bye")
