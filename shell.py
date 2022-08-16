import math


memory = {
    "SHOW_TOKENS": 0
}
constants = {
    "PI": math.pi,
    "TAU": math.tau,
    "E": math.e,
    "TRUE": 1,
    "FALSE": 0,
}


def help_cmd():
    print(helpMsg)


def memory_cmd():
    for m in memory:
        print(str(m) + " = " + str(memory[m]))


commands = {
    "help": help_cmd,
    "memory": memory_cmd,
}

functions = {
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "tan": lambda x: math.tan(x),
    "asin": lambda x: math.asin(x),
    "acos": lambda x: math.acos(x),
    "atan": lambda x: math.atan(x),
    "csc": lambda x: 1 / math.sin(x),
    "sec": lambda x: 1 / math.cos(x),
    "cot": lambda x: 1 / math.tan(x),
    "acsc": lambda x: 1 / math.asin(x),
    "asec": lambda x: 1 / math.acos(x),
    "acot": lambda x: 1 / math.atan(x),
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
