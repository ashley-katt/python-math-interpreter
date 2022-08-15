BASE_TOKENS = ["(", ")", "+", "-", "/", "*"]
ADDOP = ["+", "-"]
MULOP = ["*", "/"]


def tokenize(inp: str) -> list:
    out = []
    index = 0
    while index < len(inp):
        c = inp[index]
        if c in BASE_TOKENS:
            out.append(c)
        elif c.isnumeric():
            num = ""
            while index < len(inp) and (inp[index].isnumeric() or inp[index] == "."):
                num += inp[index]
                index += 1
            index -= 1
            try:
                out.append(float(num))
            except ValueError:
                raise IOError("Invalid number")
        elif c.isspace():
            pass  # Do nothing if it's a space
        else:
            raise IOError("Invalid character")
        index += 1
    return out


def parse_eq(tokens) -> float:
    v = parse_term(tokens)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in ADDOP:
                    op = tokens.pop(0)
                    nex = parse_term(tokens)
                    if op == "+":
                        v = v + nex
                    elif op == "-":
                        v = v - nex
                    else:
                        raise IOError("Invalid operation")
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Expected value - Found none")
    return v


def parse_term(tokens) -> float:
    v = parse_value(tokens)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in MULOP:
                    op = tokens.pop(0)
                    nex = parse_value(tokens)
                    if op == "*":
                        v = v * nex
                    elif op == "/":
                        v = v / nex
                    else:
                        raise IOError("Invalid operation")
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Expected value - Found none")
    return v


def parse_value(tokens) -> float:
    try:
        n = tokens.pop(0)
        if type(n) is float:
            return n
        elif n == "(":
            inner = []
            nest = 1
            while nest > 0:
                nex = tokens.pop(0)
                if nex == "(":
                    nest += 1
                elif nex == ")":
                    nest -= 1
                if nest > 0:
                    inner.append(nex)
            return parse_eq(inner)
        else:
            raise IOError("Invalid token - Expected Expression")
    except IndexError:
        raise IOError("Unexpected end of expression")


while True:
    statement = input("ENTER EQUATION:\n")
    if len(statement) > 0:
        tks = tokenize(statement)
        output = parse_eq(tks)
        print("= " + str(output))
    else:
        break

