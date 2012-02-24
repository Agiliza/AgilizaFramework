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
from agiliza.net.http import HttpResponseOk

# Just a test
from agiliza.resources import Resource
class Test(Resource):
    @method(allow='GET')
    def get(self, request):
        print('get method')
        form = '''
        <html><head></head>
        <body>
        <p>%s</p>
        <form name="uno" action="/otra" method="get">
        <p><input type="text" name="username" id="username" /></p>
        <input type="password" name="password" id="password" /></p>
        <p><input type="checkbox" name="item" value="1" />
        <input type="checkbox" name="item" value="2" /></p>
        <p><input type="submit" value="Submit" /></p>
        </form>
        <br />
        <form action="." method="post" enctype="multipart/form-data">
        <input type="file" name="failas" />
        <input type="submit" value="Varom" />
        </form>
        </body>
        </html>
        ''' % request.query
        return HttpResponseOk(content=form)

    @method(allow=['PUT', 'POST'])
    def change(self, request):
        print('change method')
        return HttpResponseOk(str(request.data))

class Test1(Resource):
    @method(allow='GET')
    def get(self, request):
        return HttpResponseOk(str(request.data))

class BaseHandler(object):
    def __init__(self):
        try:
            self.load_middleware()
        except:
            # Unload whatever middleware we got
            self._request_middleware = None
            raise

    def load_middleware(self):
        """Populate middleware lists."""
        pass

    def get_response(self, request):
        """Returns an Response object for the given Request."""
        if request.path_info == '/otra':
            resource = Test1()
        else:
            resource = Test()
        return resource.dispatch(request)
