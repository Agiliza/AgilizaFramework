# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4
from agiliza.net.http.response import HttpResponse


class HttpResponseBadRequest(HttpResponse):
    status_code = 400


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class HttpResponsePaymentRequired(HttpResponse):
    status_code = 402


class HttpResponseForbidden(HttpResponse):
    status_code = 403


class HttpResponseNotFound(HttpResponse):
    status_code = 404


class HttpResponseNotAllowed(HttpResponse):
    status_code = 405


class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406


class HttpResponseProxyAuthenticationRequired(HttpResponse):
    status_code = 407


class HttpResponseRequestTimeout(HttpResponse):
    status_code = 408


class HttpResponseConflict(HttpResponse):
    status_code = 409


class HttpResponseGone(HttpResponse):
    status_code = 410


class HttpResponseLengthRequired(HttpResponse):
    status_code = 411


class HttpResponsePreconditionFailed(HttpResponse):
    status_code = 412


class HttpResponseRequestEntityTooLarge(HttpResponse):
    status_code = 413


class HttpResponseRequestURITooLong(HttpResponse):
    status_code = 414


class HttpResponseUnsupportedMediaType(HttpResponse):
    status_code = 415


class HttpResponseRequestedRangeNotSatisfiable(HttpResponse):
    status_code = 416


class HttpResponseExpectationFailed(HttpResponse):
    status_code = 417
