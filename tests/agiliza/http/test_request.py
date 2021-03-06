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

from agiliza.http import HttpRequest
from agiliza.http.exceptions import HttpNegativeContentLengthException


class HttpRequestTest(unittest.TestCase):

    def get_environ(self):
        return {
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'SERVER_SOFTWARE': 'WSGIServer/0.2',
            'SCRIPT_NAME': '',
            'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '',
            'SERVER_NAME': 'tx2500',
            'SERVER_PORT': '8888',
            'REMOTE_HOST': 'localhost',
            'REMOTE_ADDR': '127.0.0.1',
            'CONTENT_TYPE': 'text/plain',
            'CONTENT_LENGTH': '',
            'HTTP_CONNECTION': 'keep-alive',
            'HTTP_CACHE_CONTROL': 'max-age=0',
            'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Linux x86_64; rv:13.0)',
            'HTTP_HOST': 'localhost:8888',
            'HTTP_ACCEPT': 'text/html,application/xhtml+xml,\
                application/xml;q=0.9,*/*;q=0.8',
            'GATEWAY_INTERFACE': 'CGI/1.1',
            'HTTP_ACCEPT_LANGUAGE': 'es-es,es;q=0.8,en-us;\
                q=0.5,en;q=0.3',
            'PATH_INFO': '/',
        }

    def get_wsgi_environ(self):
        environ = self.get_environ()

        environ.update({
            'wsgi.version': (1, 0),
            'wsgi.multiprocess': False,
            'wsgi.url_scheme': 'http',
            'wsgi.multithread': True,
            'wsgi.run_once': False,
            'wsgi.input': object(),
            'wsgi.errors': object(),
            'wsgi.file_wrapper': object(),
            #'wsgi.input': <_io.BufferedReader name=4>,
            #'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>,
            #'wsgi.file_wrapper': <class 'wsgiref.util.FileWrapper'>,
        })

        return environ


    def test_http_method_must_be_correct(self):
        environ = self.get_wsgi_environ()
        environ['REQUEST_METHOD'] = 'put'
        request = HttpRequest(environ)

        self.assertEqual(
            request.method, 'PUT',
            "Request method is incorrect in HttpRequest"
        )

    def test_path_info_must_be_correct(self):
        environ = self.get_wsgi_environ()
        environ['PATH_INFO'] = '/'
        request = HttpRequest(environ)

        self.assertEqual(
            request.path_info, '/',
            "Path info is incorrect in HttpRequest"
        )

    def test_script_name_must_be_correct(self):
        environ = self.get_wsgi_environ()
        environ['SCRIPT_NAME'] = '/myapp'
        request = HttpRequest(environ)

        self.assertEqual(
            request.script_name, '/myapp',
            "Script name is incorrect in HttpRequest"
        )

    def test_request_must_be_xhr(self):
        environ = self.get_wsgi_environ()
        environ['HTTP_X_REQUESTED_WITH'] = 'XMLHTTPRequest'
        request = HttpRequest(environ)

        self.assertTrue(request.is_xhr(), "Request must be xhr")

    def test_request_must_be_ajax(self):
        environ = self.get_wsgi_environ()
        environ['HTTP_X_REQUESTED_WITH'] = 'XMLHTTPRequest'
        request = HttpRequest(environ)

        self.assertTrue(request.is_ajax(), "Request must be ajax")

    def test_request_must_be_secure(self):
        environ = self.get_wsgi_environ()
        environ['wsgi.url_scheme'] = 'https'
        request = HttpRequest(environ)

        self.assertTrue(request.is_secure(), "Request must be secure")

    def test_host_through_http_host(self):
        environ = self.get_wsgi_environ()
        environ['HTTP_HOST'] = 'agiliza.com'
        request = HttpRequest(environ)

        self.assertEqual(
            request.get_host,
            'agiliza.com',
            "Host name is wrong"
        )

    def test_cached_host_through_http_host(self):
        environ = self.get_wsgi_environ()
        environ['HTTP_HOST'] = 'agiliza.com'
        request = HttpRequest(environ)
        host = request.get_host
        cached_host = request.get_host

        self.assertEqual(
            cached_host,
            'agiliza.com',
            "Host name is wrong"
        )

    def test_host_through_server_name(self):
        environ = self.get_wsgi_environ()
        del environ['HTTP_HOST']
        environ['SERVER_PORT'] = '80'
        environ['SERVER_NAME'] = 'agiliza.com'
        environ['wsgi.url_scheme'] = 'http'
        request = HttpRequest(environ)

        self.assertEqual(
            request.get_host,
            'agiliza.com',
            "Host name is wrong"
        )

    def test_host_through_server_name_with_different_port(self):
        environ = self.get_wsgi_environ()
        del environ['HTTP_HOST']
        environ['SERVER_PORT'] = '8080'
        environ['SERVER_NAME'] = 'agiliza.com'
        environ['wsgi.url_scheme'] = 'http'
        request = HttpRequest(environ)

        self.assertEqual(
            request.get_host,
            'agiliza.com:8080',
            "Host name is wrong"
        )

    def test_secure_host_through_server_name(self):
        environ = self.get_wsgi_environ()
        del environ['HTTP_HOST']
        environ['SERVER_PORT'] = '443'
        environ['SERVER_NAME'] = 'agiliza.com'
        environ['wsgi.url_scheme'] = 'https'
        request = HttpRequest(environ)

        self.assertEqual(
            request.get_host,
            'agiliza.com',
            "Host name is wrong"
        )

    def test_secure_host_through_server_name_with_different_port(self):
        environ = self.get_wsgi_environ()
        del environ['HTTP_HOST']
        environ['SERVER_PORT'] = '9999'
        environ['SERVER_NAME'] = 'agiliza.com'
        environ['wsgi.url_scheme'] = 'https'
        request = HttpRequest(environ)

        self.assertEqual(
            request.get_host,
            'agiliza.com:9999',
            "Host name is wrong"
        )

    def test_query_must_be_correct(self):
        environ = self.get_wsgi_environ()
        environ['QUERY_STRING'] = 'field1=value1&field2=value2'

        request = HttpRequest(environ)
        query = request.query

        self.assertDictEqual(query, {
                'field1': ['value1'],
                'field2': ['value2'],
            },
            "Query does not fetch right values"
        )

    def test_query_must_be_cached(self):
        environ = self.get_wsgi_environ()
        environ['QUERY_STRING'] = 'field1=value1&field2=value2'

        request = HttpRequest(environ)
        query = request.query
        query2 = request.query

        self.assertDictEqual(query2, {
                'field1': ['value1'],
                'field2': ['value2'],
            },
            "Query does not fetch right values"
        )

    def test_content_length_must_be_correct(self):
        environ = self.get_wsgi_environ()
        environ['CONTENT_LENGTH'] = '123'
        request = HttpRequest(environ)

        self.assertEqual(
            request.content_length, 123,
            "Content length is incorrect in HttpRequest"
        )

    def test_content_length_must_be_0_if_not_present(self):
        environ = self.get_wsgi_environ()
        del environ['CONTENT_LENGTH']
        request = HttpRequest(environ)

        self.assertEqual(
            request.content_length, 0,
            "Content length must be 0 if not present"
        )

    def test_content_length_must_launch_an_exception_if_negative(self):
        environ = self.get_wsgi_environ()
        environ['CONTENT_LENGTH'] = '-1'

        with self.assertRaises(HttpNegativeContentLengthException,
            msg="Content length is negative"):
            request = HttpRequest(environ)

    def test_request_must_be_printable(self):
        environ = self.get_wsgi_environ()
        environ['REQUEST_METHOD'] = 'POST'
        environ['PATH_INFO'] = '/myapp'
        request = HttpRequest(environ)

        self.assertEqual(
            str(request), 'HttpRequest <POST /myapp HTTP/%s>' % request.VERSION,
            "Response must be printable"
        )


if __name__ == '__main__':
    unittest.main()
