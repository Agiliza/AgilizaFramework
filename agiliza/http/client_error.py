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
# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4
from agiliza.http.exceptions import HttpResponseException
from agiliza.http.response import HttpResponse


class HttpResponseBadRequest(HttpResponse, HttpResponseException):
    status_code = 400
    status_text = 'BAD REQUEST'


class HttpResponseUnauthorized(HttpResponse, HttpResponseException):
    status_code = 401
    status_text = 'UNAUTHORIZED'


class HttpResponsePaymentRequired(HttpResponse, HttpResponseException):
    status_code = 402
    status_text = 'PAYMENT REQUIRED'


class HttpResponseForbidden(HttpResponse, HttpResponseException):
    status_code = 403
    status_text = 'FORBIDDEN'


class HttpResponseNotFound(HttpResponse, HttpResponseException):
    status_code = 404
    status_text = 'NOT FOUND'


class HttpResponseMethodNotAllowed(HttpResponse, HttpResponseException):
    status_code = 405
    status_text = 'METHOD NOT ALLOWED'

    def __init__(self, permitted_methods):
        super(HttpResponseMethodNotAllowed, self).__init__()
        self['Allow'] = ', '.join(permitted_methods)


class HttpResponseNotAcceptable(HttpResponse, HttpResponseException):
    status_code = 406
    status_text = 'NOT ACCEPTABLE'


class HttpResponseProxyAuthenticationRequired(HttpResponse, HttpResponseException):
    status_code = 407
    status_text = 'PROXY AUTHENTICATION REQUIRED'


class HttpResponseRequestTimeout(HttpResponse, HttpResponseException):
    status_code = 408
    status_text = 'REQUEST TIMEOUT'


class HttpResponseConflict(HttpResponse, HttpResponseException):
    status_code = 409
    status_text = 'CONFLICT'


class HttpResponseGone(HttpResponse, HttpResponseException):
    status_code = 410
    status_text = 'GONE'


class HttpResponseLengthRequired(HttpResponse, HttpResponseException):
    status_code = 411
    status_text = 'LENGTH REQUIRED'


class HttpResponsePreconditionFailed(HttpResponse, HttpResponseException):
    status_code = 412
    status_text = 'PRECONDITION FAILED'


class HttpResponseRequestEntityTooLarge(HttpResponse, HttpResponseException):
    status_code = 413
    status_text = 'REQUEST ENTITY TOO LARGE'


class HttpResponseRequestURITooLong(HttpResponse, HttpResponseException):
    status_code = 414
    status_text = 'REQUEST-URI TOO LONG'


class HttpResponseUnsupportedMediaType(HttpResponse, HttpResponseException):
    status_code = 415
    status_text = 'UNSUPPORTED MEDIA TYPE'


class HttpResponseRequestedRangeNotSatisfiable(HttpResponse, HttpResponseException):
    status_code = 416
    status_text = 'REQUESTED RANGE NOT SATISFIABLE'


class HttpResponseExpectationFailed(HttpResponse, HttpResponseException):
    status_code = 417
    status_text = 'EXPECTATION FAILED'
