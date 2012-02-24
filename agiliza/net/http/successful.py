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
