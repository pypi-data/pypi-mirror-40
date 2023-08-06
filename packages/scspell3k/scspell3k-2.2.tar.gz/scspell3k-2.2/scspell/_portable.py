#
# scspell
# Copyright (C) 2009 Paul Pelzl
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""Contains functions for hiding differences between platforms."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

# Special key codes returned from getch()
CTRL_C = '\x03'
CTRL_D = '\x04'
CTRL_Z = '\x1a'

getch = None
# Cross-platform version of getch()
try:
    import msvcrt

    def msvcrt_getch():
        return msvcrt.getwch()
    getch = msvcrt_getch

except ImportError:
    import tty
    import termios

    def termios_getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    getch = termios_getch


def allow_non_terminal_input():
    def testing_getch():
        s = sys.stdin.read(1)
        if s == '':
            return CTRL_D
        return s
    global getch
    getch = testing_getch


def get_data_dir(prog_name):
    """Retrieves a platform-appropriate data directory for the specified
    program."""
    if sys.platform == 'win32':
        parent_dir = os.getenv('APPDATA')
        prog_dir = prog_name
    else:
        parent_dir = os.path.expanduser('~')
        prog_dir = '.' + prog_name
    return os.path.normpath(os.path.join(parent_dir, prog_dir))
