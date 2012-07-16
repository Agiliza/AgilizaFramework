"""
This file is part of Agiliza.

Agiliza is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Agiliza is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Agiliza. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
import functools
import importlib


def import_object(name):
    """
    This function imports an object from a module.

    Can throw ImportError or AttributeError if object_name it is not valid.
    """
    assert isinstance(name, str), "The module name must be a string"

    parts = name.split('.')
    assert len(parts) > 1, "'%s' is not a valid module name" % name

    attr_name = parts[-1]
    module_name = functools.reduce(lambda x, y: x + '.' + y, parts[0:-1])
    module = importlib.import_module(module_name)

    return getattr(module, attr_name)
