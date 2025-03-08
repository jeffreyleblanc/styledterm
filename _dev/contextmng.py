
"""
Sketch of a setup that allows for class methods that can be used both as direct calls and `with`
"""


class Header:

    def __init__(self, main_class, text):
        self.main_class = main_class
        self.text = text
        self._entered = False

    def __enter__(self):
        self._entered = True
        self.main_class._ctx_depth += 1
        indent = ' ' * self.main_class._ctx_depth * 4  # Indentation by 4 spaces per level
        print(f"{indent}>>> {self.text}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.main_class._ctx_depth -= 1

    def __del__(self):
        if not self._entered:
            print(self.text)


class MainClass:
    def __init__(self):
        self._ctx_depth = 0

    # Works both for direct calls and with 'with' blocks
    def header(self, text):
        return Header(self, text)


# Example Usage:
main = MainClass()

# Example 1: Call header directly like a method
main.header("This is just a header")

# Example 2: Using header within the 'with' statement to manage indentation
with main.header("Step 1: Start processing"):
    print("post step 1")
    with main.header("Substep 1.1: Preprocessing"):
        print("post step 1.1")
    print("final")
