# -*- coding: utf-8 -*-
# pebble - Passman client
# Copyright (C) 2018,2019 Damien Goutte-Gattat
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

class Command(object):

    def __init__(self, name, help, description=None):
        self._name = name
        self._help = help
        self._desc = description

    def name(self):
        return self._name

    def prepare_parser(self, subparsers):
        return subparsers.add_parser(self._name, help=self._help,
                                     description=self._desc)

    def execute(self, vault, args):
        pass
