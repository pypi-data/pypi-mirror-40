# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import socket
import struct

__version__ = '1.0.0'
copyright = "Copyright 2012 Geoff Crompton"

# Global variable, to save re-calculating it in threads
bytes_in_double = struct.calcsize("d")

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.
ICMP_ECHO_REPLY = 0  # Seems to be the same on Solaris.
ICMP_SOURCE_QUENCH = 4
ICMP_DEST_UNREACH = 3
ICMP_TIME_EXCEEDED = 11

# From /usr/include/linux/icmpv6.h; your milage may vary.
ICMPV6_ECHO_REQUEST = 128  # Seems to be the same on Solaris.
ICMPV6_ECHO_REPLY = 129  # Seems to be the same on Solaris.
ICMPV6_DEST_UNREACH = 1
ICMPV6_TIME_EXCEED = 3

ICMP_DEST_UNREACH_CODE = {
    0: 'network unreachable',
    1: 'host unreachable',
    2: 'protocol unreachable',
    3: 'port unreachable',
    4: 'fragmendation needed and DF set',
    5: 'source route failed',
}

AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6
