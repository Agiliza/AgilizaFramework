"""
See http://www.w3.org/TR/html401/interact/forms.html#h-17.13 and
http://www.ietf.org/rfc/rfc2388.txt
"""
import cgi
import urllib

from agiliza.net.http.exceptions import FormDataProcessingException


def parse_form_data(meta, stream):
    ctype, pdict = cgi.parse_header(meta.get('CONTENT_TYPE', ''))
    data = {}
    if ctype == 'application/x-www-form-urlencoded':
        method = meta['REQUEST_METHOD']
        if method == 'GET':
            query_string = meta.get('QUERY_STRING','')
        else:
            length = int(meta.get('CONTENT_LENGTH', '0'))
            query_string = stream.read(length)
        data = urllib.parse.parse_qs(query_string, keep_blank_values=True)
    elif ctype == 'multipart/form-data':
        data = cgi.parse_multipart(stream, pdict)

    return data

