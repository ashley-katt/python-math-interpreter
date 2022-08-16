import math

BASE_TOKENS = ["(", ")", "+", "-", "/", "*", "^", "="]
ADDOP = ["+", "-"]
MULOP = ["*", "/"]
POWOP = ["^"]
memory = {
    "SHOW_TOKENS": 0
}


def help_cmd():
    print(helpMsg)


def memory_cmd():
    for m in memory:
        print(str(m) + " = " + str(memory[m]))


shell_functions = {
    "help": help_cmd,
    "memory": memory_cmd,
}


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

Commands:
  help         - Displays this message
  memory       - Shows all variables in memory

Math Functions:
  a+b, a-b, a*b, a/b, a^b
  sin(x), cos(x), tan(x), csc(x), sec(x), cot(x), 
  asin(x), acos(x), atan(x), acsc(x), asec(x), acot(x), 
  abs(x), sqrt(x), rad(x), deg(x)

Special Variables:
  SHOW_TOKENS  - If nonzero, will show the found tokens after parsing an expression.
"""


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


def parse_stmnt(tokens):
    if shell_functions.__contains__(tokens[0]):
        shell_functions[tokens[0]]()
    elif len(tokens) >= 3 and (type(tokens[0]) is str and tokens[1] == '='):  # identifier = expression
        name = tokens.pop(0)
        if defined_functions.__contains__(name):
            raise IOError("Invalid variable name, already used as function")
        tokens.pop(0)  # remove =
        val = parse_eq(tokens)
        memory[name] = val
        print(str(name) + " = " + str(val))
    else:
        print("= " + str(parse_eq(tokens)))


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
                elif type(tokens[0]) is float or tokens[0] == '(' or \
                        defined_functions.__contains__(tokens[0]) or memory.__contains__(tokens[0]):
                    nex = parse_pow(tokens)
                    v = v * nex
                else:
                    break
            else:
                break
        except IndexError:
            raise IOError("Unexpected end of expression.")
    return v


def parse_pow(tokens) -> float:
    v = parse_value(tokens, True)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in POWOP:
                    op = tokens.pop(0)
                    nex = parse_value(tokens, False)
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


def parse_value(tokens, begin: bool) -> float:
    try:
        n = tokens.pop(0)
        if type(n) is float:
            return n
        if begin and n == '-':
            return -tokens.pop(0)
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
            elif memory.__contains__(n):
                return memory[n]
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
        try:
            tks = tokenize(statement)
            if memory["SHOW_TOKENS"]:
                print(tks)
            output = parse_stmnt(tks)
        except IOError as e:
            print("Exception while parsing expression: \n" + str(e))
    else:
        break
