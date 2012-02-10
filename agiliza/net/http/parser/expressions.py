import re

"""
    See http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.1

    Accept         = "Accept" ":"
                    #( media-range [ accept-params ] )

    media-range    = ( "*/*"
                    | ( type "/" "*" )
                    | ( type "/" subtype )
                    ) *( ";" parameter )
    accept-params  = ";" "q" "=" qvalue *( accept-extension )
    accept-extension = ";" token [ "=" ( token | quoted-string ) ]
"""
ACCEPT_HEADER = re.compile(r'^Accept[ ]*:[ ]*.+') #  TODO refinar la expresion
ACCEPT_MEDIA_RANGE = re.compile(r'(?P<type>\*|[\w-]+)/(?P<subtype>\*|[\w-]+)[ ]*([ ]*;[ ]*q[ ]*=[ ]*(?P<q>\d.\d\d?))?') #  TODO dar soporte a otros parametros (como level)

