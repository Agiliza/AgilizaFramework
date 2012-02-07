# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3
from agiliza.net.http.response import HttpResponse


class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300
    status_text = 'MULTIPLE CHOICES'

    def __init__(self, preferred_location=None):
        super(HttpResponseMultipleChoices, self).__init__()
        if preferred_location:
            self['Location'] = preferred_location


class HttpResponseMovedPermanently(HttpResponse):
    status_code = 301
    status_text = 'MOVED PERMANENTLY'

    def __init__(self, redirect_to):
        super(HttpResponseMovedPermanently, self).__init__()
        self['Location'] = redirect_to


class HttpResponseFound(HttpResponse):
    status_code = 302
    status_text = 'FOUND'

    def __init__(self, redirect_to):
        super(HttpResponseFound, self).__init__()
        self['Location'] = redirect_to


class HttpResponseSeeOther(HttpResponse):
    status_code = 303
    status_text = 'SEE OTHER'

    def __init__(self, redirect_to):
        super(HttpResponseSeeOther, self).__init__()
        self['Location'] = redirect_to


class HttpResponseNotModified(HttpResponse):
    status_code = 304
    status_text = 'NOT MODIFIED'


class HttpResponseUseProxy(HttpResponse):
    status_code = 305
    status_text = 'USE PROXY'

    def __init__(self, redirect_to):
        super(HttpResponseUseProxy, self).__init__()
        self['Location'] = redirect_to


class HttpResponseTemporaryRedirect(HttpResponse):
    status_code = 307
    status_text = 'TEMPORARY REDIRECT'

    def __init__(self, redirect_to):
        super(HttpResponseTemporaryRedirect, self).__init__()
        self['Location'] = redirect_to
