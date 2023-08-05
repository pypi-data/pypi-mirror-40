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

import logging
import socket
import struct
import timeit
import select
import threading
try:
    import queue
except ImportError:
    import Queue as queue

from .const import bytes_in_double, ICMP_ECHO_REQUEST, ICMP_ECHO_REPLY, \
    ICMP_SOURCE_QUENCH, ICMP_DEST_UNREACH, ICMP_TIME_EXCEEDED, \
    ICMPV6_ECHO_REQUEST, ICMPV6_ECHO_REPLY, ICMPV6_DEST_UNREACH, \
    ICMPV6_TIME_EXCEED, ICMP_DEST_UNREACH_CODE, AF_INET, AF_INET6
from .util import gen_ints, buf_to_icmp, buf_to_icmp4, checksum


class PingTarget:
    '''This class holds data attributes of a ping target (it's address, the
    current state of whether we consider the target up or down) and methods
    to assist with generating and receiving packets. It doesn't do any I/O
    of it's own though.'''
    def __init__(self, hostname, unique_id, comment=''):
        self.name = hostname
        self.id = unique_id
        self.sockaddr = None
        self.family = None
        self.comment = comment
        self.error = ''
        self.state = 'unknown'
        self.state_start = None
        self.packets_sent = 0
        self.packets_received = 0
        self.next_send_time = None
        self.last_send_time = None
        self.start_time = timeit.default_timer()
        self._counter = gen_ints(0, wrap=2**15)

        self.lookup_echo_request_code = {
            AF_INET: ICMP_ECHO_REQUEST,
            AF_INET6: ICMPV6_ECHO_REQUEST,
        }

    def display_state(self):
        return {
            'state': self.state,
            'error': self.error,
            'duration': timeit.default_timer() - self.start_time,
            'state_start': self.state_start,
            'packets_sent': self.packets_sent,
            'packets_received': self.packets_received,
            'loss': self.packet_loss(),
            'name': self.name,
            'id': self.id,
            'comment': self.comment,
        }

    def generate_ping(self):
        sequence = self.counter()
        my_checksum = 0

        icmp_code = self.lookup_echo_request_code[self.family]
        # Header is type (8), code (8), checksum (16), id (16), sequence
        # (16), this is true for both ICMP and ICMPv6
        header = struct.pack(
            "!BBHHh", icmp_code, 0, my_checksum, self.id, sequence)

        # embed a timestamp
        data = (192 - bytes_in_double) * "Q".encode('utf8')
        data = struct.pack("!d", timeit.default_timer()) + data

        # Calculate checksum, then re-write the header with that checksum.
        my_checksum = checksum(header + data)
        header = struct.pack(
            "!BBHHh", icmp_code, 0, my_checksum, self.id, sequence)
        packet = header + data

        return packet

    def counter(self):
        return next(self._counter)

    def set_state(self, state, message):
        self.error = message
        if self.state != state:
            self.state = state
            logging.info("%s changing to state %s (%s)",
                         self.name, state, message)
            self.state_start = timeit.default_timer()

    def packet_loss(self):
        try:
            return float(self.packets_sent - self.packets_received) \
                / self.packets_sent * 100
        except ZeroDivisionError:
            return 0.0

    def process_packet(self, packet):
            self.packets_received += 1

            # Check if this packet is an echo reply
            if (packet['family'], packet['type']) in (
                    (AF_INET, ICMP_ECHO_REPLY),
                    (AF_INET6, ICMPV6_ECHO_REPLY)):

                # Work out how long since we sent the echo request
                time_sent = struct.unpack(
                    "!d", packet['data'][0:bytes_in_double])[0]
                delay = packet['time_received'] - time_sent
                # TODO: average out the RTT, or do something more
                # sophisticated than updating it on every single packet
                # received. Maybe an average of the last 5 received packets,
                # and their delay?

                self.set_state('alive', "Alive, RTT=%f" % delay)
            elif (packet['family'], packet['type']) in (
                    (AF_INET, ICMP_TIME_EXCEEDED),
                    (AF_INET6, ICMPV6_TIME_EXCEED),
                    (AF_INET, ICMP_DEST_UNREACH),
                    (AF_INET6, ICMPV6_DEST_UNREACH)):

                # Confirm that the inner packet really was an
                # ICMP_ECHO_REQUEST packet. Otherwise we could be
                # receving a response packet for some other process,
                # completely unrelated to our echo requests.
                if (packet['family'], packet['original']['type']) \
                        not in (
                        (AF_INET, ICMP_ECHO_REQUEST),
                        (AF_INET6, ICMPV6_ECHO_REQUEST)):
                    logging.debug("PingServer: ignore packet, doesn't contain what we want, type is %d", packet['original']['type']) # noqa E501
                    return

                if (packet['family'], packet['type']) in (
                        (AF_INET, ICMP_TIME_EXCEEDED),
                        (AF_INET6, ICMPV6_TIME_EXCEED)):
                    self.set_state('ttlexpired', "TTL expired")
                elif (packet['family'], packet['type']) in (
                        (AF_INET, ICMP_DEST_UNREACH),
                        (AF_INET6, ICMPV6_DEST_UNREACH)):
                    self.set_state(
                        'down', "Unreachable: %s"
                        % ICMP_DEST_UNREACH_CODE[packet['code']])

    def __str__(self):
        elapsed = timeit.default_timer() - self.state_start
        message = self.message
        name = self.name()

        return '%20s: %0.1f%% loss %s (for %0.2f seconds)' % (
            name, self.packet_loss(), message, elapsed)


