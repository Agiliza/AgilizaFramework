# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5
from agiliza.net.http.response import HttpResponse


class HttpResponseInternalServerError(HttpResponse):
    status_code = 500


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501


class HttpResponseBadGateway(HttpResponse):
    status_code = 502


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503


class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504


class HttpResponseHTTPVersionNotSupported(HttpResponse):
    status_code = 505
