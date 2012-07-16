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
from agiliza import http
from agiliza.http.exceptions import HttpParserException, HttpResponseException
from agiliza.core.handlers import Handler


class WSGIHandler(Handler):
    def __call__(self, environ, start_response):

        try:
            request = http.HttpRequest(environ)
            response = self.dispatch(request)
        except (UnicodeDecodeError, HttpParserException):
            response = http.HttpResponseBadRequest()
        except HttpResponseException as exception:
            response = exception
        except:
            response = http.HttpResponseInternalServerError()

        start_response(response.status, response.headers)
        return response.content
