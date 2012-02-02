# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2
from agiliza.net.http.response import HttpResponse


class HttpResponseOk(object):
    status_code = 200


class HttpResponseCreated(HttpResponse):
    status_code = 201


class HttpResponseAccepted(HttpResponse):
    status_code = 202


class HttpResponseNonAuthoritativeInformation(HttpResponse):
    status_code = 203


class HttpResponseNoContent(HttpResponse):
    status_code = 204


class HttpResponseResetContent(HttpResponse):
    status_code = 205


class HttpResponsePartialContent(HttpResponse):
    status_code = 206
