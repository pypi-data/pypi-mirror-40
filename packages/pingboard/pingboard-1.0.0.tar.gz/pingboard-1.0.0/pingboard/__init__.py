#!/usr/bin/python
"""
%(prog)s [options] server server server ....

Continuously pings each named server, and outputs a display showing how
long each server has been in it's current state (of responding or not
responding). You can specify servers by name or IP address.
"""


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

from argparse import ArgumentParser
import logging
import collections
import os
import curses
import re

from .io import SocketMaster, PingTarget
from .util import gen_ints
from .ui import draw_windows


def main(argv=None):

    argp = ArgumentParser(usage=__doc__)
    argp.add_argument(
        '--max-wait',
        default=3.0,
        type=float,
        help='how long to wait for an icmp echo reply before considering the server to be down or unreachable', # noqa E501
    )
    argp.add_argument(
        '--min-wait',
        default=1.0,
        type=float,
        help="How long to wait in between pings (so we don't flood ping)",
    )
    argp.add_argument(
        '--refresh-interval',
        '-i',
        default=1.0,
        type=float,
        help='How long before updating the screen each time',
    )
    argp.add_argument(
        '--debug',
        '-d',
        const=True,
        default=False,
        action='store_const',
        help='Show debugging output',
    )
    argp.add_argument(
        '--log-file',
        help='File to send log messages to, instead of stderr',
    )
    argp.add_argument(
        '--sort-reverse',
        '-r',
        const=True,
        default=False,
        action='store_const',
        help='Sort the output in reverse order',
    )
    argp.add_argument(
        '--server-list',
        help='''Instead of passing arguments, you can pass a file that lists
        servers to ping.  Should be a text file with one server per line.
        Anything between a whitespace and the end of line is treated as a
        comment, and also displayed''',
    )
    argp.add_argument(
        'servers', metavar='N', nargs='*',
        default=None,
        help='''Servers to ping'''
    )

    arguments = argp.parse_args(argv)

    server_list = []
    server_comments = collections.defaultdict(str)
    if arguments.server_list:
        fp = open(arguments.server_list)
        for line in fp:
            s, comment = re.split(r'\s+', line, maxsplit=1)
            server_list.append(s)
            server_comments[s] = comment.strip()
    else:
        server_list = arguments.servers

    if len(server_list) < 1:
        raise SystemExit("Must specify at least one server")

    # Protect against flood pings
    if arguments.min_wait <= 0.5:
        raise SystemExit("--min-wait must be greater than 0.5")

    if arguments.log_file:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        se = logging.StreamHandler(open(arguments.log_file, 'a'))
        se.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        logger.addHandler(se)

        if arguments.debug:
            se.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

    header_line = "Ping Dashboard. %s released under GPL-3" % copyright
    print(header_line)
    print(len(header_line)*"-")

    ints = gen_ints(1)
    targets = dict()
    for arg in server_list:

        id_base = os.getpid() & 0xFFFF
        server_id = id_base + next(ints)
        pt = PingTarget(hostname=arg, unique_id=server_id,
                        comment=server_comments[arg])
        targets[server_id] = pt

    socketmaster = SocketMaster(
        min_wait=arguments.min_wait,
        max_wait=arguments.max_wait,
        targets=targets,
    )
    socketmaster.setDaemon(True)
    socketmaster.start()

    curses.wrapper(draw_windows, arguments.refresh_interval,
                   target_details=socketmaster.target_details,
                   sort_reverse=arguments.sort_reverse)


if __name__ == '__main__':
    main()
