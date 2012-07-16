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
along with Agiliza.  If not, see <http://www.gnu.org/licenses/>.


Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
import importlib
import unittest

from agiliza.core.utils.decorators import cached_property


class CachedPropertyTest(unittest.TestCase):

    def get_example_object(self):

        class ExampleObject(object):
            @cached_property
            def some_value(self):
                return 5

        return ExampleObject()


    def test_must_raise_an_attribute_error(self):
        obj = self.get_example_object()

        with self.assertRaises(AttributeError,
            msg="Must be raise an AttributeError"):
            getattr(obj, '_lazy_some_value')

    def test_must_get_some_value_first_time(self):
        obj = self.get_example_object()

        self.assertEqual(
            obj.some_value, 5,
            "cached_property does not get right value"
        )

    def test_must_get_some_value_multiple_times(self):
        obj = self.get_example_object()
        some_value = obj.some_value
        some_value = obj.some_value
        some_value = obj.some_value

        self.assertEqual(
            some_value, 5,
            "cached_property does not get right value"
        )

if __name__ == '__main__':
    unittest.main()
