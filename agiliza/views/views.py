from agiliza.net.protocols import http


class View(object):
    def dispatch(self, request, *args, **kwargs):
        method_name = request.method.lower()
        try:
            method = getattr(self, method_name)
            response = method(request, *args, **kwargs)
        except AttributeError as e:
            response = http.HttpResponseMethodNotAllowed()

        return response
