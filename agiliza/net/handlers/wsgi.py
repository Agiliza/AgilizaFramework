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
        script_name = environ.get('SCRIPT_NAME')
        path_info = environ.get('PATH_INFO', '/')
        if not path_info or path_info == script_name:
            # Sometimes PATH_INFO exists, but is empty (e.g. accessing
            # the SCRIPT_NAME URL without a trailing slash). We really need to
            # operate as if they'd requested '/'. Not amazingly nice to force
            # the path like this, but should be harmless.
            path_info = '/'
        self.environ = environ
        self.path_info = path_info
        self.path = '%s%s' % (script_name, path_info)
        self.method = environ['REQUEST_METHOD'].upper()
        self._stream = self.environ['wsgi.input']

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

        start_response(response.status, response.headers)
        return response.body
