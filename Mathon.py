import sys

from Node import *


def processCommand(origRoot, origParenDepth, command):
    # clone off the original info.
    # if there is an error, we'll return the original.
    root = origRoot.clone()
    parenDepth = origParenDepth

    first = True
    try:
        for k in command:
            if k in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                if first and isinstance(root, NumberNode):
                    # restart the formula
                    root = NumberNode(int(k))
                else:
                    # continue the formula
                    root = root.append(NumberNode(int(k)))
            elif k == '.':
                root = root.appendDecimalPoint()
            elif k == '+':
                root = root.append(AdditionOperatorNode(parenDepth))
            elif k == '-':
                root = root.append(SubtractionOperatorNode(parenDepth))
            elif k == 'x':
                root = root.append(MultiplicationOperatorNode(parenDepth))  # preferred symbol for multiply
            elif k == '*':
                root = root.append(MultiplicationOperatorNode(parenDepth))  # allowed alternative symbol for multiply
            elif k == '/':
                root = root.append(DivisionOperatorNode(parenDepth))
            elif k == '%':
                root = root.append(ModuloOperatorNode(parenDepth))
            elif k == '^':
                root = root.append(ExponentiationOperatorNode(parenDepth))
            elif k == '(':
                parenDepth += 1
                if first and isinstance(root, NumberNode):
                    # restart the formula
                    # We need an operator to hold the parenthesized atom as a right child.
                    # we could just use the AdditionOperatorNode, but then the printout would look
                    # wrong: "4+3" ==> "0+4+3", or "(2x3)" ==> "0+(2x3)"
                    # We use the "Right" pseudo-operator, that only prints and evaluates its right side.
                    parenDepth = 1
                    root = NumberNode(0)
                    root = root.append(RightOperatorNode(0))
                root = root.append(ParenthesisNode(parenDepth))
            elif k == ')':
                if parenDepth > 0:
                    root = root.closeParen(parenDepth)
                    parenDepth -= 1
                else:
                    print(") error")
                    raise InvalidOperatorSequenceError()

            first = False
    except:
        print("Error; try again")
        return origRoot, origParenDepth

    return root, parenDepth


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
