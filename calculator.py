import math

BASE_TOKENS = ["(", ")", "+", "-", "/", "*", "^"]
ADDOP = ["+", "-"]
MULOP = ["*", "/"]
POWOP = ["^"]
defined_functions = {
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "tan": lambda x: math.tan(x),
    "asin": lambda x: math.asin(x),
    "acos": lambda x: math.acos(x),
    "atan": lambda x: math.atan(x),
    "csc": lambda x: 1/math.sin(x),
    "sec": lambda x: 1/math.cos(x),
    "cot": lambda x: 1/math.tan(x),
    "acsc": lambda x: 1/math.asin(x),
    "asec": lambda x: 1/math.acos(x),
    "acot": lambda x: 1/math.atan(x),
    "abs": lambda x: abs(x),
    "sqrt": lambda x: math.sqrt(x),
    "rad": lambda x: math.radians(x),
    "deg": lambda x: math.degrees(x),
}


helpMsg = """
92      - Number
92.5    - Number
a+b     - Sum of a and b
a-b     - Difference of a and b
a*b     - Product of a and b
a/b     - Quotient of a and b
a^b     - a raised to the power of b
sin(x)  - Sin of x
cos(x)  - Cos of x
tan(x)  - Tan of x
csc(x)  - Csc of x
sec(x)  - Sec of x
cot(x)  - Cot of x
asin(x) - Arcsin of x
acos(x) - Arccos of x
atan(x) - Arctan of x
acsc(x) - Arccsc of x
asec(x) - Arcsec of x
acot(x) - Arccot of x
abs(x)  - Absolute value of x
sqrt(x) - Square root of x
rad(x)  - Degrees to radians
deg(x)  - Radians to degrees
"""


def tokenize(inp: str) -> list:
    out = []
    index = 0
    while index < len(inp):
        c = inp[index]
        if c in BASE_TOKENS:
            out.append(c)
        elif c.isnumeric() or c == ".":
            num = ""
            while index < len(inp) and (inp[index].isnumeric() or inp[index] == "."):
                num += inp[index]
                index += 1
            index -= 1
            try:
                out.append(float(num))
            except ValueError:
                raise IOError("Invalid number " + str(num) + ".")
        elif c.isalpha():
            ident = ""
            while index < len(inp) and inp[index].isalnum():
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
                        raise IOError("Invalid operation " + str(op) + ".")
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Unexpected end of expression.")
    return v


def parse_term(tokens) -> float:
    v = parse_pow(tokens)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in MULOP:
                    op = tokens.pop(0)
                    nex = parse_pow(tokens)
                    if op == "*":
                        v = v * nex
                    elif op == "/":
                        if nex != 0:
                            v = v / nex
                        else:
                            raise IOError("Division by zero.")
                    else:
                        raise IOError("Invalid operation " + str(op) + ".")
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Unexpected end of expression.")
    return v


def parse_pow(tokens) -> float:
    v = parse_value(tokens)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in POWOP:
                    op = tokens.pop(0)
                    nex = parse_term(tokens)
                    if op == "^":
                        v = math.pow(v, nex)
                    else:
                        raise IOError("Invalid operation " + str(op) + ".")
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Unexpected end of expression.")
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
        elif type(n) is str:
            if defined_functions.__contains__(n):
                nex = parse_pow(tokens)
                return defined_functions[n](nex)
            else:
                raise IOError("Unrecognized function \"" + str(n) + "\".")
        else:
            raise IOError("Invalid token " + str(tokens[0]) + ".")
    except IndexError:
        raise IOError("Unexpected end of expression.")


print("Type expressions, or \"help\" for info:")
while True:
    statement = input("――――――――――――――――――――――――――――――――――――――――――――――――――\n")
    if len(statement) > 0:
        if statement == "help":
            print(helpMsg)
        else:
            try:
                tks = tokenize(statement)
                output = parse_eq(tks)
                print("= " + str(output))
            except IOError as e:
                print("Exception while parsing expression: \n" + str(e))
    else:
        break

