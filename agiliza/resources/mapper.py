from agiliza.net import http


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
            if not http_method in self._resources:
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

            resource_method[media_type][media_subtype] = method

    def find(self, http_method, accept_list):
        # Get info about ``http_method`` for this resource
        try:
            resource_method = self._resources[http_method]
        except KeyError:
            raise MethodNotAllowedException()

        # Look for the appropiate media
        for media in accept_list:
            media_type, media_subtype = media.split('/')
            if media_type in resource_method:
                if media_subtype in resource_method[media_type]:
                    return resource_method[media_type][media_subtype]
                if media_subtype == '*':
                    all_subtypes = resource_method[media_type].values()
                    first_subtype = list(all_subtypes)[0]
                    return first_subtype
            elif media_type == '*':
                all_types = resource_method.values()
                first_type = list(all_types)[0]
                all_subtypes = first_type.values()
                first_subtype = list(all_subtypes)[0]
                return first_subtype


        # No method found
        supported_media = []
        [
            list(
                map(
                    lambda x: supported_media.append(key + '/' + x),
                    value.keys()
                )
            )
            for key, value in resource_method.items()
        ]
        exception = NotAcceptableException()
        exception.supported_media = supported_media
        raise exception

    def allow_methods(self):
        return self._resources.keys()
