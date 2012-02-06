# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3
from agiliza.net.http.response import HttpResponse


class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300
    status_text = 'MULTIPLE CHOICES'


class HttpResponseMovedPermanently(HttpResponse):
    status_code = 301
    status_text = 'MOVED PERMANENTLY'


class HttpResponseFound(HttpResponse):
    status_code = 302
    status_text = 'FOUND'


class HttpResponseSeeOther(HttpResponse):
    status_code = 303
    status_text = 'SEE OTHER'


class HttpResponseNotModified(HttpResponse):
    status_code = 304
    status_text = 'NOT MODIFIED'


class HttpResponseUseProxy(HttpResponse):
    status_code = 305
    status_text = 'USE PROXY'


class HttpResponseTemporaryRedirect(HttpResponse):
    status_code = 307
    status_text = 'TEMPORARY REDIRECT'
