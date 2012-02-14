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
        <form action="." method="post">
        <p><input type="text" name="username" id="username" /></p>
        <input type="password" name="password" id="password" /></p>
        <p><input type="checkbox" name="item" value="1" />
        <input type="checkbox" name="item" value="2" /></p>
        <p><input type="submit" value="Submit" /></p>
        </form>
        </body>
        </html>
        ''' % request.query
        return HttpResponseOk(content=form)

    @method(allow=['PUT', 'POST'])
    def change(self, request):
        print('change method')
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
        resource = Test()
        return resource.dispatch(request)
