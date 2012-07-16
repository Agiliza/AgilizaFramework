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
import types
import sys
import unittest

from agiliza.core.utils.imports import import_object


class ImportObjectTest(unittest.TestCase):

    def test_must_not_load_too_short_name(self):
        with self.assertRaises(AssertionError,
            msg="Must be raise a AssertionError"):
            import_object('too_short')

    def test_must_not_load_no_string_arg(self):
        with self.assertRaises(AssertionError,
            msg="Must be raise a AssertionError"):
            import_object(3)

    def test_must_not_load_invalid_module(self):
        with self.assertRaises(ImportError,
            msg="Must be raise a ImportError"):

            import_object('invalid_module.and_attribute')

    def test_must_not_load_invalid_object(self):
        my_module = types.ModuleType('my_module')
        sys.modules.setdefault('my_module', my_module)

        with self.assertRaises(AttributeError,
            msg="Must be raise a ImportError"):
            obj = import_object('my_module.object')

        sys.modules.pop('my_module')

    def test_must_not_load_an_object(self):
        my_module = types.ModuleType('my_module')
        my_module.object = object()
        sys.modules.setdefault('my_module', my_module)

        obj = import_object('my_module.object')

        self.assertEqual(
            my_module.object, obj,
            "import_object must load an object"
        )

        sys.modules.pop('my_module')


if __name__ == '__main__':
    unittest.main()
