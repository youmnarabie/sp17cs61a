def countdown(n):
    """
    A generator that counts down from N to 0.
    >>> for number in countdown(5):
    ...     print(number)
    ...
    5
    4
    3
    2
    1
    0
    >>> for number in countdown(2):
    ...     print(number)
    ...
    2
    1
    0
    """
    while n >= 0:
        yield n
        n -= 1

class Countdown:
    """
    An iterator that counts down from N to 0.
    >>> for number in Countdown(5):
    ...     print(number)
    ...
    5
    4
    3
    2
    1
    0
    >>> for number in Countdown(2):
    ...     print(number)
    ...
    2
    1
    0
    """
    def __init__(self, cur):
        self.cur = cur

    def __next__(self):
        if self.cur >= 0:
            result = self.cur
            self.cur -= 1
            return result 
        else:
            raise StopIteration()

    def __iter__(self):
        """So that we can use this iterator as an iterable."""
        return self

class Tree:
    def __init__(self, label, branches=[]):
        for c in branches:
            assert isinstance(c, Tree)
        self.label = label
        self.branches = branches

    def __repr__(self):
        if self.branches:
            branches_str = ', ' + repr(self.branches)
        else:
            branches_str = ''
        return 'Tree({0}{1})'.format(self.label, branches_str)

    def is_leaf(self):
        return not self.branches

    def __eq__(self, other):
        return type(other) is type(self) and self.label == other.label \
               and self.branches == other.branches

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the label.

    >>> print_tree(Tree(1))
    1
    >>> print_tree(Tree(1, [Tree(2)]))
    1
      2
    >>> numbers = Tree(1, [Tree(2), Tree(3, [Tree(4), Tree(5)]), Tree(6, [Tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(t.label))
    for b in t.branches:
        print_tree(b, indent + 1)


import re

OPERATORS = ('*', '+', '-')

# Alternative names of parts of an expression tree.

class Expr(Tree):

    num_exprs = 0

    def __init__(self, op, *branches):
        """For convenience, an Expr may be constructed as Expr(op, [c1, ...])
        or Expr(op, c1, ...)."""
        Expr.num_exprs += 1
        if len(branches) == 1 and type(branches[0]) is list:
            super().__init__(op, branches[0])
        else:
            super().__init__(op, list(branches))

    # The following methods allow you to write E.oper, E[k] for the label
    # and kth child of E, in keeping with the usual language for dealing with
    # expressions.  The class inherits from Tree, to == is also defined.

    @property
    def oper(self):
        return self.label

    def __getitem__(self, k):
        return self.branches[k]

    def __setitem__(self, k, v):
        self.branches[k] = v

    def arity(self):
        """The number of operands in this expression."""
        return len(self.branches)

# Useful constants:

ZERO = Expr(0)
ONE = Expr(1)

def postfix_to_expr(postfix_expr):
    """Return an expression tree equivalent to POSTFIX_EXPR, a string
    in postfix ("reverse Polish") notation.  In postfix, one writes
    E1 OP E2 (where E1 and E2 are expressions and OP is an operator) as
    E1' E2' OP, where E1' and E2' are the postfix versions of E1 and E2. For
    example, '2*(3+x)' is written '2 3 x + *' and '2*3+x' is `2 3 * x +'.
    >>> print_tree(postfix_to_expr("2 3 x + *"))
    *
      2
      +
        3
        x
    """

    E = re.split(r'\s+', postfix_expr.strip())
    def expr():
        """Removes and returns an expression from the end of E.  Modifies
        the list E, which is a list of operands and operators taken from a
        postfix expression string."""
        op = E.pop()
        if op in OPERATORS:
            right = expr()
            left = expr()
            return Expr(op, left, right)
        else:
            try:
                op = int(op)
            except:
                pass
            return Expr(op)
    return expr()

def expr_to_infix(expr):
    """A string containing a standard infix denotation of the expression
    tree EXPR"""
    if expr.is_leaf():
        return str(expr.label)
    else:
        return "({} {} {})".format(expr_to_infix(expr[0]), 
                                   expr.label,
                                   expr_to_infix(expr[1]))
    
def expr_to_postfix(expr):
    """The inverse of postfix_to_expr."""
    if expr.is_leaf():
        return str(expr.oper)
    else:
        return "{} {} {}".format(expr_to_postfix(expr[0]),
                                 expr_to_postfix(expr[1]),
                                 expr.oper)


def simplify(expr):
    """EXPR must be an expression tree involving the operators
    '+', '*', and '-' in inner nodes; numbers and strings (standing for
    variable names) in leaves.  Returns an equivalent, simplified version
    of EXPR.
    >>> def simp(postfix_expr):
    ...     v0 = postfix_to_expr(postfix_expr)
    ...     v1 = postfix_to_expr(postfix_expr)
    ...     r = expr_to_infix(simplify(v0))
    ...     assert v0 == v1, "Input was modified by simplify"
    ...     return r
    >>> simp("x y + 0 *")
    '0'
    >>> simp("0 x y + *")
    '0'
    >>> simp("x y + 0 +")
    '(x + y)'
    >>> simp("0 x y + +")
    '(x + y)'
    >>> simp("x y + 1 *")
    '(x + y)'
    >>> simp("1 x y + *")
    '(x + y)'
    >>> simp("x y + x y + -")
    '0'
    >>> simp("x y y - + x - a b * *")
    '0'
    >>> simp("x y 3 * -")
    '(x - (y * 3))'
    >>> simp("x y 0 + 3 * -")
    '(x - (y * 3))'
    """
    if expr.is_leaf():
        return Expr(expr.oper)
    else:
        left_side = expr[0]
        right_side = expr[1]
        simplified_right = simplify(right_side)
        simplified_left = simplify(left_side)
        if expr.oper == '*' and (simplified_left == ZERO or simplified_right == ZERO):
            return ZERO
        elif expr.oper == '*' and simplified_left == ONE:
            return simplified_right
        elif expr.oper == '*' and simplified_right == ONE:
            return simplified_left
        elif expr.oper == '+' and simplified_left == ZERO:
            return simplified_right
        elif expr.oper == '+' and simplified_right == ZERO:
            return simplified_left
        elif expr.oper == '-' and simplified_left == simplified_right:
            return ZERO
        elif expr.oper == '-' and simplified_left == ZERO:
            return simplified_right
        elif expr.oper == '-' and simplified_right == ZERO:
            return simplified_left
        return Expr(expr.oper, [simplified_left, simplified_right])

def dsimplify(expr):
    """EXPR must be an expression tree involving the operators
    '+', '*', and '-' in inner nodes; numbers and strings (standing for
    variable names) in leaves.  Returns an equivalent, simplified version
    of EXPR.
    >>> def simp(postfix_expr):
    ...     expr = postfix_to_expr(postfix_expr)
    ...     cnt0 = Expr.num_exprs
    ...     v = expr_to_infix(dsimplify(expr))
    ...     assert cnt0 == Expr.num_exprs, "New expression trees created."
    ...     return v
    >>> simp("x y + 0 *")
    '0'
    >>> simp("0 x y + *")
    '0'
    >>> simp("x y + 0 +")
    '(x + y)'
    >>> simp("0 x y + +")
    '(x + y)'
    >>> simp("x y + 1 *")
    '(x + y)'
    >>> simp("1 x y + *")
    '(x + y)'
    >>> simp("x y + x y + -")
    '0'
    >>> simp("x y y - + x - a b * *")
    '0'
    >>> simp("x y 3 * -")
    '(x - (y * 3))'
    >>> simp("x y 0 + 3 * -")
    '(x - (y * 3))'
    """
    if expr.is_leaf():
        return expr
    else:
        expr[0] = dsimplify(expr[0])
        expr[1] = dsimplify(expr[1])
        if expr.oper == '*' and (expr[0] == ZERO or expr[1] == ZERO):
            expr = ZERO
        elif expr.oper == '*' and expr[0] == ONE:
            expr = expr[1]
        elif expr.oper == '*' and expr[1] == ONE:
            expr = expr[0]
        elif expr.oper == '+' and expr[0] == ZERO:
            expr = expr[1]
        elif expr.oper == '+' and expr[1] == ZERO:
            expr = expr[0]
        elif expr.oper == '-' and expr[0] == expr[1]:
            expr = ZERO
        elif expr.oper == '-' and expr[0] == ZERO:
            expr = expr[1]
        elif expr.oper == '-' and expr[1] == ZERO:
            expr = expr[0]
        return expr

class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.deposit(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, kind, cost, quantity=0, cash=0):
        self.kind = kind
        self.quantity = quantity
        self.cost = cost
        self.cash = cash
        self.vend = self.__vend__
        self.restock = self.__restock__
        self.deposit = self.__deposit__
    def __restock__(self, amount):
        self.quantity += amount
        return 'Current ' + str(self.kind) + ' stock:' + " " + str(self.quantity)
    def __vend__(self):
        if self.quantity == 0:
            return 'Machine is out of stock.' 
        elif self.cash < self.cost:
            self.needed = self.cost - self.cash
            return 'You must deposit $' + str(self.needed) + " more."
        elif self.cash > self.cost:
            self.extra = self.cash - self.cost
            self.cash = 0
            self.quantity -= 1
            return 'Here is your ' + str(self.kind) + ' and $' + str(self.extra) + " change."
        else:
            self.quantity -= 1
            return 'Here is your '  + str(self.kind) + '.'
        self.quantity -= 1
    def __deposit__(self, number):
        self.cash += number
        if self.quantity == 0:
            return 'Machine is out of stock. Here is your $' + str(number) + "."
        else:
            return 'Current balance: $' + str(self.cash)




def merge(s0, s1):
    """Yield the elements of strictly increasing iterables s0 and s1, removing
    repeats. Assume that s0 and s1 have no repeats. You can also assume that s0
    and s1 represent infinite sequences.

    >>> m = merge([0, 2, 4, 6, 8, 10, 12, 14], [0, 3, 6, 9, 12, 15])
    >>> type(m)
    <class 'generator'>
    >>> list(m)
    [0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    >>> def big(n):
    ...    k = 0
    ...    while True: yield k; k += n
    >>> m = merge(big(2), big(3))
    >>> [next(m) for _ in range(11)]
    [0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    i0, i1 = iter(s0), iter(s1)
    e0, e1 = next(i0, None), next(i1, None)
    while True:
        if e0 == None and e1 == None:
            raise StopIteration()
        elif e1 == None:
            tobepassed = e0
            e0 = next(i0, None)
            yield tobepassed
        elif e0 == None:
            tobepassed = e1
            e1 = next(i1, None)
            yield tobepassed
        elif e1 == e0:
            tobepassed = e0
            e0 = next(i0, None)
            e1 = next(i1, None)
            yield tobepassed
        elif e1 > e0:
            tobepassed = e0
            e0 = next(i0, None)
            yield tobepassed
        elif e0 > e1:
            tobepassed = e1
            e1 = next(i1, None)
            yield tobepassed


def zip(*iterables):
    """
    Takes in any number of iterables and zips them together. 
    Returns a generator that outputs a series of lists, each 
    containing the nth items of each iterable. 
    >>> z = zip([1, 2, 3], [4, 5, 6], [7, 8])
    >>> for i in z:
    ...     print(i)
    ...
    [1, 4, 7]
    [2, 5, 8]
    """
    "*** YOUR CODE HERE ***"
