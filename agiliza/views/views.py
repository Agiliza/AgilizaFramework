from agiliza.net.protocols.http import HTTP_METHODS

def resource(allow, accept=('text/html',)):
        print('Resource', allow, accept)
        def info(target):
            print('Info', target)
            target.allow = allow
            target.accept = accept
            return target
        return info

class View(object):
    def __init__(self):
        self._get_resources = {}
        self._post_resources = {}
        self._update_resources = {}
        self._delete_resources = {}
        self._head_resources = {}
        self._options_resources = {}

        for att_name in dir(self):
            att = getattr(self, att_name)
            if callable(att) and hasattr(att, 'allow'):
                self._add_resource(att)

    def _add_resource(self, method):
        for http_method in method.allow:
            if not http_method in HTTP_METHODS:
                raise #  TODO -> custom exception
            resources_name = '_%s_resources' % http_method.lower()
            resources = getattr(self, resources_name)

            for content_type in method.accept:
                resources[content_type] = method

    def dispatch(self, request, *args, **kwargs):
        method_name = request.method.lower()
        try:
            method = getattr(self, method_name)
            response = method(request, *args, **kwargs)
        except AttributeError as e:
            response = http.HttpResponseMethodNotAllowed()

        # TODO warning if response.content_type is not in method.accept
        return response
