"""

PEP 3333

environ Variables

 - REQUEST_METHOD
 - SCRIPT_NAME
 - PATH_INFO
 - QUERY_STRING
 - CONTENT_TYPE
 - CONTENT_LENGTH
 - SERVER_NAME, SERVER_PORT
 - SERVER_PROTOCOL
 - HTTP_ Variables
"""
from agiliza.net import http
from agiliza.net.handlers import base


class WSGIRequest(http.HttpRequest):
    def __init__(self, environ):
        """Wrap a WSGI environ dictionary."""
        self.META = environ
        self._method = environ['REQUEST_METHOD'].upper()

    @property
    def method(self):
        return self._method

    @property
    def path_info(self):
        return '/' + self.META.get('PATH_INFO','').lstrip('/')

    @property
    def query_string(self):
        return '/' + self.META.get('QUERY_STRING','')

    @property
    def script_name(self):
        return self.environ.get('SCRIPT_NAME', '')

    def is_secure(self):
        return 'wsgi.url_scheme' in self.environ \
            and self.environ['wsgi.url_scheme'] == 'https'




class WSGIHandler(base.BaseHandler):
    def __call__(self, environ, start_response):
        try:
            request = WSGIRequest(environ)
        except UnicodeDecodeError:
            response = http.HttpResponseBadRequest()
        else:
            response = self.get_response(request)

        print('REQUEST')
        print('is_secure:',request.is_secure())
        print('is_ajax:',request.is_ajax())
        print('is_xhr:',request.is_xhr())
        print('get_host:',request.get_host())
        print('path_info:',request.path_info)
        print('method:',request.method)
        print('query_string:',request.query_string)
        print('script_name:',request.script_name)

        start_response(response.status, response.headers)
        return response.body
