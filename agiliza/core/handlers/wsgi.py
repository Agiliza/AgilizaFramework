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
from agiliza.core.handlers import Handler


class WSGIHandler(Handler):
    def __call__(self, environ, start_response):
        print(environ)
        try:
            request = http.HttpRequest(environ)
        except UnicodeDecodeError:
            response = http.HttpResponseBadRequest()
        else:
            response = self.get_response(request)

        print()
        print('REQUEST')
        print('is_secure:',request.is_secure())
        print('is_ajax:',request.is_ajax())
        print('is_xhr:',request.is_xhr())
        print('get_host:',request.get_host())
        print('full path:',request.get_full_path())
        print('path_info:',request.path_info)
        print('method:',request.method)
        print('query_string:',request.query_string)
        print('script_name:',request.script_name)
        print('accept:',request.accept)
        print()
        print('query:',request.query)
        print('data:',request.data)
        print('files:',request.files)
        print()

        start_response(response.status, response.headers)
        return response.content
