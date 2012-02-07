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
    @abc.abstractmethod
    def is_secure(self):
        pass
