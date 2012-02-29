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
# See http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3
from agiliza.http.response import HttpResponse


class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300
    status_text = 'MULTIPLE CHOICES'

    def __init__(self, preferred_location=None):
        super(HttpResponseMultipleChoices, self).__init__()
        if preferred_location:
            self['Location'] = preferred_location


class HttpResponseMovedPermanently(HttpResponse):
    status_code = 301
    status_text = 'MOVED PERMANENTLY'

    def __init__(self, redirect_to):
        super(HttpResponseMovedPermanently, self).__init__()
        self['Location'] = redirect_to


class HttpResponseFound(HttpResponse):
    status_code = 302
    status_text = 'FOUND'

    def __init__(self, redirect_to):
        super(HttpResponseFound, self).__init__()
        self['Location'] = redirect_to


class HttpResponseSeeOther(HttpResponse):
    status_code = 303
    status_text = 'SEE OTHER'

    def __init__(self, redirect_to):
        super(HttpResponseSeeOther, self).__init__()
        self['Location'] = redirect_to


class HttpResponseNotModified(HttpResponse):
    status_code = 304
    status_text = 'NOT MODIFIED'


class HttpResponseUseProxy(HttpResponse):
    status_code = 305
    status_text = 'USE PROXY'

    def __init__(self, redirect_to):
        super(HttpResponseUseProxy, self).__init__()
        self['Location'] = redirect_to


class HttpResponseTemporaryRedirect(HttpResponse):
    status_code = 307
    status_text = 'TEMPORARY REDIRECT'

    def __init__(self, redirect_to):
        super(HttpResponseTemporaryRedirect, self).__init__()
        self['Location'] = redirect_to
