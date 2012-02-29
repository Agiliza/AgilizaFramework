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
from agiliza.http import HttpResponseOk


class Handler(object):
    def __init__(self):
        try:
            self.load_middleware()
        except:
            # Unload whatever middleware we got
            self._request_middleware = None
            raise

    def load_middleware(self):
        """Populate middleware lists."""

    def get_response(self, request):
        """Returns an Response object for the given Request."""
