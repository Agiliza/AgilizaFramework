import collections

from agiliza.net import http
from agiliza.net.http.exceptions import AllowHeaderValuesException


def method(allow, accept='text/html'):
        def info(target):
            allow_list = allow
            if isinstance(allow, str):
                allow_list = [allow, ]

            if not isinstance(allow_list, collections.Iterable):
                raise AllowHeaderValuesException(
                    "In a method, allow parameter must be iterable")

            if not isinstance(accept, str):
                raise ValueError("In a method, accept must be a string")

            target.allow = allow_list
            target.accept = accept
            return target

        return info


class Resource(object):
    def __init__(self):
        self._allow_methods = set()
        self._get_resources = {}
        self._post_resources = {}
        self._put_resources = {}
        self._delete_resources = {}
        self._head_resources = {}
        self._options_resources = {}

        for att_name in dir(self):
            att = getattr(self, att_name)
            if callable(att) and hasattr(att, 'allow'):
                self._add_method(att)

    def _add_method(self, method):
        for http_method in method.allow:
            if not http_method in http.HTTP_METHODS:
                raise ValueError("Method %s not valid" % http_method)
            resources_name = '_%s_resources' % http_method.lower()
            resources = getattr(self, resources_name)
            self._allow_methods.add(http_method.upper())

            for content_type in method.accept:
                resources[content_type] = method

    def dispatch(self, request, *args, **kwargs):
        if not request.method in self._allow_methods:
            return http.HttpResponseMethodNotAllowed(allow_list)

        method_name = request.method.lower()
        try:
            method = getattr(self, method_name)
            response = method(request, *args, **kwargs)
        except AttributeError:
            allow_list = list(self._allow_methods)
            response = http.HttpResponseMethodNotAllowed(allow_list)

        # TODO warning if response.content_type is not in method.accept
        return response
