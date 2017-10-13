
__all__ = [
    'InvalidOperatorSequenceError',
    'NumberNode',
    'AdditionOperatorNode', 'SubtractionOperatorNode',
    'MultiplicationOperatorNode', 'DivisionOperatorNode',
    'ModuloOperatorNode',
    'ExponentiationOperatorNode',
    'RightOperatorNode',
    'ParenthesisNode',
    'processCommand'
]

__author__ = 'RobertD'
__version__ = '1.0'


class InvalidOperatorSequenceError(Exception):
    pass


class MathNode:
    """MathNode is the base class for nodes used in calculator """

    def __init__(self):
        self.left = None
        self.right = None
        self.name = "#"

    def getPrecedence(self):
        """Used to compare operator precedence"""
        return -1

    def append(self, node):
        return self

    def appendDecimalPoint(self):
        return self

    def collapse(self, parendepth):
        """Reduce a tree to the minimum amount of nodes required to
        maintain the information entered so far. In the extreme, collapse
        will reduce a tree to a number"""
        return self

    def evaluate(self):
        """Returns the value of the tree. If the tree cannot fully collapse,
        then this will return a misleading value."""
        return 0

    def squawk(self, depth=0):
        """Print a tree-looking structure that described the tree"""
        print("")

    def squawk2(self):
        """Print a flat infix structure of the tree"""
        pass

    def describe(self):
        return ""

    def openParen(self, parendepth):
        """Mark the open parenthesis, and update the latest operator appropriately"""
        if self.right:
            self.right = self.right.openParen(parendepth)
        return self

    def closeParen(self, parendepth):
        """Mark the close parenthesis, and update the operator at this depth appropriately"""
        if self.right:
            self.right = self.right.closeParen(parendepth)
        return self

    def clone(self):
        return self


class EmptyNode(MathNode):
    def __init__(self):
        super(EmptyNode, self).__init__()

    def append(self, node):
        return node


class NumberNode(MathNode):
    """A NumberNode holds a numeric value."""

    def __init__(self, value):
        super(NumberNode, self).__init__()
        self.value = value
        self.dp = False
        self.numdp = 0
        self.name = str(value)

    def getPrecedence(self):
        # Technically, a number has the highest precedence of all nodes,
        # but we don't ever make use of a NumberNode's precedence.

        return 0

    def evaluate(self):
        return self.value

    def append(self, node):
        # print("append " + node.name + " to " + self.name)
        if isinstance(node, NumberNode):     # Allows character-by-character parsing. Kinda goofy, really.
            if self.dp:
                self.value += node.value / (10 ** self.numdp)
                self.numdp += 1
            else:
                self.value *= 10
                self.value += node.value
            self.name = str(self.value)
            return self
        elif isinstance(node, OperatorNode):  # m, op --> op(m,_)
            # Insert the new node as this node's parent, and make this node the new node's
            # left child. Return the new node so that it becomes the number node's parent's
            # child.
            node.left = self
            return node
        else:
            return self

    def appendDecimalPoint(self):
        if not self.dp:
            self.dp = True
            self.numdp = 1
        self.name = str(self.value)
        return self

    def squawk(self, depth=0):
        print((' ' * depth) + str(self.value))

    def squawk2(self):
        return str(self.value) + ' '

    def describe(self):
        return str(self.value)

    def clone(self):
        return NumberNode(self.value)


class OperatorNode(MathNode):
    def __init__(self, name, precedence, parendepth):
        super(OperatorNode, self).__init__()
        self.name = name
        self.precedence = precedence + (10 * parendepth)
        self.parendepth = parendepth
        # This is a hacky way to handle 2 + -4.
        # Works okay, but would be better to handle in the parser.
        # If we do it in the parser, though, we'd need to handle 3 + -(2 x 5).
        self.signOfSubsequent = 1

    def closeParen(self, parendepth):
        if self.right is not None:
            self.right = self.right.closeParen(parendepth)
        return self

    def getPrecedence(self):
        return self.precedence

    def collapse(self, parendepth)->MathNode:

        if self.left is not None:
            # should be an error; cannot add an operator without a left-node!
            self.left = self.left.collapse(parendepth)
        if self.right is not None:
            self.right = self.right.collapse(parendepth)

        if self.left is not None\
                and isinstance(self.left, NumberNode)\
                and self.right is not None\
                and isinstance(self.right, NumberNode):
            return NumberNode(self.evaluate())
        else:
            return self

    def evaluate(self):
        return 0  # subclass must override

    def append(self, node):
        # print("append " + node.name + "[" + str(node.getPrecedence()) + "] to " + self.name + "[" + str(self.getPrecedence()) + "]")
        if isinstance(node, NumberNode):
            if self.right is None:
                self.right = node  # op(n,_), m -> op(n,m)
                return self
            else:
                self.right = self.right.append(node)  # op(n,e), m -> op(n,(e,m))
                return self
        elif isinstance(node, ParenthesisNode):
            if self.right is None:
                self.right = node
                return self
            else:
                self.right = self.right.append(node)
                return self
        elif isinstance(node, OperatorNode):
            if self.right is None:
                # we got two operators in a row!
                if node.name == '-':
                    self.signOfSubsequent = -1 * self.signOfSubsequent
                    return self
                elif node.name == '+':
                    return self
                    # just a thought: we could support ** = exponentiation here, if we wanted to...
                    # but it would be better to support that in the parser, rather than here.
                else:
                    print("e1")
                    raise InvalidOperatorSequenceError()
            elif node.getPrecedence() > self.getPrecedence():
                # evaluate this node before you evaluate me
                self.right = self.right.append(node)
                return self
            else:
                # evaluate me then this node
                node.left = self
                return node
        else:
            print("e2")
            raise InvalidOperatorSequenceError()

    def appendDecimalPoint(self):
        if self.right is None:
            self.right = NumberNode(0)
        self.right = self.right.appendDecimalPoint()
        return self

    def squawk(self, depth=0):
        print(
            (' ' * depth)
            + self.name
            + '[' + str(self.parendepth) + ']'
            + ('-' if self.signOfSubsequent < 0 else '')
        )
        if self.left is not None:
            self.left.squawk(depth+1)
            if self. right is not None:
                self.right.squawk(depth+1)

    def squawk2(self):
        s = ""
        if self.left is not None:
            s += self.left.squawk2()

        if self.signOfSubsequent < 0:
            s += self.name + '-'
        else:
            s += self.name + ' '

        if self.right is not None:
            s += self.right.squawk2()

        return s

    def describe(self):
        d = ""
        if self.left is not None:
            d = d + self.left.describe()
        d = d + self.name
        if self.signOfSubsequent < 0:
            d = d + '-'
        if self.right is not None:
            d = d + self.right.describe()
        return d

    def _finishCloning(self, k):
        k. signOfSubsequent = self.signOfSubsequent
        if self.left is not None:
            k.left = self.left.clone()
        if self.right is not None:
            k.right = self.right.clone()
        return k


class AdditionOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(AdditionOperatorNode, self).__init__("+", 1, parendepth)

    def evaluate(self):
        v = 0
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            v += self.signOfSubsequent * self.right.evaluate()
        return v

    def clone(self):
        k = AdditionOperatorNode(self.parendepth)
        return self._finishCloning(k)


class SubtractionOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(SubtractionOperatorNode, self).__init__("-", 1, parendepth)

    def evaluate(self):
        v = 0
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            v -= self.signOfSubsequent * self.right.evaluate()
        return v

    def clone(self):
        k = SubtractionOperatorNode(self.parendepth)
        return self._finishCloning(k)


class MultiplicationOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(MultiplicationOperatorNode, self).__init__("x", 2, parendepth)

    def evaluate(self):
        v = 1
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            v *= (self.signOfSubsequent * self.right.evaluate())
        return v

    def clone(self):
        k = MultiplicationOperatorNode(self.parendepth)
        return self._finishCloning(k)


class DivisionOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(DivisionOperatorNode, self).__init__("/", 2, parendepth)

    def evaluate(self):
        v = 1
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            d = self.right.evaluate()
            if d == 0:  # survive this error!
                raise ZeroDivisionError()
            else:
                v /= (self.signOfSubsequent * d)
        return v

    def clone(self):
        k = DivisionOperatorNode(self.parendepth)
        return self._finishCloning(k)


class ModuloOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(ModuloOperatorNode, self).__init__("%", 2, parendepth)

    def evaluate(self):
        v = 0
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            d = self.right.evaluate()
            if d == 0:  # survive this error!
                raise ZeroDivisionError()
            else:
                v %= (self.signOfSubsequent * d)
        return v

    def clone(self):
        k = ModuloOperatorNode(self.parendepth)
        return self._finishCloning(k)


class ExponentiationOperatorNode(OperatorNode):
    def __init__(self, parendepth):
        super(ExponentiationOperatorNode, self).__init__("^", 3, parendepth)

    def evaluate(self):
        v = 0
        if self.left is not None:
            v = self.left.evaluate()
        if self.right is not None:
            d = self.right.evaluate()
            if d == 0:
                v = 1
            else:
                v = v ** (self.signOfSubsequent * d)
        return v

    def clone(self):
        k = ExponentiationOperatorNode(self.parendepth)
        return self._finishCloning(k)


class RightOperatorNode(OperatorNode):
    # A RightOperatorNode is a pseudo-operator that is used when we
    # start an expression with a parenthesis. The parenthesis is held
    # by the preceding operator, so we need _some_ kind of operator
    # here. The RightOperator just ignores its left child.
    def __init__(self, parendepth):
        super(RightOperatorNode, self).__init__("R", -1, 0)

    def evaluate(self):
        if self.right:
            return self.right.evaluate()
        return 0

    def clone(self):
        k = RightOperatorNode(self.parendepth)
        return self._finishCloning(k)

    def squawk2(self):
        if self.right is not None:
            return self.right.squawk2()

    def describe(self):
        d = ""
        if self.right is not None:
            d = d + self.right.describe()
        return d


class ParenthesisNode(OperatorNode):
    def __init__(self, parendepth):
        super(ParenthesisNode, self).__init__("(", 4, parendepth)
        self.endParen = False

    def evaluate(self):
        if self.left is not None:
            return self.left.evaluate()
        return 0

    def closeParen(self, parendepth):
        # print("closeparen at " + str(parendepth) + "apply to "+ str(self.parendepth))
        if self.parendepth == parendepth:
            self.endParen = True
        elif self.left:
            self.left = self.left.closeParen(parendepth)

        return self

    def collapse(self, parendepth)->MathNode:
        if self.left is not None:
            self.left = self.left.collapse(parendepth)

        if self.left is not None and isinstance(self.left, NumberNode) and self.endParen:
            return NumberNode(self.evaluate())
        else:
            return self

    def append(self, node):
        # print("append" + node.name + " to " + self.name)
        if self.endParen:
            node.left = self
            return node
        else:
            if not self.left:
                self.left = node
            else:
                self.left = self.left.append(node)
        return self

    def clone(self):
        k = ParenthesisNode(self.parendepth)
        k.endParen = self.endParen
        return self._finishCloning(k)

    def squawk2(self):
        s = '( '
        if self.left is not None:
            s += self.left.squawk2()
        if self.endParen:
            s += ') '
        return s

    def describe(self):
        d = '('
        if self.left is not None:
            d = d + self.left.describe()
        if self.endParen:
            d = d + ')'
        return d

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
