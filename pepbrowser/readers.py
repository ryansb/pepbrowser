#!/usr/bin/python
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

import os
import sys
import requests
import subprocess
from StringIO import StringIO

PEP_CACHE_DIR = os.path.expanduser("~/.cache/python-peps/")
PEP_URL = "http://svn.python.org/view/*checkout*/peps/trunk/pep-%04d.txt"


class PEPNotFound(Exception):
    pass


def validate_pep_number(pep_number):
    #TODO: Check that a PEP actually exists
    try:
        pep_number = int(pep_number)
    except ValueError:
        return None

    return pep_number


def read_cached_pep(pep_number):
    #TODO: Read peps from a cache dir
    try:
        with open(PEP_CACHE_DIR + pep_number + '.txt') as f:
            return f.read()
    except IOError:
        return None


def cache_pep(pep_number, body):
    with open(PEP_CACHE_DIR + pep_number + '.txt', 'w') as f:
        f.write(body)


def read_network_pep(pep_number):
    r = requests.get(PEP_URL % pep_number)
    if r.status_code == 200:
        cache_pep(pep_number, r.data)
        return r.content
    elif r.status_code == 404:
        raise PEPNotFound("Request for PEP %s failed with a 404" % pep_number)
    else:
        raise Exception("Unexpected %s HTTP code, with data %s" %
                        (r.status_code, r.content))


def page_pep(input_pep):
    pep_number = validate_pep_number(input_pep)
    if not pep_number:
        raise PEPNotFound("PEP %s could not be found.")
    pep_contents = read_cached_pep(pep_number) or read_network_pep(pep_number)
    try:
        pager = subprocess.Popen(['less', '-F', '-R', '-S', '-X', '-K'],
                                 stdin=StringIO(pep_contents),
                                 stdout=sys.stdout)
        pager.wait()
    except KeyboardInterrupt:
        # let less handle this, -K will exit cleanly
        return


def init_cache():
    if os.path.isdir(PEP_CACHE_DIR):
        os.mkdir(PEP_CACHE_DIR)

