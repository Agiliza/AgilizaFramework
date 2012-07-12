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
from agiliza.http.exceptions import HttpAcceptHeaderParserException
from agiliza.http.parser import parse_accept_header


class ParseAcceptHeaderTest(unittest.TestCase):

    def test_must_accept_all_types(self):
        parsed_header = parse_accept_header('*/*')

        self.assertDictEqual(
            parsed_header, { '*/*': 1.0 },
            "Does not accept all types"
        )

    def test_must_not_validate_some_text(self):
        with self.assertRaises(HttpAcceptHeaderParserException,
                               msg="ACCEPT HEADER must not validate 'Some text'"):
            parse_accept_header('Some text')

    def test_must_not_validate_only_a_type(self):
        with self.assertRaises(HttpAcceptHeaderParserException,
                               msg="ACCEPT HEADER must contains subtype"):
            parse_accept_header('text')

    def test_must_accept_multiple_types(self):
        parsed_header = parse_accept_header('text/plain; q=0.5,\
            text/html, text/x-dvi; q=0.8, text/x-c')

        self.assertDictEqual(parsed_header, {
                'text/plain': 0.5,
                'text/html': 1.0,
                'text/x-dvi': 0.8,
                'text/x-c': 1.0,
            },
            "ACCEPT HEADER do not accept multiple types",
        )
        
    def test_must_accept_multiple_types_with_plus_symbols(self):
        parsed_header = parse_accept_header('text/plain; q=0.5,\
            text/xhtml+xml, text/x-dvi; q=0.8, text/x-c')

        self.assertDictEqual(parsed_header, {
                'text/plain': 0.5,
                'text/xhtml+xml': 1.0,
                'text/x-dvi': 0.8,
                'text/x-c': 1.0,
            },
            "ACCEPT HEADER do not accept multiple types with plus symbols",
        )

    def test_must_not_validate_without_semicolon(self):
        with self.assertRaises(HttpAcceptHeaderParserException,
                               msg="ACCEPT HEADER must not validate without\
                               semicolon"):
            parse_accept_header('text/plain q=0.5')
            
    def test_must_accept_multiple_types_even_one_without_semicolon(self):
        with self.assertRaises(HttpAcceptHeaderParserException,
                               msg="ACCEPT HEADER must not validate without\
                               semicolon even with multiple types"):
            parsed_header = parse_accept_header('text/plain q=0.5,\
                text/html, text/x-dvi; q=0.8, text/x-c')


if __name__ == '__main__':
    unittest.main()
