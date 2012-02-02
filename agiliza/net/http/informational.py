# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1
from agiliza.net.http.response import HttpResponse


class HttpResponseContinue(HttpResponse):
    status_code = 100


class HttpResponseSwitchingProtocols(HttpResponse):
    status_code = 101
