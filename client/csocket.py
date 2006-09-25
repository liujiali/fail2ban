# This file is part of Fail2Ban.
#
# Fail2Ban is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Fail2Ban is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fail2Ban; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Author: Cyril Jaquier
# 
# $Revision$

__author__ = "Cyril Jaquier"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2004 Cyril Jaquier"
__license__ = "GPL"

from cPickle import dumps, loads
import socket

class CSocket:
	
	END_STRING = "<F2B_END_COMMAND>"
	SOCKET_FILE = "/tmp/fail2ban.sock"
	
	def __init__(self):
		# Create an INET, STREAMing socket
		#self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__csock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		#self.csock.connect(("localhost", 2222))
		self.__csock.connect(CSocket.SOCKET_FILE)
	
	def send(self, msg):
		# Convert every list member to string
		obj = dumps(map(str, msg))
		self.__csock.send(obj + CSocket.END_STRING)
		ret = self.receive(self.__csock)
		self.__csock.close()
		return ret
	
	def receive(self, socket):
		msg = ''
		while msg.rfind(CSocket.END_STRING) == -1:
			chunk = socket.recv(6)
			if chunk == '':
				raise RuntimeError, "socket connection broken"
			msg = msg + chunk
		return loads(msg)
