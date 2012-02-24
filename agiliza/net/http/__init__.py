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
from agiliza.net.http.client_error import (HttpResponseBadRequest,
    HttpResponseUnauthorized, HttpResponsePaymentRequired,
    HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseMethodNotAllowed, HttpResponseNotAcceptable,
    HttpResponseProxyAuthenticationRequired, HttpResponseRequestTimeout,
    HttpResponseConflict, HttpResponseGone, HttpResponseLengthRequired,
    HttpResponsePreconditionFailed, HttpResponseRequestEntityTooLarge,
    HttpResponseRequestURITooLong, HttpResponseUnsupportedMediaType,
    HttpResponseRequestedRangeNotSatisfiable,
    HttpResponseExpectationFailed)
from agiliza.net.http.informational import (HttpResponseContinue,
    HttpResponseSwitchingProtocols)
from agiliza.net.http.redirection import (HttpResponseMultipleChoices,
    HttpResponseMovedPermanently, HttpResponseFound,
    HttpResponseSeeOther, HttpResponseNotModified, HttpResponseUseProxy,
    HttpResponseTemporaryRedirect)
from agiliza.net.http.request import HttpRequest
from agiliza.net.http.server_error import (
    HttpResponseInternalServerError, HttpResponseNotImplemented,
    HttpResponseBadGateway, HttpResponseServiceUnavailable,
    HttpResponseGatewayTimeout, HttpResponseHTTPVersionNotSupported)
from agiliza.net.http.successful import (HttpResponseOk,
    HttpResponseCreated, HttpResponseAccepted,
    HttpResponseNonAuthoritativeInformation, HttpResponseNoContent,
    HttpResponseResetContent, HttpResponsePartialContent)

HTTP_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS',
    'TRACE', 'CONNECT')
