"""
See http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.5,
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6.2 and
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

6.2 Response Header Fields

    Accept-Ranges           ; Section 14.5
    Age                     ; Section 14.6
    ETag                    ; Section 14.19
    Location                ; Section 14.30
    Proxy-Authenticate      ; Section 14.33

    Retry-After             ; Section 14.37
    Server                  ; Section 14.38
    Vary                    ; Section 14.44
    WWW-Authenticate        ; Section 14.47

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
import abc
import collections
from http.cookies import SimpleCookie

from agiliza.core.datastructures import MultiValueDict


class HttpResponse(metaclass=abc.ABCMeta):
    """
    A basic HTTP response, with content and dictionary-accessed headers.
    """
    @abc.abstractproperty
    def status_code(self):
        pass

    @abc.abstractproperty
    def status_text(self):
        pass

    def __init__(self, content='', content_type=None):
        # _headers is a mapping of the lower-case name to the original
        # case of the header (required for working with legacy systems)
        # and the header value.
        self._headers = {}
        self._charset = 'utf-8'  # TODO settings
        default_content_type = 'text/html'  # TODO settings
        if not content_type:
            content_type = "%s; charset=%s" % (default_content_type,
                self._charset)
        if isinstance(content, collections.Iterable) and \
            not isinstance(content, str):
            self._container = content
            self._is_string = False
        else:
            self._container = [content]
            self._is_string = True
        self.cookies = SimpleCookie()

        self['Content-Type'] = content_type
        self._content = content

    @property
    def status(self):
        return '%s %s' % (self.status_code, self.status_text)

    @property
    def headers(self):
        response_headers = [
            (key, value) for key, value in self._headers.values()
        ]
        return response_headers

    @property
    def content(self):
        return [ self._content.encode(self._charset) ]

    def __setitem__(self, header, value):
        self._headers[header.lower()] = (header, value)

    def __delitem__(self, header):
        try:
            del self._headers[header.lower()]
        except KeyError:
            pass

    def __getitem__(self, header):
        return self._headers[header.lower()][1]
