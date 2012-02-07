from agiliza.net.http import HttpResponseOk


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
        return HttpResponseOk()
