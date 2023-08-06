# -*- coding: utf-8 -*-
# pebble - Passman client
# Copyright (C) 2018 Damien Goutte-Gattat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . import delete
from . import edit
from . import list
from . import new
from . import show

def get_commands(subparsers):
    command_list = []
    command_list.append(delete.DeleteCommand())
    command_list.append(edit.EditCommand())
    command_list.append(list.ListCommand())
    command_list.append(new.NewCommand())
    command_list.append(show.ShowCommand())

    command_dict = {}
    for command in command_list:
        command.prepare_parser(subparsers)
        command_dict[command.name()] = command
    return command_dict
