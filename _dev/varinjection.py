
"""
Sketch of a setup that allows for class methods that can be used both as direct calls and `with`
"""

from styledterm import StyledTerminalPrinter

class InjectPrinter(StyledTerminalPrinter):

    def set_local_methods(self,*args):
        lst = []
        for method_name in args:
            meth = getattr(self,method_name)
            if not callable(meth):
                raise Exception(f"'{method_name}' is not a callable")
            lst.append(meth)
        return lst

    def inject2(self, _locals, *args):
        # This avenue doesn't work
        print("??",_locals)
        for n in args:
            if n not in _locals:
                print("Setting",n)
                _locals[n] = getattr(self,n)
            else:
                raise KeyError(f"Cannot overwrite locals: {n}")

def main():
    P = InjectPrinter()

    H1,H3,pp = P.set_local_methods("H1","H3","pp")
    H1("Header 1")
    H3("Header 3")
    pp("[green2]something green")

    # P.inject2(locals(),"pjson")
    # pjson(dict(a=1,b=2))

if __name__ == "__main__":
    main()

