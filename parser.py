import tokenizer
import shell


def parse_stmnt(tokens):
    if shell.commands.__contains__(tokens[0]):
        shell.commands[tokens[0]]()
    elif len(tokens) >= 3 and (type(tokens[0]) is str and tokens[1] == '='):  # identifier = expression
        name = tokens.pop(0)
        if (not (type(name) is str)) or tokenizer.BASE_TOKENS.__contains__(name):
            raise IOError("Invalid variable name, already used as a token")
        if shell.constants.__contains__(name):
            raise IOError("Invalid variable name, already used as constant")
        if shell.functions.__contains__(name):
            raise IOError("Invalid variable name, already used as function")
        tokens.pop(0)  # remove =
        val = parse_eq(tokens)
        shell.memory[name] = val
        shell.constants["ANS"] = val
        print(str(name) + " = " + str(val))
    else:
        val = parse_eq(tokens)
        shell.constants["ANS"] = val
        print("= " + str(val))


def parse_eq(tokens) -> float:
    v = parse_term(tokens)
    while True:
        try:
            if len(tokens) > 0:
                if tokens[0] in tokenizer.ADDOP:
                    op = tokens.pop(0)
                    nex = parse_term(tokens)
                    if op == "+":
                        v = v + nex
                    elif op == "-":
                        v = v - nex
                    else:
                        raise IOError("Invalid operation " + str(op) + ".")
                else:
                    raise IOError("Unexpected token \"" + str(tokens[0]) + "\"")
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
                if tokens[0] in tokenizer.MULOP:
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
                elif type(tokens[0]) is float or tokens[0] == '(' or shell.functions.__contains__(tokens[0]) \
                        or shell.memory.__contains__(tokens[0]) or shell.constants.__contains__(tokens[0]):
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
                if tokens[0] in tokenizer.POWOP:
                    op = tokens.pop(0)
                    nex = parse_value(tokens, False)
                    if op == "^":
                        v = v ** nex
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
            if shell.functions.__contains__(n):
                nex = parse_pow(tokens)
                return shell.functions[n](nex)
            elif shell.memory.__contains__(n):
                return shell.memory[n]
            elif shell.constants.__contains__(n):
                return shell.constants[n]
            else:
                raise IOError("Unrecognized function/variable \"" + str(n) + "\".")
        else:
            raise IOError("Invalid token " + str(tokens[0]) + ".")
    except IndexError:
        raise IOError("Unexpected end of expression.")


# statement                = expression | vardef
# vardef                   = IDENTIFIER, EQUALS, expression
#
# expression               = term, {addop, term}
# term                     = pow, {mulop, pow}
# pow                      = value, {expop, value }
# value                    = NUMBER | OPENPAREN, expression, CLOSEPAREN
#
# addop                    = PLUS | SUB
# mulop                    = MULT | DIVIDE
# expop                    = CARET




