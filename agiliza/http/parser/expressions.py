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
ACCEPT_MEDIA_RANGE = re.compile(r'(?P<type>\*|[\w-]+)/(?P<subtype>\*|[\w-]+)[ ]*([ ]*;[ ]*q[ ]*=[ ]*(?P<q>\d.\d\d?))?') #  TODO dar soporte a otros parametros (como level)

