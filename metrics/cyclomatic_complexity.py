#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2021 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""cyclomatic_complexity.py"""

import sys

from javalang import tree, parse


def branches(parser_class):
    """
    Determines the number of branches for a node
    according to the Extended Cyclomatic Complexity metric.
    Binary operations (&&, ||) and each case statement
    are taken into account.
    :param parser_class: class provided by the parser (targeted to Java 8 spec)
    :rtype int
    :returns: number
    """
    count = 0
    if isinstance(parser_class, tree.BinaryOperation):
        if parser_class.operator == '&&' or parser_class.operator == '||':
            count = 1
    elif (isinstance(parser_class, (
            tree.ForStatement,
            tree.IfStatement,
            tree.WhileStatement,
            tree.DoStatement,
            tree.TernaryExpression
    ))):
        count = 1
    elif isinstance(parser_class, tree.SwitchStatementCase):
        count = 1
        # count = len(node.case)
    elif isinstance(parser_class, tree.TryStatement):
        count = 1
        # count = len(node.catches)
    return count


if __name__ == '__main__':
    java = sys.argv[1]
    metrics = sys.argv[2]
    with open(java, encoding='utf-8', errors='ignore') as f:
        try:
            complexity: int = 1
            ast = parse.parse(f.read())
            for path, node in ast:
                complexity += branches(node)
            with open(metrics, 'a') as m:
                m.write(f'cc {complexity}: Cyclomatic Complexity\n')
        except FileNotFoundError as exception:
            message = f"{type(exception).__name__} {str(exception)}: {java}"
            sys.exit(message)
