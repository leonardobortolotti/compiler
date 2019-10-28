import string
import sys


def split_token_from_array(string, print_line):

    text = string

    tokens_array = []

    token = ''

    mark_special_symbol = False

    symbol_mark = False

    for line in text:

        if line[0] == "#":
            continue

        char_index = -1

        for char in line:

            char_index += 1

            if char.isspace():
                token = ''
                continue

            if symbol_mark:
                symbol_mark = False
                continue

            if char == "\"" and mark_special_symbol:
                print_symbol("\"", "simbolo especial") if print_line else False
                tokens_array.append("\"")
                mark_special_symbol = False
            elif char == "\"":
                print_symbol("\"", "simbolo especial") if print_line else False
                tokens_array.append("\"")
                mark_special_symbol = True

            if mark_special_symbol:
                continue

            if char_index + 1 < len(line):
                next_token = line[char_index + 1]
            else:
                next_token = " "

            if char in language_symbols:

                symbol_mark = True

                if next_token == "=" and char == ">":
                    token_symbol = ">="
                elif next_token == "=" and char == "<":
                    token_symbol = "<="
                elif next_token == "=" and char == "=":
                    token_symbol = "=="
                elif next_token == "=" and char == "+":
                    token_symbol = "+="
                elif next_token == "=" and char == "-":
                    token_symbol = "-="
                else:
                    symbol_mark = False
                    token_symbol = char

                print_symbol(token_symbol, "simbolo especial") if print_line else False
                tokens_array.append(token_symbol)
            elif char in language_letters:

                token += char

                if next_token not in language_letters:

                    if token in language_words:
                        print_symbol(token, "palavra reservada") if print_line else False
                        tokens_array.append(token)
                        token = ''
                    else:
                        print_symbol(token, "identificador") if print_line else False
                        tokens_array.append(token)
                        token = ''

            elif char in language_digits:

                token += char

                if next_token in language_letters:
                    print("erro")
                elif next_token not in language_digits:
                    print_symbol(token, "constante inteira") if print_line else False
                    tokens_array.append(token)

    file.close()

    print(tokens_array)
    return tokens_array


def print_symbol(token, type):
    print(type, token)


if __name__ == '__main__':

    syntactic_table = {
        "E": {
            "id": "ST",
            "num": "ST",
            "(": "ST",
        },
        "T": {
            "id": "GF",
            "num": "GF",
            "(": "GF",
        },
        "S": {
            "+": "ST+",
            "-": "ST-",
            ")": "VAZIO",
            "$": "VAZIO",
        },
        "G": {
            "+": "VAZIO",
            "-": "VAZIO",
            "*": "GF*",
            "/": "GF/",
            ")": "VAZIO",
            "$": "VAZIO",
        },
        "F": {
            "id": "id",
            "num": "num",
            "(": ")E(",
        }
    }

    rules = ["E", "T", "S", "G", "F"]
    language_symbols = ["[", "]", "<", ">", "<=", "+", ";", "=", "{", "}", "(", ")", "*", ".", "#", "%", ",", "/"]
    language_letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    language_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    language_words = ["main", "int", "float", "char", "printf", "if", "typedef", "void", "switch", "while",
                      "case", "break", "return", "puts", "scanf", "fopen", "FILE", "null", "exit", "gets"]

    file = open('code_in_c.txt', 'r')
    text = file.readlines()

    tokens_array = split_token_from_array(text, True)

    index_token = 0
    repeat = True
    tokens_array.append("$")
    table_recognize = ["$", "E"]

    while repeat:
        current_token = tokens_array[0]
        table_recognize_top = table_recognize[-1]
        print("----------------------------------------------------------------------")
        print("PILHA  |", table_recognize, "|")
        print("CADEIA |", tokens_array, "|")

        if table_recognize_top not in rules or table_recognize_top == "$":

            if table_recognize_top == current_token:

                tokens_array.pop(0)
                table_recognize.pop()
                if table_recognize_top == "$":
                    print("Sucesso")
                else:
                    current_token = tokens_array[0]
            else:
                print("Erro")
                sys.exit()
        else:
            if current_token in syntactic_table[table_recognize_top]:
                table_recognize.pop()

                rule_value = syntactic_table[table_recognize_top][current_token]
                print("REGRA  |", table_recognize_top, "->", rule_value, "|")
                if rule_value == "VAZIO":
                    continue
                if table_recognize_top == "F" and current_token != "(":

                    table_recognize.append(rule_value)
                else:
                    array_rule = split_token_from_array(rule_value, False)

                    for token in array_rule:
                        table_recognize.append(token)

            else:
                print("Erro")
                sys.exit()

        if table_recognize_top == "$":
            repeat = False


