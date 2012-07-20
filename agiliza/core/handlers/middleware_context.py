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
Copyright (c) 2012 Alvaro Hurtado <alvarohurtado84@gmail.com>
"""
from agiliza.core.config import ConfigRunner
from agiliza.http import HttpResponseException


class MiddlewareLevel0Context(object):
    def __init__(self, request):
        self.config = ConfigRunner()
        self.request = request

    def __enter__(self):
        for middleware in self.config.middleware_level0:
            if hasattr(middleware, 'process_request'):
                middleware.process_request(self.request)
        return self

    def __exit__(self, type, value, traceback):
        if isinstance(value, HttpResponseException):
            self.response = value

        for middleware in self.config.middleware_level0:
            if hasattr(middleware, 'process_response'):
                middleware.process_response(self.request, self.response)

    def set_response(self, response):
        self.response = response

class MiddlewareLevel1Context(object):
    def __init__(self, controller, request, params):
        self.config = ConfigRunner()
        self.request = request
        self.controller = controller
        self.params = params

    def __enter__(self):
        for middleware in self.config.middleware_level1:
            if hasattr(middleware, 'process_controller'):
                middleware.process_controller(
                    self.controller, self.request, self.params
                )
        return self

    def __exit__(self, type, value, traceback):
        if isinstance(value, HttpResponseException):
            self.response = value

        for middleware in self.config.middleware_level1:
            if hasattr(middleware, 'process_controller_response'):
                middleware.process_controller_response(
                    self.controller, self.request, self.response
                )

    def set_response(self, response):
        self.response = response
