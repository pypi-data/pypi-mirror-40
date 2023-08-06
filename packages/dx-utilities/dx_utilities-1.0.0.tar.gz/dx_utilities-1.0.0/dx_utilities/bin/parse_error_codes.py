"""Parse coded-errors handled in the codebase.

Usage::

    git grep -WE "raise \w{10,}\(" | python -m bin.parse_error_codes

Prints in standard output pairs of the form::

    <error-code> <parent function or class>

"""
import logging
import argparse

import sys
import re


def main():
    logging.info("Parsing error codes...")
    class_reg = re.compile(r'class\s(?P<fname>\w+)\(')
    func_reg = re.compile(r'def\s(?P<fname>\w+)\(')
    raise_reg = re.compile(r'raise [a-z]{10,}\((?P<code>\d{4}\b)?',
                           flags=re.I)
    error_reg = re.compile(r'(?P<code>\d{4}\b)')

    funcs = []
    classes = []
    parsed = []
    while True:
        try:
            line = next(sys.stdin)
        except StopIteration:
            break
        cmatch = class_reg.search(line)
        if cmatch:
            classes.append(cmatch.group('fname'))
            continue
        fmatch = func_reg.search(line)
        if fmatch:
            funcs.append(fmatch.group('fname'))
            continue
        rmatch = raise_reg.search(line)
        if rmatch:
            if rmatch.group('code'):
                try:
                    cname = ''
                    if classes:
                        cname = classes[-1]
                    fname = funcs[-1]
                    name = '.'.join((cname, fname))
                except:
                    print(repr(funcs))
                    raise
                else:
                    parsed.append((rmatch.group('code'), name))
                    continue
            else:
                try:
                    line = next(sys.stdin)
                except StopIteration:
                    break
                code = error_reg.search(line).group('code')
                try:
                    cname = ''
                    if classes:
                        cname = classes[-1]
                    fname = funcs[-1]
                    name = '.'.join((cname, fname))
                except:
                    print(repr(funcs))
                    raise
                else:
                    parsed.append((code, name))
                continue
    print('\n'.join(['\t'.join(t) for t in parsed]))


if __name__ == "__main__":
    main()
