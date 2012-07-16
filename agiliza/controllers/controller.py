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
from agiliza import http
from agiliza.core.utils.decorators import cached_property


class Controller(object):

    @cached_property
    def permitted_methods(self):
        methods = tuple([
            method_name
            for method_name in http.HTTP_METHODS
            if getattr(self, method_name.lower(), None)
        ])

        return methods

    def dispatch(self, request, params, settings, session, cookies):
        method_name = request.method.lower()

        try:
            method = getattr(self, method_name)
        except AttributeError:
            raise http.HttpResponseMethodNotAllowed(self.permitted_methods)

        return method(request, params, settings, session, cookies)
