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

VERSION = "0.1.8"

# try:
#   from socket import MSG_WAITALL
  
# except ImportError: # Fucking non-BSD compliant system !
#   def recvall(s, n): return s.makefile("rb").read(n)
  
# else: # Linux,..., good system
#   def recvall(s, n): return s.recv(n, MSG_WAITALL)
  
