import tokenizer
import shell
import parser

last_statement = "help"
program_running = True

if __name__ == "__main__":
    shell.clear_cmd()
    print("Type expressions, or \"help\" for info:")
    while program_running:
        statement = input("――――――――――――――――――――――――――――――――――――――――――――――――――\n")
        if len(statement) == 0:
            statement = last_statement
        else:
            last_statement = statement

        try:
            tks = tokenizer.tokenize(statement)
            if shell.memory["SHOW_TOKENS"]:
                print(tks)
            parser.parse_stmnt(tks)
        except IOError as e:
            print("Exception while parsing expression: \n" + str(e))
