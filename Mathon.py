import sys

from Node import *




if __name__ == "__main__":

    root = NumberNode(0)

    command = ""

    # get the initial command from the command line (skipping the program name...)
    for a in sys.argv[1:]:
        command += a

    print(command)
    print()

    # parenDepth is used to increase the precendence of operators that occur within parentheses
    parenDepth = 0

    while 1:
        root, parenDepth = processCommand(root, parenDepth, command)

        try:
            runningValue = root.evaluate()
        except:
            print("Error evaluating; try again")
            root = NumberNode(0)

        # print(parenDepth)
        # root.squawk()
        # print()

        # Don't "overcollapse": if parenDepth > 0, don't evaluate the contents of those parentheses
        root = root.collapse(parenDepth)
        # Show the current "running" tree, to which the user may append operations.
        print(root.squawk2(), end='', flush=True)

        try:
            command = sys.stdin.readline()
        except:
            print()
            print()
            print("Bye!")
            quit()
