"""
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
class HttpRequest(object):
    """A basic HTTP request."""

    def __init__(self, environ):
        """Wrap a WSGI environ dictionary."""
        self.meta = environ
        self.method = environ['REQUEST_METHOD'].upper()
        self.path_info = '/' + self.meta.get('PATH_INFO','').lstrip('/')
        self.query_string = '/' + self.meta.get('QUERY_STRING','')
        self.script_name = self.meta.get('SCRIPT_NAME', '')
        # Cached values
        self._host = None

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

    def get_host(self):
        if self._host:
            return self._host

        if 'HTTP_HOST' in self.meta:
            return self.meta['HTTP_HOST']
        host = self.meta['SERVER_NAME']

        if self.meta['wsgi.url_scheme'] == 'https':
            if self.meta['SERVER_PORT'] != '443':
               host += ':' + self.meta['SERVER_PORT']
        else:
            if self.meta['SERVER_PORT'] != '80':
               host += ':' + self.meta['SERVER_PORT']

        self._host = host
        return self._host

    def get_full_path(self):
        from urllib import quote
        url = self.meta['wsgi.url_scheme'] + '://'
        url += self.get_host()
        url += quote(self.meta.get('SCRIPT_NAME', ''))
        url += quote(self.meta.get('PATH_INFO', ''))
        if self.meta.get('QUERY_STRING'):
            url += '?' + self.meta['QUERY_STRING']

        return url
