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


class HttpResponseStatusTest(unittest.TestCase):

    def test_check_status_code_and_status_text_of_100(self):
        response = http.Http100()

        self.assertEqual(
            (response.status_code, response.status_text),
            (100, 'CONTINUE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_101(self):
        response = http.Http101()

        self.assertEqual(
            (response.status_code, response.status_text),
            (101, 'SWITCHING PROTOCOLS'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_200(self):
        response = http.Http200()

        self.assertEqual(
            (response.status_code, response.status_text),
            (200, 'OK'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_201(self):
        response = http.Http201()

        self.assertEqual(
            (response.status_code, response.status_text),
            (201, 'CREATED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_202(self):
        response = http.Http202()

        self.assertEqual(
            (response.status_code, response.status_text),
            (202, 'ACCEPTED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_203(self):
        response = http.Http203()

        self.assertEqual(
            (response.status_code, response.status_text),
            (203, 'NON-AUTHORITATIVE INFORMATION'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_204(self):
        response = http.Http204()

        self.assertEqual(
            (response.status_code, response.status_text),
            (204, 'NO CONTENT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_205(self):
        response = http.Http205()

        self.assertEqual(
            (response.status_code, response.status_text),
            (205, 'RESET CONTENT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_206(self):
        response = http.Http206()

        self.assertEqual(
            (response.status_code, response.status_text),
            (206, 'PARTIAL CONTENT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_300(self):
        response = http.Http300('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (300, 'MULTIPLE CHOICES'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_301(self):
        response = http.Http301('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (301, 'MOVED PERMANENTLY'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_302(self):
        response = http.Http302('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (302, 'FOUND'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_303(self):
        response = http.Http303('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (303, 'SEE OTHER'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_304(self):
        response = http.Http304()

        self.assertEqual(
            (response.status_code, response.status_text),
            (304, 'NOT MODIFIED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_305(self):
        response = http.Http305('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (305, 'USE PROXY'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_307(self):
        response = http.Http307('/redirect/to')

        self.assertEqual(
            (response.status_code, response.status_text),
            (307, 'TEMPORARY REDIRECT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_400(self):
        response = http.Http400()

        self.assertEqual(
            (response.status_code, response.status_text),
            (400, 'BAD REQUEST'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_401(self):
        response = http.Http401()

        self.assertEqual(
            (response.status_code, response.status_text),
            (401, 'UNAUTHORIZED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_402(self):
        response = http.Http402()

        self.assertEqual(
            (response.status_code, response.status_text),
            (402, 'PAYMENT REQUIRED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_403(self):
        response = http.Http403()

        self.assertEqual(
            (response.status_code, response.status_text),
            (403, 'FORBIDDEN'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_404(self):
        response = http.Http404()

        self.assertEqual(
            (response.status_code, response.status_text),
            (404, 'NOT FOUND'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_405(self):
        response = http.Http405(['GET',])

        self.assertEqual(
            (response.status_code, response.status_text),
            (405, 'METHOD NOT ALLOWED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_406(self):
        response = http.Http406()

        self.assertEqual(
            (response.status_code, response.status_text),
            (406, 'NOT ACCEPTABLE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_407(self):
        response = http.Http407()

        self.assertEqual(
            (response.status_code, response.status_text),
            (407, 'PROXY AUTHENTICATION REQUIRED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_408(self):
        response = http.Http408()

        self.assertEqual(
            (response.status_code, response.status_text),
            (408, 'REQUEST TIMEOUT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_409(self):
        response = http.Http409()

        self.assertEqual(
            (response.status_code, response.status_text),
            (409, 'CONFLICT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_410(self):
        response = http.Http410()

        self.assertEqual(
            (response.status_code, response.status_text),
            (410, 'GONE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_411(self):
        response = http.Http411()

        self.assertEqual(
            (response.status_code, response.status_text),
            (411, 'LENGTH REQUIRED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_412(self):
        response = http.Http412()

        self.assertEqual(
            (response.status_code, response.status_text),
            (412, 'PRECONDITION FAILED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_413(self):
        response = http.Http413()

        self.assertEqual(
            (response.status_code, response.status_text),
            (413, 'REQUEST ENTITY TOO LARGE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_414(self):
        response = http.Http414()

        self.assertEqual(
            (response.status_code, response.status_text),
            (414, 'REQUEST-URI TOO LONG'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_415(self):
        response = http.Http415()

        self.assertEqual(
            (response.status_code, response.status_text),
            (415, 'UNSUPPORTED MEDIA TYPE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_416(self):
        response = http.Http416()

        self.assertEqual(
            (response.status_code, response.status_text),
            (416, 'REQUESTED RANGE NOT SATISFIABLE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_417(self):
        response = http.Http417()

        self.assertEqual(
            (response.status_code, response.status_text),
            (417, 'EXPECTATION FAILED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_500(self):
        response = http.Http500()

        self.assertEqual(
            (response.status_code, response.status_text),
            (500, 'INTERNAL SERVER ERROR'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_501(self):
        response = http.Http501()

        self.assertEqual(
            (response.status_code, response.status_text),
            (501, 'NOT IMPLEMENTED'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_502(self):
        response = http.Http502()

        self.assertEqual(
            (response.status_code, response.status_text),
            (502, 'BAD GATEWAY'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_503(self):
        response = http.Http503()

        self.assertEqual(
            (response.status_code, response.status_text),
            (503, 'SERVICE UNAVAILABLE'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_504(self):
        response = http.Http504()

        self.assertEqual(
            (response.status_code, response.status_text),
            (504, 'GATEWAY TIMEOUT'),
            "Status code or status text does not mismatch"
        )

    def test_check_status_code_and_status_text_of_505(self):
        response = http.Http505()

        self.assertEqual(
            (response.status_code, response.status_text),
            (505, 'HTTP VERSION NOT SUPPORTED'),
            "Status code or status text does not mismatch"
        )


    def test_check_status_of_100(self):
        response = http.Http100()

        self.assertEqual(
            response.status, '100 CONTINUE',
            "Status of response is wrong"
        )

    def test_check_status_of_101(self):
        response = http.Http101()

        self.assertEqual(
            response.status, '101 SWITCHING PROTOCOLS',
            "Status of response is wrong"
        )

    def test_check_status_of_200(self):
        response = http.Http200()

        self.assertEqual(
            response.status, '200 OK',
            "Status of response is wrong"
        )

    def test_check_status_of_201(self):
        response = http.Http201()

        self.assertEqual(
            response.status, '201 CREATED',
            "Status of response is wrong"
        )

    def test_check_status_of_202(self):
        response = http.Http202()

        self.assertEqual(
            response.status, '202 ACCEPTED',
            "Status of response is wrong"
        )

    def test_check_status_of_203(self):
        response = http.Http203()

        self.assertEqual(
            response.status, '203 NON-AUTHORITATIVE INFORMATION',
            "Status of response is wrong"
        )

    def test_check_status_of_204(self):
        response = http.Http204()

        self.assertEqual(
            response.status, '204 NO CONTENT',
            "Status of response is wrong"
        )

    def test_check_status_of_205(self):
        response = http.Http205()

        self.assertEqual(
            response.status, '205 RESET CONTENT',
            "Status of response is wrong"
        )

    def test_check_status_of_206(self):
        response = http.Http206()

        self.assertEqual(
            response.status, '206 PARTIAL CONTENT',
            "Status of response is wrong"
        )

    def test_check_status_of_300(self):
        response = http.Http300('/redirect/to')

        self.assertEqual(
            response.status, '300 MULTIPLE CHOICES',
            "Status of response is wrong"
        )

    def test_check_status_of_301(self):
        response = http.Http301('/redirect/to')

        self.assertEqual(
            response.status, '301 MOVED PERMANENTLY',
            "Status of response is wrong"
        )

    def test_check_status_of_302(self):
        response = http.Http302('/redirect/to')

        self.assertEqual(
            response.status, '302 FOUND',
            "Status of response is wrong"
        )

    def test_check_status_of_303(self):
        response = http.Http303('/redirect/to')

        self.assertEqual(
            response.status, '303 SEE OTHER',
            "Status of response is wrong"
        )

    def test_check_status_of_304(self):
        response = http.Http304()

        self.assertEqual(
            response.status, '304 NOT MODIFIED',
            "Status of response is wrong"
        )

    def test_check_status_of_305(self):
        response = http.Http305('/redirect/to')

        self.assertEqual(
            response.status, '305 USE PROXY',
            "Status of response is wrong"
        )

    def test_check_status_of_307(self):
        response = http.Http307('/redirect/to')

        self.assertEqual(
            response.status, '307 TEMPORARY REDIRECT',
            "Status of response is wrong"
        )

    def test_check_status_of_400(self):
        response = http.Http400()

        self.assertEqual(
            response.status, '400 BAD REQUEST',
            "Status of response is wrong"
        )

    def test_check_status_of_401(self):
        response = http.Http401()

        self.assertEqual(
            response.status, '401 UNAUTHORIZED',
            "Status of response is wrong"
        )

    def test_check_status_of_402(self):
        response = http.Http402()

        self.assertEqual(
            response.status, '402 PAYMENT REQUIRED',
            "Status of response is wrong"
        )

    def test_check_status_of_403(self):
        response = http.Http403()

        self.assertEqual(
            response.status, '403 FORBIDDEN',
            "Status of response is wrong"
        )

    def test_check_status_of_404(self):
        response = http.Http404()

        self.assertEqual(
            response.status, '404 NOT FOUND',
            "Status of response is wrong"
        )

    def test_check_status_of_405(self):
        response = http.Http405(['GET',])

        self.assertEqual(
            response.status, '405 METHOD NOT ALLOWED',
            "Status of response is wrong"
        )

    def test_check_status_of_406(self):
        response = http.Http406()

        self.assertEqual(
            response.status, '406 NOT ACCEPTABLE',
            "Status of response is wrong"
        )

    def test_check_status_of_407(self):
        response = http.Http407()

        self.assertEqual(
            response.status, '407 PROXY AUTHENTICATION REQUIRED',
            "Status of response is wrong"
        )

    def test_check_status_of_408(self):
        response = http.Http408()

        self.assertEqual(
            response.status, '408 REQUEST TIMEOUT',
            "Status of response is wrong"
        )

    def test_check_status_of_409(self):
        response = http.Http409()

        self.assertEqual(
            response.status, '409 CONFLICT',
            "Status of response is wrong"
        )

    def test_check_status_of_410(self):
        response = http.Http410()

        self.assertEqual(
            response.status, '410 GONE',
            "Status of response is wrong"
        )

    def test_check_status_of_411(self):
        response = http.Http411()

        self.assertEqual(
            response.status, '411 LENGTH REQUIRED',
            "Status of response is wrong"
        )

    def test_check_status_of_412(self):
        response = http.Http412()

        self.assertEqual(
            response.status, '412 PRECONDITION FAILED',
            "Status of response is wrong"
        )

    def test_check_status_of_413(self):
        response = http.Http413()

        self.assertEqual(
            response.status, '413 REQUEST ENTITY TOO LARGE',
            "Status of response is wrong"
        )

    def test_check_status_of_414(self):
        response = http.Http414()

        self.assertEqual(
            response.status, '414 REQUEST-URI TOO LONG',
            "Status of response is wrong"
        )

    def test_check_status_of_415(self):
        response = http.Http415()

        self.assertEqual(
            response.status, '415 UNSUPPORTED MEDIA TYPE',
            "Status of response is wrong"
        )

    def test_check_status_of_416(self):
        response = http.Http416()

        self.assertEqual(
            response.status, '416 REQUESTED RANGE NOT SATISFIABLE',
            "Status of response is wrong"
        )

    def test_check_status_of_417(self):
        response = http.Http417()

        self.assertEqual(
            response.status, '417 EXPECTATION FAILED',
            "Status of response is wrong"
        )

    def test_check_status_of_500(self):
        response = http.Http500()

        self.assertEqual(
            response.status, '500 INTERNAL SERVER ERROR',
            "Status of response is wrong"
        )

    def test_check_status_of_501(self):
        response = http.Http501()

        self.assertEqual(
            response.status, '501 NOT IMPLEMENTED',
            "Status of response is wrong"
        )

    def test_check_status_of_502(self):
        response = http.Http502()

        self.assertEqual(
            response.status, '502 BAD GATEWAY',
            "Status of response is wrong"
        )

    def test_check_status_of_503(self):
        response = http.Http503()

        self.assertEqual(
            response.status, '503 SERVICE UNAVAILABLE',
            "Status of response is wrong"
        )

    def test_check_status_of_504(self):
        response = http.Http504()

        self.assertEqual(
            response.status, '504 GATEWAY TIMEOUT',
            "Status of response is wrong"
        )

    def test_check_status_of_505(self):
        response = http.Http505()

        self.assertEqual(
            response.status, '505 HTTP VERSION NOT SUPPORTED',
            "Status of response is wrong"
        )


if __name__ == '__main__':
    unittest.main()
