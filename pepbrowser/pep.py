#!/bin/env python
# -*- coding: utf-8 -*-
# pepbrowser is a command line viewer for Python Enhancement Proposals.
# Copyright (C) 2013 Ryan Brown <ryansb@csh.rit.edu>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys
import urwid
import argparse
import subprocess
PEP_FILE = "/home/ryansb/remotes/hg.python.org/peps/pep-%04d.txt"
PEP_URL = "http://svn.python.org/view/*checkout*/peps/trunk/pep-%04d.txt"
PEP_CACHE_DIR = "~/.cache/python-peps/"


def get_pep(pep):
    with open(PEP_FILE % pep) as f:
        try:
            f.close()
            pager = subprocess.Popen(['less', '-F', '-R', '-S',
                                      '-X', '-K', PEP_FILE % pep],
                                     stdin=subprocess.PIPE,
                                     stdout=sys.stdout)
            pager.wait()
        except KeyboardInterrupt:
            # let less handle this, -K will exit cleanly
            return
        return
    print "Couldn't find that PEP, sorry bro."


#TODO: Handle PEP0 specially (table of PEP contents)


class PEPWidget(urwid.WidgetWrap):
    def __init__(self, num, title):
        self.num = num
        self.item = [
            ('fixed', 16, urwid.Padding(urwid.AttrWrap(
                urwid.Text('PEP %04d' % self.num), 'body', 'focus'), left=2)),
            urwid.AttrWrap(urwid.Text('%s' % title), 'body', 'focus'),
        ]
        w = urwid.Columns(self.item)
        self.__super.__init__(w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


def get_pep_list():
    return [PEPWidget(x, "This is a PEP") for x in range(1, 50)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('pep', nargs='?', default=None)
    args = ap.parse_args()
    if not args.pep:
        print "Ask for at least one PEP."
        exit(1)
    get_pep(int(args.pep))
