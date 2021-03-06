import unittest
from Node import *


class TestNode(unittest.TestCase):
    def testManual(self):
        root = NumberNode(0)

        root = root.append(NumberNode(3))
        self.assertTrue(root.evaluate() == 3)
        root = root.append(NumberNode(6))
        self.assertTrue(root.evaluate() == 36)

        root = root.append(AdditionOperatorNode(0))
        # 36+
        self.assertTrue(root.describe() == '36+')

        root = root.append(NumberNode(4))
        # 36+4
        self.assertTrue(root.evaluate() == 40)
        self.assertTrue(root.describe() == '36+4')

        root = root.append(MultiplicationOperatorNode(0))
        # 36+4x
        self.assertTrue(root.describe() == '36+4x')
        root = root.append(NumberNode(6))
        # 36+4x6
        self.assertTrue(root.evaluate() == 60)

    def testString1(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, 0, "4+6")
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.evaluate() == 10)

    def testStringWithPrecedence(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, 0, "4+6x4")
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.evaluate() == 28)

    def testStringWithParens(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, "4 x (6 + 4)")
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.evaluate() == 40)
        self.assertTrue(root.describe() == '4x(6+4)')

    def testStringWithParens2(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, "4 x (6")
        self.assertTrue(paren_depth == 1)
        self.assertTrue(root.describe() == '4x(6')

        root, paren_depth = MathNode.process_command(root, paren_depth, '+4')
        self.assertTrue(paren_depth == 1)
        self.assertTrue(root.describe() == '4x(6+4')

        root, paren_depth = MathNode.process_command(root, paren_depth, ')')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '4x(6+4)')
        self.assertTrue(root.evaluate() == 40)

    def testStartWithParen(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '(4+5)')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '(4+5)')
        self.assertTrue(root.evaluate() == 9)

    def testAddNegative(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '4+-3')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '4+-3')
        self.assertTrue(root.evaluate() == 1)

    def testParen1(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '(4+3)x5')

        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '(4+3)x5')
        self.assertTrue(root.evaluate() == 35)

    def testParen2(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '2x(4+3)')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '2x(4+3)')
        self.assertTrue(root.evaluate() == 14)

    def testParen3(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '1+(4+3)x5')

        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '1+(4+3)x5')
        self.assertTrue(root.evaluate() == 36)

    def testAppendToParen(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '(4+3)')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '(4+3)')
        self.assertTrue(root.evaluate() == 7)

        root, paren_depth = MathNode.process_command(root, paren_depth, 'x5')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '(4+3)x5')
        self.assertTrue(root.evaluate() == 35)

    def testStartWithNegativeParen(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, '-(4+3)')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '0-(4+3)')
        self.assertTrue(root.evaluate() == -7)

        root, paren_depth = MathNode.process_command(root, paren_depth, 'x5')
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == '0-(4+3)x5')
        self.assertTrue(root.evaluate() == -35)

    def testTwoParens(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, "(4+3)x(3+5)")
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == "(4+3)x(3+5)")
        self.assertTrue(root.evaluate() == 56)

    def testNestedParens(self):
        root = NumberNode(0)
        paren_depth = 0
        root, paren_depth = MathNode.process_command(root, paren_depth, "4x(4+(3x5))")
        self.assertTrue(paren_depth == 0)
        self.assertTrue(root.describe() == "4x(4+(3x5))")
        self.assertTrue(root.evaluate() == 76)


if __name__ == '__main__':
    unittest.main()
