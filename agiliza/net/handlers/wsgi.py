from agiliza.net import http
from agiliza.net.handlers import base


class WSGIHandler(base.BaseHandler):
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
