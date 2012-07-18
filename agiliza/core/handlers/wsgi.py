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
import cgi

from agiliza import http
from agiliza.http.exceptions import HttpParserException, HttpResponseException
from agiliza.core.handlers.base import Handler


class InputProcessed(object):
    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')
    readline = readlines = __iter__ = read

class WSGIHandler(Handler):
    def is_post_request(self, env):
        if env['REQUEST_METHOD'].upper() != 'POST':
            return False

        content_type = env.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
        return content_type.startswith('application/x-www-form-urlencoded') \
            or content_type.startswith('multipart/form-data')

    def get_post_form(self, env):
        input = env['wsgi.input']
        post_form = env.get('wsgi.post_form')
        if post_form is not None and post_form[0] is input:
            return post_form[2]
        # This must be done to avoid a bug in cgi.FieldStorage
        env.setdefault('QUERY_STRING', '')
        fs = cgi.FieldStorage(
            fp=input,
            environ=env,
            keep_blank_values=1
        )
        new_input = InputProcessed()
        post_form = (new_input, input, fs)
        env['wsgi.post_form'] = post_form
        env['wsgi.input'] = new_input
        return fs

    def process_environ(self, env):

        if self.is_post_request(env):
            self.get_post_form(env)

        return env

    def __call__(self, environ, start_response):
        environ = self.process_environ(environ)

        try:
            request = http.HttpRequest(environ)
            response = self.dispatch(request)
        except (UnicodeDecodeError, HttpParserException):
            response = http.HttpResponseBadRequest()
        except HttpResponseException as exception:
            response = exception
        #except:
        #    response = http.HttpResponseInternalServerError()

        start_response(response.status, response.headers)
        return response.content
