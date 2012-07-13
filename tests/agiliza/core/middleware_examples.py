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
class MiddlewareBadExample(object):
    pass


class MiddlewareLevel0Example1(object):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

class MiddlewareLevel0Example2(object):
    def process_request(self, request):
        pass


class MiddlewareLevel0Example3(object):
    def process_response(self, request, response):
        pass

class MiddlewareLevel1Example1(object):
    def process_controller(self, request, controllerfunc, controllerargs,
        controllerkwargs):
        pass

    def process_template(self, request, response, template):
        pass

class MiddlewareLevel1Example2(object):
    def process_controller(self, request, controllerfunc, controllerargs,
        controllerkwargs):
        pass

class MiddlewareLevel1Example3(object):
    def process_template(self, request, response, template):
        pass
