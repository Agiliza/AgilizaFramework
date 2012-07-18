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
import os
import sys
import unittest

from agiliza import http
from agiliza.core.config import ConfigRunner
from agiliza.core.handlers.base import Handler
from agiliza.core.handlers.exceptions import *
from agiliza.config.urls import url, include
from tests.mocks.config import *
from tests.mocks.controllers import *
from tests.mocks.middleware import *
from tests.mocks.request import *


class HandlerTest(unittest.TestCase):

    def setUp(self):
        self.config_module = ConfigModuleMock()

        sys.modules.setdefault('my_config_module', self.config_module)
        sys.modules.setdefault('my_config_module.urls', self.config_module.urls)
        os.environ['AGILIZA_CONFIG'] = 'my_config_module'

        ConfigRunner.invalidateInstance()

    def tearDown(self):
        del os.environ['AGILIZA_CONFIG']
        sys.modules.pop('my_config_module')
        sys.modules.pop('my_config_module.urls')

    def test_must_load_from_config_module(self):
        handler = Handler()

        self.assertTrue(
            isinstance(handler.config, ConfigRunner),
            "Handler does not load from config module"
        )

    def test_must_raise_http_404_without_url_patterns(self):
        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'

        with self.assertRaises(http.Http404,
            msg="Must be raise a Http404"):

            handler.dispatch(request)

    def test_must_raise_http_405_using_controller_without_get_method(self):
        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp1',
                    'tests.mocks.controllers.GetControllerMock',
                    'exp1'
                ),
                url(
                    '/exp2',
                    'tests.mocks.controllers.PutControllerMock',
                    'exp2'
                ),
            )
        )

        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp2'

        with self.assertRaises(http.Http405,
            msg="Must be raise a InvalidConfigModuleException"):

            handler.dispatch(request)

    def test_must_not_launch_exception_with_200_response(self):
        GetControllerMock.get = lambda self, *args, **kwargs: \
            http.Http200()

        self.config_module.urls.url_patterns = (
            (
                url('/exp1', GetControllerMock, 'exp1'),
            )
        )

        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp1'
        request.accept['text/html'] = 1.0

        response = handler.dispatch(request)

    def test_must_not_launch_exception_with_context_data_response(self):
        GetControllerMock.get = lambda self, *args, **kwargs: \
            { 'title': 'Just now' }

        self.config_module.urls.url_patterns = (
            (
                url('/exp1', GetControllerMock, 'exp1'),
            )
        )

        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp1'
        request.accept['text/html'] = 1.0

        with self.assertRaises(http.Http415,
            msg="Must be raise a Http415"):
            handler.dispatch(request)

    def test_middleware_level0_must_add_mw_field_to_request_and_response(self):
        GetControllerMock.get = lambda self, *args, **kwargs: \
            http.Http200()

        self.config_module.urls.url_patterns = (
            (
                url('/exp1', GetControllerMock, 'exp1'),
            )
        )

        CompleteMiddlewareLevel0Mock.process_request = lambda self, request: \
            setattr(request, 'mw', True)

        CompleteMiddlewareLevel0Mock.process_response = \
            lambda self, request, response: \
                setattr(response, 'mw', True)

        self.config_module.middleware_level0.append(
            CompleteMiddlewareLevel0Mock
        )

        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp1'
        request.accept['text/html'] = 1.0

        response = handler.dispatch(request)

        self.assertTrue(
            getattr(request, 'mw', False) and getattr(response, 'mw', False),
            "Middleware level0 does not add 'mw' field to request and response"
        )

    def test_must_render_a_response(self):
        self.config_module.templates['directory'] = \
            os.path.join(os.getcwd(), 'tests/data/templates/')

        GetControllerMock.get = lambda self, *args, **kwargs: \
            { 'title': 'Just now' }

        self.config_module.urls.url_patterns = (
            (
                url('/home', GetControllerMock, 'home'),
            )
        )

        handler = Handler()

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/home'
        request.accept['text/html'] = 1.0

        response = handler.dispatch(request)

        self.assertTrue(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()
