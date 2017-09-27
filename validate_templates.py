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

"""Validate Jinja2 templates"""

import os
import sys
import jinja2

env = None


class FilterStub(dict):
    "Stub out all filters used by our Jinja templates"
    def get(item, default):
        return lambda: None


class Jinja2Error(object):
    def __init__(self, template, exc_obj):
        self.template = template
        self.msg = exc_obj.message

    def __str__(self):
        return "Jinja2 Template Error: %s: %s" % (self.template, self.msg)


def check_jinja2(template):
    try:
        env.get_template(template)
    except Exception as e:
        return Jinja2Error(template, e)


def check_tree(topdir, filterf=None):
    errors = []
    for root, _, filenames in os.walk(topdir):
        for f in filenames:
            path = os.path.join(root, f)
            if filterf and filterf(path):
                continue
            err = check_jinja2(path)
            if err:
                errors.append(err)
    return errors


def setup_jinja2_env():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    env.filters = FilterStub()

    return env


def main():
    global env

    env = setup_jinja2_env()
    errors = check_tree('.', lambda x: not x.endswith('.j2'))

    for tree in ['host_vars', 'group_vars']:
        errors += check_tree(tree, lambda x: '.svn' in x or x.rsplit('/')[-1].startswith('.'))

    for err in errors:
        print >>sys.stderr, "%s" % err

    return False if errors else True


if __name__ == '__main__':
    sys.exit(not main())
