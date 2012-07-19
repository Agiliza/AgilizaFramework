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



See http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.5,
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.3 and
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec7.html#sec7.1

4.5 General Header Fields

    Cache-Control            ; Section 14.9
    Connection               ; Section 14.10
    Date                     ; Section 14.18
    Pragma                   ; Section 14.32
    Trailer                  ; Section 14.40
    Transfer-Encoding        ; Section 14.41
    Upgrade                  ; Section 14.42
    Via                      ; Section 14.45
    Warning                  ; Section 14.46

5.3 Request Header Fields

    Accept                   ; Section 14.1
    Accept-Charset           ; Section 14.2
    Accept-Encoding          ; Section 14.3
    Accept-Language          ; Section 14.4
    Authorization            ; Section 14.8
    Expect                   ; Section 14.20
    From                     ; Section 14.22
    Host                     ; Section 14.23
    If-Match                 ; Section 14.24

    If-Modified-Since        ; Section 14.25
    If-None-Match            ; Section 14.26
    If-Range                 ; Section 14.27
    If-Unmodified-Since      ; Section 14.28
    Max-Forwards             ; Section 14.31
    Proxy-Authorization      ; Section 14.34
    Range                    ; Section 14.35
    Referer                  ; Section 14.36
    TE                       ; Section 14.39
    User-Agent               ; Section 14.43

7.1 Entity Header Fields

    Allow                    ; Section 14.7
    Content-Encoding         ; Section 14.11
    Content-Language         ; Section 14.12
    Content-Length           ; Section 14.13
    Content-Location         ; Section 14.14
    Content-MD5              ; Section 14.15
    Content-Range            ; Section 14.16
    Content-Type             ; Section 14.17
    Expires                  ; Section 14.21
    Last-Modified            ; Section 14.29

"""
import cgi
import urllib
from http.cookies import SimpleCookie

from agiliza.core.utils.decorators import cached_property
from agiliza.http.exceptions import HttpNegativeContentLengthException
from agiliza.http.parser import parse_accept_header


class HttpRequest(object):
    """A basic HTTP request."""
    VERSION = '1.1'

    def __init__(self, environ):
        """Wrap a WSGI environ dictionary."""
        self.meta = environ.copy()
        self.query_string = self.meta.get('QUERY_STRING', '')
        # This must be done to avoid a bug in cgi.FieldStorage
        self.meta.setdefault('QUERY_STRING', '')

        self.method = self.meta['REQUEST_METHOD'].upper()

        self.path_info = '/' + self.meta.get('PATH_INFO', '')\
            .lstrip('/')
        self.script_name = self.meta.get('SCRIPT_NAME', '')

        content_type = self.meta.get('CONTENT_TYPE', '')
        self.content_type, pdict = cgi.parse_header(content_type)
        self.charset = pdict.get('charset', 'utf-8') # TODO settings
        self.boundary = pdict.get('boundary', '')
        try:
            self.content_length = int(
                self.meta.get('CONTENT_LENGTH', 0))
        except ValueError:
            self.content_length = 0

        if self.content_length < 0:
            raise HttpNegativeContentLengthException()

        accept_hdr = self.meta.get('HTTP_ACCEPT', 'text/html') # TODO settings
        self.accept = parse_accept_header(accept_hdr)
        self._stream = self.meta['wsgi.input']

        self.cookies = SimpleCookie()
        self.cookies.load(self.meta.get('HTTP_COOKIE', ''))

    def is_secure(self):
        return 'wsgi.url_scheme' in self.meta \
            and self.meta['wsgi.url_scheme'] == 'https'

    def is_ajax(self):
        """Alias for :attr:`is_xhr`. "Ajax" is not the right term."""
        return self.is_xhr()

    def is_xhr(self):
        """
        True if the request was triggered by a XMLHttpRequest. This only
        works with JavaScript libraries that support the
        `X-Requested-With` header (most of the popular libraries do).
        """
        requested_with = self.meta.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'

    @cached_property
    def get_host(self):
        if 'HTTP_HOST' in self.meta:
            return self.meta['HTTP_HOST']

        host = self.meta['SERVER_NAME']

        if self.meta['wsgi.url_scheme'] == 'https':
            if self.meta['SERVER_PORT'] != '443':
               host += ':' + self.meta['SERVER_PORT']
        else:
            if self.meta['SERVER_PORT'] != '80':
               host += ':' + self.meta['SERVER_PORT']

        return host

    @cached_property
    def get_full_path(self):
        from urllib.parse import quote
        url = self.meta['wsgi.url_scheme'] + '://'
        url += self.get_host()
        url += quote(self.script_name)
        url += quote(self.path_info)
        if self.query_string:
            url += '?' + self.query_string

        return url

    @cached_property
    def query(self):
        return urllib.parse.parse_qs(self.query_string, keep_blank_values=True)

    @cached_property
    def data(self):

        return cgi.FieldStorage(
            fp=self._stream,
            environ=self.meta,
            keep_blank_values=True
        )

    def __str__(self):
        return 'HttpRequest <%s %s HTTP/%s>' % (
            self.method, self.path_info, self.VERSION
        )
