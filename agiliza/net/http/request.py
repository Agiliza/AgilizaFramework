"""
See http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.5 and
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5.3

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

"""
import abc



class HttpRequest(metaclass=abc.ABCMeta):
    """A basic HTTP request."""
    @abc.abstractproperty
    def method(self): pass

    @abc.abstractproperty
    def path_info(self): pass

    @abc.abstractproperty
    def query_string(self): pass

    @abc.abstractproperty
    def script_name(self): pass

    @abc.abstractmethod
    def is_secure(self): pass

    def is_ajax(self):
        """Alias for :attr:`is_xhr`. "Ajax" is not the right term."""
        return self.is_xhr()

    def is_xhr(self):
        """
        True if the request was triggered by a XMLHttpRequest. This only
        works with JavaScript libraries that support the
        `X-Requested-With` header (most of the popular libraries do).
        """
        requested_with = self.META.get('HTTP_X_REQUESTED_WITH', '')
        return requested_with.lower() == 'xmlhttprequest'

    def get_host(self):
        if 'HTTP_HOST' in self.META:
            return self.META['HTTP_HOST']
        result = self.META['SERVER_NAME']
        if(self.META['wsgi.url_scheme'],
           self.META['SERVER_PORT']) not \
           in ((b'https', b'443'), (b'http', b'80')):
            result += b':' + self.META['SERVER_PORT']
        return result