class SocketMaster(threading.Thread):
    '''The SocketMaster is a threading class that looks after reading and
    writing from it's sockets, to affect sending and receiving the necessary
    ICMP packets.'''

    def __init__(self, min_wait, max_wait, targets, select_sleep=0.1):
        self.queued_pings = queue.Queue()
        self.select_sleep = select_sleep
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.lock = threading.Lock()
        self.targets = targets

        # TODO: I should improve this error handling. It's possible some
        # clients might not be able to do v6, but can do v4. I shouldn't
        # crash out in that situation.
        self._all_sockets = []
        try:
            self._v4_socket = socket.socket(
                AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
            self._v4_socket.setblocking(False)
            self._all_sockets.append(self._v4_socket)
        except socket.error as socket_error_args:
            (errno, msg) = socket_error_args.args
            if errno == 1:
                # Operation not permitted
                msg = msg + (
                    " - Note that ICMP messages can only be sent from"
                    " processes running as root."
                )
                raise SystemExit(msg)
            raise  # raise the original error

        try:
            self._v6_socket = socket.socket(
                AF_INET6, socket.SOCK_RAW,
                socket.getprotobyname("ipv6-icmp"))
            self._v6_socket.setblocking(False)
            self._all_sockets.append(self._v6_socket)
        except socket.error as socket_error_args:
            (errno, msg) = socket_error_args.args
            if errno == 1:
                # Operation not permitted
                msg = msg + (
                    " - Note that ICMP messages can only be sent from",
                    " processes running as root."
                )
                print(socket.error(msg))
                raise SystemExit
            raise  # raise the original error
        threading.Thread.__init__(self)

    def run(self):

        try:
            self.lock.acquire()
            # resolve any hostnames to sockaddr
            for target in self.targets.values():
                if target.sockaddr is None:
                    self.lock.release()
                    (family, sockaddr) = self.resolve(target.name)
                    self.lock.acquire()
                    target.family = family
                    target.sockaddr = sockaddr
            self.lock.release()
        except PingBoardError as e:
            target.error = str(e)
            target.set_state(self, 'error', str(e))
            self.lock.release()

        family_mapping = {
            self._v4_socket: AF_INET,
            self._v6_socket: AF_INET6,
            }

        while True:
            # Check all ping targets, and see if they are due to have any
            # pings sent.
            self.lock.acquire()
            now = timeit.default_timer()
            for target in self.targets.values():
                if target.next_send_time is None or \
                        now > target.next_send_time:
                    # queue up a ping for sending
                    # Add to self.queued_pings a ping packet.
                    packet = target.generate_ping()
                    data = {
                        'family': target.family,
                        'sockaddr': target.sockaddr,
                        'packet': packet,
                        'target': target,
                    }
                    self.queued_pings.put(data)
                    # set the next sending time.
                    target.next_send_time = now + self.min_wait
                    target.last_send_time = now
            self.lock.release()

            # Send any queued packets, but don't block waiting for them
            try:
                while True:
                    data = self.queued_pings.get(False)
                    self._send_echo_request(data)
            except queue.Empty:
                pass

            # Check for any replies
            what_ready = select.select(
                self._all_sockets, [], [], self.select_sleep)
            for sock in what_ready[0]:
                family = family_mapping[sock]
                try:
                    (buf, address) = sock.recvfrom(1024)
                    self.process_packet(buf, address, family)
                except socket.error as e:
                    logging.debug("socket error: {}".format(e))

            # Update the state on each ping target. If we haven't received
            # any pings lately, might be down. If we have, might be up.
            for target in self.targets.values():

                # Check last sent time, and if we are now past the max_wait
                # time.
                if target.last_send_time and \
                        now > target.last_send_time + self.max_wait:
                    target.set_state("down", "Not Responding")

    def resolve(self, hostname):
        '''Try and resolve a hostname into a sockaddr. This is done after
        the threading loop starts, so that the ui thread can get started to
        draw the UI'''
        # resolve to an IP address. Only care about the first address
        try:
            gai_result = socket.getaddrinfo(hostname, None,
                                            socket.AF_UNSPEC,
                                            socket.SOCK_RAW)[0]

            (family, socktype, proto, canonname, sockaddr) = gai_result
        except socket.gaierror:
            raise PingBoardError("Problem resolving s to an IP address")

        if family not in (AF_INET, AF_INET6):
            raise PingBoardError("Returned an address family that is not supported.") # noqa E501

        return (family, sockaddr)

    def process_packet(self, buf, address, family):
        if family == AF_INET:
            # AF_INET SOCK_RAW sockets give us the whole IPv4 packet,
            # including the headers.
            packet = buf_to_icmp4(buf)
            packet['family'] = AF_INET
        elif family == AF_INET6:
            # It seems AF_INET6 SOCK_RAW sockets give us the payload, but
            # not the IPv6 headers.
            packet = buf_to_icmp(buf, AF_INET6)
            packet['family'] = AF_INET6

        #  Note when we received the packet
        packet['time_received'] = timeit.default_timer()

        if (family, packet['type']) in (
                (AF_INET, ICMP_ECHO_REPLY),
                (AF_INET6, ICMPV6_ECHO_REPLY)):
            self.lock.acquire()
            try:
                self.targets[packet['ID']].process_packet(packet)
            except KeyError:
                logging.debug("SocketMaster: Received echo reply for server %s, but we don't have one of those. Dropping it.", packet['ID']) # noqa E501
            finally:
                self.lock.release()
        elif (family, packet['type']) in (
                (AF_INET, ICMP_DEST_UNREACH),
                (AF_INET, ICMP_TIME_EXCEEDED),
                (AF_INET6, ICMPV6_DEST_UNREACH),
                (AF_INET6, ICMPV6_TIME_EXCEED)):

            # Find the right target. This shouldn't occur too
            # frequently, so searching through all the
            # targets is ok.
            self.lock.acquire()
            try:
                target = [v for v
                          in list(self.targets.values())
                          if v.sockaddr[0] ==
                          packet['original']['destination']][0]
                logging.debug("SocketMaster: Received error packet for server %s", target.id) # noqa E501
                target.process_packet(packet)
            except IndexError:
                logging.debug("Failed to lookup ping server for IP %s. Must not have been a packet for this process", packet['original']['destination']) # noqa E501
            finally:
                self.lock.release()

        elif (family, packet['type']) == (AF_INET, ICMP_SOURCE_QUENCH):
            # for now we'll deliberately ignore this. Perhaps in future
            # we'll make the PingServer slow down it's transmissions.
            pass

    def _send_echo_request(self, data):
        """Send an echo request packet on the socket"""
        logging.debug("SocketMaster: sending packet to %s", data['sockaddr'][0]) # noqa E501
        try:
            if data['family'] == AF_INET:
                self._v4_socket.sendto(data['packet'], data['sockaddr'])
            elif data['family'] == AF_INET6:
                self._v6_socket.sendto(data['packet'], data['sockaddr'])
        except (OSError, IOError) as e:
            # Find which ping server it was, and let them know there was a
            # problem.
            logging.debug("got an error %s, details %s", e, [e.errno, e.strerror]) # noqa E501
            self.lock.acquire()
            data['target'].set_state('down', str(e))
            self.lock.release()

    def target_details(self):
        '''Provide a copy of the targets state, for the UI thread to use
        while drawing'''
        details = []
        self.lock.acquire()
        for t in self.targets.values():
            details.append(t.display_state())
        self.lock.release()
        return details


class PingBoardError(Exception):
    pass
