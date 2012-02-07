# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2
from agiliza.net.http.response import HttpResponse


class HttpResponseOk(HttpResponse):
    status_code = 200
    status_text = 'OK'


class HttpResponseCreated(HttpResponse):
    status_code = 201
    status_text = 'CREATED'


class HttpResponseAccepted(HttpResponse):
    status_code = 202
    status_text = 'ACCEPTED'


class HttpResponseNonAuthoritativeInformation(HttpResponse):
    status_code = 203
    status_text = 'NON-AUTHORITATIVE INFORMATION'


class HttpResponseNoContent(HttpResponse):
    status_code = 204
    status_text = 'NO CONTENT'


class HttpResponseResetContent(HttpResponse):
    status_code = 205
    status_text = 'RESET CONTENT'


class HttpResponsePartialContent(HttpResponse):
    status_code = 206
    status_text = 'PARTIAL CONTENT'
