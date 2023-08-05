#! /usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import print_function
import ast
import sys
from itertools import chain, islice
try:
    from _collections_abc import Iterable, Sequence
except:
    from collections import Iterable, Sequence


# ## Handy global vairables defined
# TODO


# ## Examples
# TODO


def p(value, *args, **kwargs):
    if isinstance(value, str):
        print(value, *args, **kwargs)
        return

    try:
        values = iter(value)
    except TypeError:
        # If value is not iterable, just print it
        print(value, *args, **kwargs)
        return

    if args:
        raise Exception("Giving extra arguments with a sequence of strs is not allowed")

    # TODO: Decide default end character for a sequence input
    #       Which one would be better, '' or '\n'?
    # kwargs['end'] = kwargs.get('end', '')
    for v in values:
        print(v, *args, **kwargs)


# [Abstract base classes(ABC's) used]
# Iterable: What you can get an iterator from. A container.
# Iterator: What you can call next() on.
# Sequence: What supports all the operations on a read-only sequence, such
#           as __contains__, __reversed__, index and count methods
# Note that Iterable and Iterator are not mutually exclusive in python,
# which can be confusing from time to time. For example, every iterator
# is an iterable.


class SubscriptableStdin(Iterable):
    def __iter__(self):
        for line in sys.stdin:
            yield line

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            return next(islice(self, key, key+1))
        elif isinstance(key, slice):
            return islice(self, key.start, key.stop, key.step)
        raise KeyError('Error')


class LazySequence(Sequence):
    """A LazySequence lazily constructs a Sequence from an iterable."""

    def __init__(self, iterable):
        self.iterable = iterable
        self.restored = False
    
    def get_container(self):
        if self.restored:
            return
        self.restored = True
        self.restored_iterable = list(self.iterable)
    
    def __len__(self):
        self.get_container()
        return len(self.restored_iterable)
    
    def __getitem__(self, key):
        self.get_container()
        return self.restored_iterable[key]


# TODO: Maybe lines -> ls for brevity
lines = SubscriptableStdin()
_lines = LazySequence(lines)


def exec_and_eval_last(code, globals):
    stmts = list(ast.iter_child_nodes(ast.parse(code)))
    if not len(stmts):
        raise Exception("No statements given")

    if isinstance(stmts[-1], ast.Expr):
        if len(stmts) > 1:
            exec(compile(ast.Module(
                body=stmts[:-1]), filename="<ast>", mode="exec"), globals)
        return eval(compile(ast.Expression(body=stmts[-1].value), filename="<ast>", mode="eval"), globals)

    exec(code, globals)


def exec_one(code, globals):
    pos = sys.stdout.tell()
    result = exec_and_eval_last(code, globals)

    # If nothing was written to stdout print the last expression
    if pos== sys.stdout.tell():
        p(result)  # TODO: Maybe change end argument


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='pythonp')
    parser.add_argument('-e', '--each',
                        action='store_true',
                        help="evalute code on each 'line'")
    parser.add_argument('code', nargs=1)
    args = parser.parse_args()

    g = globals().copy()

    if args.each:
        del g['lines'], g['_lines']
        for line in sys.stdin:
            g['line'] = line
            exec_one(args.code[0], g)
    else:
        exec_one(args.code[0], g)



if __name__ == '__main__':
    main()
