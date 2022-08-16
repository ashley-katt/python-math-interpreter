BASE_TOKENS = ["(", ")", "+", "-", "/", "*", "^", "="]
ADDOP = ["+", "-"]
MULOP = ["*", "/"]
POWOP = ["^"]


def tokenize(inp: str) -> list:
    out = []
    index = 0
    while index < len(inp):
        c = inp[index]
        if c.isnumeric() or c == ".":
            num = ""
            while index < len(inp) and (inp[index].isnumeric() or inp[index] == "."):
                num += inp[index]
                index += 1
            index -= 1
            try:
                f = float(num)
                out.append(f)
            except ValueError:
                raise IOError("Invalid number " + str(num) + ".")
        elif c in BASE_TOKENS:
            out.append(c)
        elif c.isalpha():
            ident = ""
            while index < len(inp) and (inp[index].isalpha() or inp[index] == "_"):
                ident += inp[index]
                index += 1
            index -= 1
            out.append(str(ident))
        elif c.isspace():
            pass  # Do nothing if it's a space
        else:
            raise IOError("Invalid character \"" + str(c) + "\".")
        index += 1
    return out
