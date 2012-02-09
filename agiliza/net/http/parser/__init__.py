from agiliza.net.http.exceptions import AcceptHeaderException
from agiliza.net.http.parser import expressions


def parse_accept_header(accept_header):
    if not expressions.ACCEPT_HEADER.match(accept_header):
        raise AcceptHeaderException("It isn't an accept header")

    media_range = {}
    for it in expressions.ACCEPT_MEDIA_RANGE.finditer(accept_header):
        media_type = it.group('type') or '*'
        media_subtype = it.group('subtype') or '*'
        try:
            media_q = float(it.group('q') or 1.0)
        except ValueError:
            raise AcceptHeaderException()

        key = '%s/%s' % (media_type, media_subtype)
        media_range[key] = float(media_q or 1.0)

    if len(media_range) == 0:
        raise AcceptHeaderException("Accept header is empty")

    return media_range
