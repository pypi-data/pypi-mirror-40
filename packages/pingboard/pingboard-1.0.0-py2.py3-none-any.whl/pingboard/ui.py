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

import timeit
import curses
import time


def draw_windows(stdscr, refresh_interval, target_details, sort_reverse=False):
    max_y, max_x = stdscr.getmaxyx()
    num_header_lines = 6
    header = stdscr.derwin(num_header_lines, max_x, 0, 0)
    body = stdscr.derwin(num_header_lines, 0)
    start_time = timeit.default_timer()

    # A data structure that names the columns, and defines their widths
    # The last column has -1 width, it gets what ever width is remaining
    columns = [
        # code name,  width,  display name
        ("name", 15, "Host Name"),
        ("comment", 15, "Comment"),
        ("loss", 5, "Loss%"),
        ("state", 11, "State"),
        ("duration", 10, "Duration"),
        ("error", -1, "Notes "),
    ]

    display_details = target_details()
    while True:

        # Listen for any keystrokes
        body.nodelay(1)
        key_pressed = body.getch()
        if key_pressed in (curses.KEY_CANCEL, ord('q')):
            # Quit out of the program
            break
        if key_pressed == curses.KEY_RESIZE:
            max_y, max_x = stdscr.getmaxyx()

        # Draw the header
        header.addstr(
            0, 0,
            "Ping Dashboard. Copyright 2012 Geoff Crompton released under GPL-3"[0:max_x-1]) # noqa E501
        header.addstr("\n\n")

        header.addstr("Hosts: %s Total, " % len(display_details))
        header.addstr("\n")

        running = timeit.default_timer() - start_time
        header.addstr("Running: %0.1f seconds\n" % running)
        header.addstr("\n")

        width_written = 0
        for code_name, width, display_name in columns:
            if width < 0:
                # negative number means use the rest of the available space.
                width = max_x - width_written - 1

            padded_display = center_and_pad(display_name, width)
            width_written += width
            header.addstr("%s" % padded_display.upper())

        # Draw the body
        body.move(0, 0)
        body.clrtobot()
        cur_y = num_header_lines

        # Update all the details from the targets
        display_details = target_details()
        # Sort them
        display_details.sort(key=lambda x: x['name'], reverse=sort_reverse)

        # start displaying them
        for display_info in display_details:

            width_written = 0
            for code_name, width, display_name in columns:
                value = display_info[code_name]

                # If negative width, assume we can use the rest of the line
                if width < 0:
                    width = max_x - width_written - 1
                body.addstr(pad_and_right(value, width))
                width_written += width

            # Don't write pass the bottom of the screen
            if cur_y >= max_y-1:
                break
            body.addstr("\n")
            cur_y += 1

        header.refresh()
        body.refresh()
        time.sleep(refresh_interval)


def center_and_pad(s, width):
    """Return a string that is width characters long, with s in the centre
    of it. If s is too long it's truncated, if it's short, spaces are padded
    before and after it."""
    len_s = len(s)
    if len_s >= width:
        return s[0:width]

    space_needed = width - len_s
    return ' '*(space_needed//2) + s + ' '*(space_needed//2)


def pad_and_right(value, width):
    """Return a string that is width characters long, with s on the right,
    and truncated if necessary or padded with whitespace otherwise"""
    try:
        s = '%.1f' % value
    except TypeError:
        s = '%s' % value
    len_s = len(s)
    if len_s >= width:
        return s[0:width]

    space_needed = width - len_s
    return ' '*space_needed + s
