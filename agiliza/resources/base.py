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
from agiliza.core.net import http
from agiliza.core.net.http.exceptions import (MethodNotAllowedException,
    NotAcceptableException)
from agiliza.resources.interface import ResourceMetaclass


__all__ = ('Resource',)


class Resource(metaclass=ResourceMetaclass):
    def dispatch(self, request, *args, **kwargs):
        allow_list = self._mapper.allow_methods()
        if not request.method in allow_list:
            return http.HttpResponseMethodNotAllowed(allow_list)

        accept = sorted([ (q, t) for t, q in request.accept.items() ],
            reverse=True)
        accept_list = tuple(map(lambda x: x[1], accept))
        try:
            method = self._mapper.find(request.method, accept_list)
            response = method(self, request, *args, **kwargs) # TODO classmethod for methods?
        except MethodNotAllowedException:
            response = http.HttpResponseMethodNotAllowed(allow_list)
        except NotAcceptableException as exception:
            # TODO HTTP Content Negotiation
            response = http.HttpResponseNotAcceptable()

        # TODO warning if response.content_type is not in method.accept
        return response

    def get_filestorage(self):
        '''
            Debería buscar si la vista tiene asociado algún filestorage.
            En caso de no tenerlo, se debería buscar en la aplicación y
            si no, en el proyecto. <-- ¿Cómo localizar la aplicación?
        '''
