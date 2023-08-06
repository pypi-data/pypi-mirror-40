#! /usr/bin/env python

# Py2Play
# Copyright (C) 2001-2002 Jean-Baptiste LAMY
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os.path, sys, distutils.core

distutils.core.setup(name         = "Py2Play",
                     version      = "0.1.11",
                     license      = "GPL",
                     description  = "DEPRECATED A peer-to-peer network game engine in Python.",
                     long_description = """DEPRECATED A peer-to-peer network game engine in Python.
It does not require any server to run.
A small demo is included in the source.""",
                     author       = "Lamy Jean-Baptiste (Jiba)",
                     author_email = "jiba@tuxfamily.org",
                     url          = "http://home.gna.org/oomadness/fr/slune/index.html",
                     
                     package_dir  = {"py2play" : ""},
                     packages     = ["py2play"],
#                     scripts      = ["asker", "startdemo", "startdemo_local1", "startdemo_local2", "startdemo_local3"],
                     )
