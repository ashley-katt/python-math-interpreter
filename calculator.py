import tokenizer
import shell
import parser

if __name__ == "__main__":
    print("Type expressions, or \"help\" for info:")
    while True:
        statement = input("――――――――――――――――――――――――――――――――――――――――――――――――――\n")
        if len(statement) > 0:
            try:
                tks = tokenizer.tokenize(statement)
                if shell.memory["SHOW_TOKENS"]:
                    print(tks)
                output = parser.parse_stmnt(tks)
            except IOError as e:
                print("Exception while parsing expression: \n" + str(e))
        else:
            break
