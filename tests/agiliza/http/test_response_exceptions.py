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


class HttpResponseExceptionTest(unittest.TestCase):

    def test_raise_400(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http400

    def test_raise_401(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http401

    def test_raise_402(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http402

    def test_raise_403(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http403

    def test_raise_404(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http404

    def test_raise_405(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http405(['GET',])

    def test_raise_406(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http406

    def test_raise_407(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http407

    def test_raise_408(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http408

    def test_raise_409(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http409

    def test_raise_410(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http410

    def test_raise_411(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http411

    def test_raise_412(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http412

    def test_raise_413(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http413

    def test_raise_414(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http414

    def test_raise_415(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http415

    def test_raise_416(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http416

    def test_raise_417(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http417

    def test_raise_500(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http500

    def test_raise_501(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http501

    def test_raise_502(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http502

    def test_raise_503(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http503

    def test_raise_504(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http504

    def test_raise_505(self):
        with self.assertRaises(http.HttpResponseException,
            msg="Must be raise a HttpResponseException"):
            raise http.Http505

if __name__ == '__main__':
    unittest.main()
