import json
from inspect import stack
from colorama import Fore, Back, Style

# ctrl + shift + p = all commands, fold all

def endline(*args):
    # Prints in a special format
    statements = []
    for arg in args:
        if type(arg) == str:
            statements.append(arg.upper())
        else:
            statements.append(arg)

    print("\t", Fore.LIGHTWHITE_EX, Back.RED, "^^^^^^^^^^ ", *statements, " ^^^^^^^^^^", Style.RESET_ALL, "\n")

def debug(*args, title=None):
    # Prints in a special format to more easily find a printed statement for debugging
    # The stack portion grabs the line number in the code of the printed message and the file name
    # print(dir(stack()[1].frame))
    scope = stack()[1]
    lineno = scope.lineno
    filename = scope.filename

    if len(args) == 1: is_single_item = True
    else: is_single_item = False

    if is_single_item:
        item = args[0]
        item_type = type(item)
        # Dictionary and list formatting
        if item_type is dict or item_type is list: print_me = "Dictionary or Array with " + str(len(item)) + " items \n" + json.dumps(item, indent=4)
        # String formatting
        if item_type is str: print_me = item
        else: print_me = item
    else: print_me = args

    if is_single_item:
        if title == None:
            print("\n\t", Fore.RED, "\033[4m", "LINE NUMBER: {} | FILE NAME: {}".format(lineno, filename), Style.RESET_ALL, "\n", Fore.RED, print_me, Style.RESET_ALL, "\n")
        else:
            print("\n", Fore.RED, "\033[4m{}\tLINE NUMBER: {} | FILE NAME: {}".format(title, lineno, filename), Style.RESET_ALL, "\n", Fore.RED, print_me, Style.RESET_ALL, "\n")
    else:
        if title == None:
            print("\n\t", Fore.RED, "\033[4m", "LINE NUMBER: {} | FILE NAME: {}".format(lineno, filename), Style.RESET_ALL, "\n", Fore.RED, *print_me, Style.RESET_ALL, "\n")
        else:
            print("\n", Fore.RED, "\033[4m{}\tLINE NUMBER: {} | FILE NAME: {}".format(title, lineno, filename), Style.RESET_ALL, "\n", Fore.RED, *print_me, Style.RESET_ALL, "\n")

def title(*args):
    # Prints in a special format
    statements = []
    for arg in args:
        if type(arg) == str:
            statements.append(arg.upper())
        else:
            statements.append(arg)

    print("\n\t", Style.BRIGHT, Fore.WHITE, Back.GREEN, "-----=====", *statements, " =====-----", Style.RESET_ALL)

def startup(*args):
    print(Fore.YELLOW, *args, Style.RESET_ALL)

def info(arg):
    print(Fore.CYAN, "Type:" + str(type(arg)) + "\n", *dir(arg), Style.RESET_ALL, sep="\n")

if __name__ == "__main__":
    endline("End line test", "big boy", type("yes sir"), 12)
    debug("Just you know, testing the debug command right now", title="Title")
    debug("Just you know,", "testing the debug command right now")
    debug({"Test": 3, "Test2": 5})
    title("Title test")
    startup("This is some start up text, beep boop")
    info(stack)
