#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
#  Copyright (C) 2016 Guido Günther <agx@sigxcpu.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import os
import yaml
import sys

dirs = ['host_vars', 'group_vars']
errors = []


class YamlError(object):
    def __init__(self, exc_obj):
        self.mark = exc_obj.problem_mark
        self.problem = exc_obj.problem


def check_yaml(name):
    with open(name) as fh:
        try:
            yaml.load(fh)
        except yaml.scanner.ScannerError as e:
            return YamlError(e)


def check_tree(topdir, filterf=None):
    errors = []
    for root, _, filenames in os.walk(topdir):
        for f in filenames:
            path = os.path.join(root, f)
            if filterf and filterf(path):
                continue
            err = check_yaml(path)
            if err:
                errors.append(err)
    return errors


def main():
    errors = check_tree('.', lambda x: not x.endswith('.yml') or x.startswith('./vendor'))
    for tree in dirs:
        errors += check_tree(tree, lambda x: '.svn' in x)

    for err in errors:
        print("Error: %s: %s" % (err.mark, err.problem), file=sys.stderr)

    return False if errors else True


if __name__ == '__main__':
    sys.exit(not main())
