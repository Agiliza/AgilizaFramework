# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3
from agiliza.net.http.response import HttpResponse


class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300


class HttpResponsePermanentRedirect(HttpResponse):
    status_code = 301


class HttpResponseRedirect(HttpResponse):
    status_code = 302


class HttpResponseSeeOther(HttpResponse):
    status_code = 303


class HttpResponseNotModified(HttpResponse):
    status_code = 304


class HttpResponseUseProxy(HttpResponse):
    status_code = 305


class HttpResponseTemporaryRedirect(HttpResponse):
    status_code = 307
