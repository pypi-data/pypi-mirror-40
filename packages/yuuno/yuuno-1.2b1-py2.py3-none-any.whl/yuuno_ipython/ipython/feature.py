# -*- encoding: utf-8 -*-

# Yuuno - IPython + VapourSynth
# Copyright (C) 2017 StuxCrystal (Roland Netzsch <stuxcrystal@encode.moe>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Any

from traitlets import HasTraits, Any


class Feature(HasTraits):
    """
    Defines a feature
    """

    environment: 'YuunoIPythonEnvironment' = Any()

    @classmethod
    def feature_name(cls):
        return cls.__name__.lower()

    def initialize(self):
        """
        Initializes a feature
        """

    def deinitialize(self):
        """
        Deinitializes a feature.
        """
