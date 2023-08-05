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

import struct
import socket

from .const import ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, \
    ICMP_DEST_UNREACH, ICMP_TIME_EXCEEDED, \
    ICMPV6_ECHO_REQUEST, ICMPV6_ECHO_REPLY, ICMPV6_DEST_UNREACH, \
    ICMPV6_TIME_EXCEED, AF_INET, AF_INET6


def buf_to_icmp(buf, family):
    """Interpret 'buf' as an ICMP packet. Assumes buf starts with the ICMP
    header, and any preceeding headers have been removed. Family indicates
    if this is an ICMPv6 or and ICMP packet"""

    if len(buf) < 8:
        raise RuntimeError("buffer to short")

    # Turns out both ICMP and ICMPv6 have the same structure.
    type_, code, checksum = struct.unpack("!BBH", buf[:4])
    packet = {
        'type': type_,
        'code': code,
        'checksum': checksum,
        'data': buf[8:]
    }

    if (family, type_) in (
            (AF_INET, ICMP_ECHO_REQUEST),
            (AF_INET, ICMP_ECHO_REPLY),
            (AF_INET6, ICMPV6_ECHO_REQUEST),
            (AF_INET6, ICMPV6_ECHO_REPLY)):
        packetID, sequence = struct.unpack("!HH", buf[4:8])
        packet['ID'] = packetID
        packet['sequence'] = sequence

    # For destination unreachable and time exceeded we expect to see an
    # inner packet as well. Interpret that.
    elif family == AF_INET and type_ in \
            (ICMP_DEST_UNREACH, ICMP_TIME_EXCEEDED):

        # Before we try and use this data, check we've got enough of the
        # packet.
        if len(packet['data']) < 20:
            raise RuntimeError("Expected more data, to cover inner IPv4 packet header") # noqa 501

        (ver_ihl,) = struct.unpack("!B", packet['data'][0:1])
        version = (ver_ihl & 0xf0) >> 4
        if version != 4:
            raise RuntimeError("Didn't decoded to expected version 4, got {}s".format(version)) # noqa E501
        ihl = ver_ihl & 0x0f
        if ihl < 5:
            raise RuntimeError("IHL field smaller than legal, rfc791")
        ioff = ihl*4
        original = dict()
        orig_dest = packet['data'][16:20]
        original['destination'] = socket.inet_ntop(AF_INET, orig_dest)
        original['type'], original['code'] = struct.unpack(
                "!BB", packet['data'][ioff:ioff+2])
        original['data'] = packet['data'][ioff+8:]
        packet['original'] = original
    elif family == AF_INET6 and type_ in \
            (ICMPV6_DEST_UNREACH, ICMPV6_TIME_EXCEED):
        original = buf_to_ip6(packet['data'])
        packet['original'] = original

    return packet


def buf_to_icmp4(buf):
    (ver_ihl,) = struct.unpack("!B", buf[0:1])
    version = (ver_ihl & 0xf0) >> 4
    ihl = ver_ihl & 0x0f

    if version != 4:
        raise RuntimeError("not a version 4 IP packet")
    if ihl < 5:
        raise RuntimeError("IHL field smaller than legal, rfc791")

    # Calculate the offset to the ICMP header. ihl is the number of 32
    # bit words in the header. 32/8 gives me 4 as the multiple to get
    # the number of octets into the buffer.
    ioff = ihl*4
    return buf_to_icmp(buf[ioff:], AF_INET)


def buf_to_ip6(buf):
    packet = dict()

    if len(buf) < 40:
        raise RuntimeError("buffer to short")

    (ver_class_flow,) = struct.unpack("!i", buf[0:4])
    version = (ver_class_flow & 0xf0000000) >> 28
    if version != 6:
        raise RuntimeError("Expected IPv6 packet, but didn't decode version to 6") # noqa E501

    dest = buf[24:40]
    packet['destination'] = socket.inet_ntop(AF_INET6, dest)

    (next_header,) = struct.unpack("!B", buf[6:7])

    upto_offset = 40
    ipv6_icmp_proto = socket.getprotobyname("ipv6-icmp")
    while next_header != ipv6_icmp_proto:

        if next_header == 59:
            raise RuntimeError("Got the 'No Next Header', expecting something else") # noqa E501

        try:
            next_header, hdr_len = struct.unpack(
                "!BB", buf[upto_offset:upto_offset+2])
        except struct.error:
            raise RuntimeError("Ran out of buffer while unpacking next header") # noqa E501

        # The hdr_len is the length of this header in 8-octet units, not
        # including the first 8 octets
        upto_offset += hdr_len/8 + 8
    orig_icmp_header = buf[upto_offset:]
    packet['type'], packet['code'] = struct.unpack(
        "!BB", orig_icmp_header[0:2])
    packet['data'] = orig_icmp_header[8:]
    return packet


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    """
    sum_ = 0
    countTo = (len(source_string)/2)*2
    count = 0
    while count < countTo:
        thisVal = ord(source_string[count + 1:count+2])*256 + \
            ord(source_string[count:count+1])
        sum_ = sum_ + thisVal
        sum_ = sum_ & 0xffffffff  # Necessary?
        count = count + 2

    if countTo < len(source_string):
        sum_ = sum_ + ord(source_string[
            len(source_string) - 1:len(source_string)])
        sum_ = sum_ & 0xffffffff  # Necessary?

    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ = sum_ + (sum_ >> 16)
    answer = ~sum_
    answer = answer & 0xffff

    # Swap bytes, presumably to get answer into bigendian (i.e. network
    # order).
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def gen_ints(start, wrap=None):
    '''Return an incrementing number. If wrap is specified, then we modulo
    that number, in order to keep it within a range.'''
    while True:
        yield start
        start += 1
        if wrap:
            start = start % wrap
