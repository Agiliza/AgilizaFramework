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
        # Check if media type is in ``media_range``. In this case, get
        # the highest value for ``media_q``
        if media_range.has_key(key):
            prev_key, prev_q = media_range[key]
            if prev_q > media_q:
                media_q = prev_q
        # Store the quality for this media type
        media_range[key] = media_q

    if len(media_range) == 0:
        raise AcceptHeaderException("Accept header is empty")

    return media_range
