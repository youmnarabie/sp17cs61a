def make_to_string(front, mid, back, empty_repr):
    """ Returns a function that turns linked lists to strings.

    >>> stans_to_string = make_to_string("[", "|-]-->", "", "[]")
    >>> michelles_to_string = make_to_string("(", " . ", ")", "()")
    >>> lst = Link(1, Link(2, Link(3, Link(4))))
    >>> stans_to_string(lst)
    '[1|-]-->[2|-]-->[3|-]-->[4|-]-->[]'
    >>> stans_to_string(Link.empty)
    '[]'
    >>> michelles_to_string(lst)
    '(1 . (2 . (3 . (4 . ()))))'
    >>> michelles_to_string(Link.empty)
    '()'
    """
    #Link.empty = empty_repr
    def stringing_along(variable):
        if variable is Link.empty:
            return empty_repr
        else:
            return front + str(variable.first) + mid + stringing_along(variable.rest) + back
    return stringing_along

def mutate_reverse(link):
    """Mutates the Link so that its elements are reversed.

    >>> link = Link(1)
    >>> mutate_reverse(link)
    >>> link
    Link(1)

    >>> link = Link(1, Link(2, Link(3)))
    >>> mutate_reverse(link)
    >>> link
    Link(3, Link(2, Link(1)))
    """
    if link is Link.empty or link.rest is Link.empty:
        return 
    mutate_reverse(link.rest)
    while link.rest is not Link.empty:
        link.first, link.rest.first = link.rest.first, link.first
        link = link.rest

def tree_map(fn, t):
    """Maps the function fn over the entries of tree and returns the
    result in a new tree.

    >>> numbers = Tree(1,
    ...                [Tree(2,
    ...                      [Tree(3),
    ...                       Tree(4)]),
    ...                 Tree(5,
    ...                      [Tree(6,
    ...                            [Tree(7)]),
    ...                       Tree(8)])])
    >>> print_tree(tree_map(lambda x: 2**x, numbers))
    2
      4
        8
        16
      32
        64
          128
        256
    """
    return Tree(fn(t.label), [tree_map(fn, b) for b in t.branches])


def add_trees(t1, t2):
    """
    >>> numbers = Tree(1,
    ...                [Tree(2,
    ...                      [Tree(3),
    ...                       Tree(4)]),
    ...                 Tree(5,
    ...                      [Tree(6,
    ...                            [Tree(7)]),
    ...                       Tree(8)])])
    >>> print_tree(add_trees(numbers, numbers))
    2
      4
        6
        8
      10
        12
          14
        16
    >>> print_tree(add_trees(Tree(2), Tree(3, [Tree(4), Tree(5)])))
    5
      4
      5
    >>> print_tree(add_trees(Tree(2, [Tree(3)]), Tree(2, [Tree(3), Tree(4)])))
    4
      6
      4
    >>> print_tree(add_trees(Tree(2, [Tree(3, [Tree(4), Tree(5)])]), Tree(2, [Tree(3, [Tree(4)]), Tree(5)])))
    4
      6
        8
        5
      5
    """
    if not t1:
            return t2 
    if not t2:
        return t1 
    new_label = t1.label + t2.label
    t1_branches, t2_branches = list(t1.branches), list(t2.branches)
    length_t1, length_t2 = len(t1_branches), len(t2_branches)
    if length_t1 < length_t2:
        t1_branches += [None for _ in range(length_t1, length_t2)]
    elif length_t1 > length_t2:
        t2_branches += [None for _ in range(length_t2, length_t1)]
    return Tree(new_label, [add_trees(branch1, branch2) for branch1, branch2 in zip(t1_branches, t2_branches)])

# Link
class Link:
    """A linked list.

    >>> s = Link(1, Link(2, Link(3)))
    >>> s.first
    1
    >>> s.rest
    Link(2, Link(3))
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is Link.empty:
            return 'Link({})'.format(self.first)
        else:
            return 'Link({}, {})'.format(self.first, repr(self.rest))
def print_link(link):
    """Print elements of a linked list link.

    >>> link = Link(1, Link(2, Link(3)))
    >>> print_link(link)
    <1 2 3>
    >>> link1 = Link(1, Link(Link(2), Link(3)))
    >>> print_link(link1)
    <1 <2> 3>
    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print_link(link1)
    <3 <4> 5 6>
    """
    print('<' + helper(link).rstrip() + '>')

def helper(link):
    if link == Link.empty:
        return ''
    elif isinstance(link.first, Link):
        return '<' + helper(link.first).rstrip() + '> ' + helper(link.rest)
    else:
        return str(link.first) +' '+  helper(link.rest)

# Tree
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