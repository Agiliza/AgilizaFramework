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


Copyright (c) 2012 Alvaro Hurtado <alvarohurtado84@gmail.com>
"""
import unittest
import sys

from agiliza.utils import slugify


class SlugifyTest(unittest.TestCase):

    def test_simple_slug(self):
        slug = slugify("Á b c y ótras")

        self.assertEqual(
            slug,
            "a-b-c-y-otras",
            msg="Slugify must create a slug without spaces, tildes..."
        )
        
    def test_slug_with_symbols(self):
        slug = slugify("aaa ?? aaa")
        
        self.assertEqual(
            slug,
            "aaa-aaa",
            msg="Slugify must remove symbols"
        )


if __name__ == '__main__':
    unittest.main()
