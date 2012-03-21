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
from agiliza.handlers.context import ContextManager


class Handler(object):
    def get_response(self, request):
        """Returns an Response object for the given Request."""
        # Locate the appropiate resource
        resource = None # TODO: Locate
        params = {} # TODO: URL params
        with ContextManager(request, params) as context:
            context_data = context.get_data()
            template_context, templates = resource.dispatch(**context)
