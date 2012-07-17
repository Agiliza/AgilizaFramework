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
from tests.mocks.utils import Singleton


class BadMiddlewareMock(Singleton):
    pass


class CompleteMiddlewareLevel0Mock(Singleton):
    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

class ProcessRequestMiddlewareLevel0Mock(Singleton):
    def process_request(self, request):
        pass

class ProcessResponseMiddlewareLevel0Mock(Singleton):
    def process_response(self, request, response):
        pass


class CompleteMiddlewareLevel1Mock(Singleton):
    def process_controller(self, request, controllerfunc, controllerargs,
        controllerkwargs):
        pass

    def process_render(self, request, response, render):
        pass

class ProcessControllerMiddlewareLevel1Mock(Singleton):
    def process_controller(self, request, controllerfunc, controllerargs,
        controllerkwargs):
        pass

class ProcessRenderMiddlewareLevel1Mock(Singleton):
    def process_render(self, request, response, render):
        pass
