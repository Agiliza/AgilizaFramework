import collections

from agiliza.net import http
from agiliza.net.http.exceptions import (MethodNotAllowedException,
    NotAcceptableException)


def method(allow, accept='text/html'):
        def info(target):
            allow_list = allow
            if isinstance(allow, str):
                allow_list = [allow, ]

            if not isinstance(allow_list, collections.Iterable):
                raise ValueError(
                    "In a method, allow parameter must be iterable")

            if not isinstance(accept, str):
                raise ValueError("In a method, accept must be a string")

            target.allow = allow_list
            target.accept = accept.strip()
            return target

        return info


class ResourceMapper(object):
    """
    Store info about media types/subtypes and the appropiate method for
    serving the a request.

    {
        'GET': {
            'text': {
                'html': method1,
                'xml': method2,
            },
            'audio': {
                'basic': method3,
            },
        },
        'POST': {
            'text': {
                'html': method1,
            },
        },
        'PUT': {
            'text': {
                'xml': method2,
            },
        },
    }
    """
    def __init__(self):
        self._resources = {}

    def add(self, method):
        for http_method in method.allow:
            # Check if ``http_method`` is a valid method
            if not http_method in http.HTTP_METHODS:
                raise ValueError("Method %s not valid" % http_method)
            # Check if its data structure is created
            if not self._resources.has_key(http_method):
                self._resources[http_method] = {}
            resource_method = self._resources[http_method]

            media_type, media_subtype = method.accept.split('/')

            # Check if media is present in the dict
            if media_type in resource_method.keys():
                if media_subtype in resource_method[media_type].keys():
                    # TODO warning
                    pass
            else:
                resource_method[media_type] = {}

            resource_method[media_type][media_sybtype] = method

    def find(self, http_method, accept_list):
        # Get info about ``http_method`` for this resource
        try:
            resource_method = self._resources[http_method]
        except KeyError:
            raise MethodNotAllowedException()

        # Look for the appropiate media
        for q, media in accept_list:
            media_type, media_subtype = media.split('/')
            if resource_method.has_key(media_type):
                if resource_method[media_type].has_key(media_subtype):
                    return resource_method[media_type][media_subtype]


        # No method found
        supported_media = []
        [
            list(
                map(
                    lambda x: supported_media.append(key + '/' + x),
                    value.keys()
                )
            )
            for key, value in a.items()
        ]
        exception = NotAcceptableException()
        exception.supported_media = supported_media
        raise exception

    def allow_methods(self):
        return self._resources.keys()


class Resource(object):
    def __init__(self):
        self._mapper = ResourceMapper()

        for att_name in dir(self): #  TODO move to metaclass?
            att = getattr(self, att_name)
            if callable(att) and hasattr(att, 'allow'):
                self._mapper.add(att)

    def dispatch(self, request, *args, **kwargs):
        allow_list = self._mapper.allow_methods()
        if not request.method in allow_list:
            return http.HttpResponseMethodNotAllowed(allow_list)

        accept = sorted([ (q, t) for t, q in request.accept.items() ])
        accept_list = tuple(map(lambda x: x[1], accept))
        try:
            method = self._mapper.find(request.method, accept_list)
            response = method(request, *args, **kwargs)
        except MethodNotAllowedException:
            response = http.HttpResponseMethodNotAllowed(allow_list)
        except NotAcceptableException as exception:
            response = http.HttpResponse <--

        # TODO warning if response.content_type is not in method.accept
        return response
