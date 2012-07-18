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
import unittest

from agiliza.core.utils.patterns import Singleton


class SingletonTest(unittest.TestCase):

    def test_must_retrieve_the_same_instance(self):
        class SingletonExample(Singleton): pass

        instance1 = SingletonExample()
        instance2 = SingletonExample.getInstance()

        self.assertEqual(
            instance1, instance2,
            "Singleton makes different instances"
        )

    def test_must_retrieve_the_same_instance_multiple_times(self):
        class SingletonExample(Singleton): pass

        instance1 = SingletonExample()

        SingletonExample()
        SingletonExample()

        instance2 = SingletonExample()

        self.assertEqual(
            instance1, instance2,
            "Singleton makes different instances"
        )

    def test_must_invalidate_a_instance(self):
        class SingletonExample(Singleton): pass

        instance1 = SingletonExample.getInstance()
        SingletonExample.invalidateInstance()
        instance2 = SingletonExample()

        self.assertNotEqual(
            instance1, instance2,
            "Singleton does not invalidate instances"
        )

if __name__ == '__main__':
    unittest.main()
