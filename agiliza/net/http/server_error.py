"""
This file is part of Agiliza.

Agiliza is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Agiliza is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Agiliza.  If not, see <http://www.gnu.org/licenses/>.


Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
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
