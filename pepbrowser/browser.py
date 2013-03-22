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

import urwid
from pepbrowser.pep import get_pep_list


def browser_main():
    """Run the program."""
    palette = [
        ('body', 'black', 'light gray'),
        ('flagged', 'black', 'dark green', ('bold', 'underline')),
        ('focus', 'light gray', 'dark blue', 'standout'),
        ('flagged focus', 'yellow', 'dark cyan', ('bold', 'standout',
                                                  'underline')),
        ('head', 'yellow', 'black', 'standout'),
        ('foot', 'light gray', 'black'),
        ('key', 'light cyan', 'black', 'underline'),
        ('title', 'white', 'black', 'bold'),
        ('dirmark', 'black', 'dark cyan', 'bold'),
        ('flag', 'dark gray', 'light gray'),
        ('error', 'dark red', 'light gray'),
    ]

    footer_text = [
        ('title', "PEP Browser"), "    ",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  ",
        ('key', "Q"),
    ]

    header = urwid.Text("Welcome to the PEP Reader")

    pep_widget_list = urwid.SimpleFocusListWalker(get_pep_list())
    listbox = urwid.ListBox(pep_widget_list)

    footer = urwid.AttrWrap(urwid.Text(footer_text), 'foot')

    view = urwid.Frame(
        urwid.AttrWrap(listbox, 'body'),
        header=urwid.AttrWrap(header, 'head'),
        footer=footer)

    def keystroke(key):
        # update display of focus directory
        if key.lower() == 'q':
            raise urwid.ExitMainLoop()
        try:
            if key.lower() == 'j':
                pep_widget_list.focus = pep_widget_list.get_next(
                    pep_widget_list.focus)[1]
                pep_widget_list._modified()
            if key.lower() == 'k':
                pep_widget_list.focus = pep_widget_list.get_prev(
                    pep_widget_list.focus)[1]
                pep_widget_list._modified()
        except IndexError:
            pass
        if key in ['enter', ' ']:
            focus = listbox.get_focus()[0].content
            view.set_header(urwid.AttrWrap(urwid.Text(
                'selected; %s' % str(focus)), 'head'))

    loop = urwid.MainLoop(view, palette, unhandled_input=keystroke)
    loop.run()
    print "Exiting, so long and thanks for all the fish!"
