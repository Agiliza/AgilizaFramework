from agiliza.net.http import HttpResponseOk

# Just a test
from agiliza.resources import Resource, method
class Test(Resource):
    @method(allow='GET')
    def get(self, request):
        print('get method')
        return HttpResponseOk('Método get')

    @method(allow=['PUT', 'POST'])
    def change(self, request):
        print('change method')
        return HttpResponseOk('Método change')

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
