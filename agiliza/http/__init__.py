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
from agiliza.http.client_error import (HttpResponseBadRequest,
    HttpResponseUnauthorized, HttpResponsePaymentRequired,
    HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseMethodNotAllowed, HttpResponseNotAcceptable,
    HttpResponseProxyAuthenticationRequired, HttpResponseRequestTimeout,
    HttpResponseConflict, HttpResponseGone, HttpResponseLengthRequired,
    HttpResponsePreconditionFailed, HttpResponseRequestEntityTooLarge,
    HttpResponseRequestURITooLong, HttpResponseUnsupportedMediaType,
    HttpResponseRequestedRangeNotSatisfiable,
    HttpResponseExpectationFailed)
from agiliza.http.exceptions import (HttpParserException, HttpResponseException)
from agiliza.http.informational import (HttpResponseContinue,
    HttpResponseSwitchingProtocols)
from agiliza.http.redirection import (HttpResponseMultipleChoices,
    HttpResponseMovedPermanently, HttpResponseFound,
    HttpResponseSeeOther, HttpResponseNotModified, HttpResponseUseProxy,
    HttpResponseTemporaryRedirect)
from agiliza.http.request import HttpRequest
from agiliza.http.server_error import (
    HttpResponseInternalServerError, HttpResponseNotImplemented,
    HttpResponseBadGateway, HttpResponseServiceUnavailable,
    HttpResponseGatewayTimeout, HttpResponseHTTPVersionNotSupported)
from agiliza.http.successful import (HttpResponseOk,
    HttpResponseCreated, HttpResponseAccepted,
    HttpResponseNonAuthoritativeInformation, HttpResponseNoContent,
    HttpResponseResetContent, HttpResponsePartialContent)

HTTP_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS',
    'TRACE', 'CONNECT')


## Shortcuts

# Informational
Http100 = HttpResponseContinue
Http101 = HttpResponseSwitchingProtocols
# Successful
Http200 = HttpResponseOk
Http201 = HttpResponseCreated
Http202 = HttpResponseAccepted
Http203 = HttpResponseNonAuthoritativeInformation
Http204 = HttpResponseNoContent
Http205 = HttpResponseResetContent
Http206 = HttpResponsePartialContent
# Redirection
Http300 = HttpResponseMultipleChoices
Http301 = HttpResponseMovedPermanently
Http302 = HttpResponseFound
Http303 = HttpResponseSeeOther
Http304 = HttpResponseNotModified
Http305 = HttpResponseUseProxy
Http307 = HttpResponseTemporaryRedirect
# Client error
Http400 = HttpResponseBadRequest
Http401 = HttpResponseUnauthorized
Http402 = HttpResponsePaymentRequired
Http403 = HttpResponseForbidden
Http404 = HttpResponseNotFound
Http405 = HttpResponseMethodNotAllowed
Http406 = HttpResponseNotAcceptable
Http407 = HttpResponseProxyAuthenticationRequired
Http408 = HttpResponseRequestTimeout
Http409 = HttpResponseConflict
Http410 = HttpResponseGone
Http411 = HttpResponseLengthRequired
Http412 = HttpResponsePreconditionFailed
Http413 = HttpResponseRequestEntityTooLarge
Http414 = HttpResponseRequestURITooLong
Http415 = HttpResponseUnsupportedMediaType
Http416 = HttpResponseRequestedRangeNotSatisfiable
Http417 = HttpResponseExpectationFailed
# Server error
Http500 = HttpResponseInternalServerError
Http501 = HttpResponseNotImplemented
Http502 = HttpResponseBadGateway
Http503 = HttpResponseServiceUnavailable
Http504 = HttpResponseGatewayTimeout
Http505 = HttpResponseHTTPVersionNotSupported

