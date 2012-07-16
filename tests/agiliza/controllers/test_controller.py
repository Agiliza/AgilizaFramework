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
from agiliza.controllers import Controller
from tests.mocks.controllers import *
from tests.mocks.request import HttpRequestMock


class ControllerTest(unittest.TestCase):

    def setUp(self):
        self.request = HttpRequestMock()

    def test_controller_does_not_have_get_method(self):
        self.request.method = 'GET'
        c = Controller()

        with self.assertRaises(http.HttpResponseMethodNotAllowed,
            msg="Must be raise a HttpResponseMethodNotAllowed"):
            c.dispatch(self.request, None, None, None, None)

    def test_must_launch_get_method(self):
        self.request.method = 'GET'
        c = GetControllerMock()
        context_data = c.dispatch(self.request, None, None, None, None)

        self.assertEqual(
            context_data, {},
            "Controller dispatch does not launch get method"
        )

    def test_must_retrieve_permitted_methods_for_put_method(self):
        c = PutControllerMock()

        self.assertEqual(
            c.permitted_methods, ('PUT',),
            "Wrong permitted methods for PutControllerMock"
        )

    def test_must_retrieve_permitted_methods_for_all_methods(self):
        c = CompleteControllerMock()

        self.assertEqual(
            c.permitted_methods, ('GET', 'POST', 'PUT', 'DELETE'),
            "Wrong permitted methods for CompleteControllerMock"
        )


if __name__ == '__main__':
    unittest.main()
