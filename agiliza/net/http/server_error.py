# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5
from agiliza.net.http.response import HttpResponse


class HttpResponseInternalServerError(HttpResponse):
    status_code = 500
    status_text = 'INTERNAL SERVER ERROR'


class HttpResponseNotImplemented(HttpResponse):
    status_code = 501
    status_text = 'NOT IMPLEMENTED'


class HttpResponseBadGateway(HttpResponse):
    status_code = 502
    status_text = 'BAD GATEWAY'


class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503
    status_text = 'SERVICE UNAVAILABLE'


class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504
    status_text = 'GATEWAY TIMEOUT'


class HttpResponseHTTPVersionNotSupported(HttpResponse):
    status_code = 505
    status_text = 'HTTP VERSION NOT SUPPORTED'
