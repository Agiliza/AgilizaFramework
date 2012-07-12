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
from contextlib import ContextDecorator


class ContextManager(ContextDecorator):
    def __init__(self, request, params):
        self.request = request
        self.params = params
        self._context = None

    def __enter__(self):
        # Apply middleware
        # Generate the context (session, user, config, ...)
        request = self.request
        params = self.params
        session = None
        config = None

        self._context = {
            'request': request,
            'params': params,
            'session': session,
            'config': config,
        }

        return self

    def __exit__(self, *exc):
        print('Finishing')
        print(exc)
        # Apply middleware
        # Update the context
        return True

    def get_data(self):
        return self._context
