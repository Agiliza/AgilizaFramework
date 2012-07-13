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

from agiliza import http


class HttpResponseTest(unittest.TestCase):

    def test_content_type_must_be_correct(self):
        response = http.Http200(content_type='text/html; charset=ascii')

        self.assertEqual(
            response.content_type, 'text/html',
            "Content type must be correct"
        )

    def test_content_could_be_iterable(self):
        response = http.Http200(content=['line1', 'line2'])

        self.assertEqual(
            response._content, ['line1', 'line2'],
            "Content type could be iterable"
        )

    def test_response_must_be_printable(self):
        response = http.Http200()

        self.assertEqual(
            str(response), 'HttpResponse <200, OK>',
            "Response must be printable"
        )


if __name__ == '__main__':
    unittest.main()
