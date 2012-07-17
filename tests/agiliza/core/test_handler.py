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
from agiliza.core.handlers import Handler
from agiliza.core.handlers.exceptions import *
from agiliza.urls import url, include
from tests.mocks.config import *
from tests.mocks.controllers import *
from tests.mocks.middleware import *
from tests.mocks.request import *


class HandlerTest(unittest.TestCase):

    def setUp(self):
        self.config_module = ConfigModuleMock({
            'installed_apps': list(),
            'middleware_level0': list(),
            'middleware_level1': list(),
            'urls': UrlModuleMock(tuple()),
        })

    def test_must_load_from_config_module(self):
        handler = Handler(self.config_module)

        self.assertTrue(
            isinstance(handler.config, ConfigRunner),
            "Handler does not load from config module"
        )

    def test_must_load_from_environ(self):
        os.environ['AGILIZA_CONFIG'] = 'my_project.config'
        sys.modules.setdefault('my_project.config', self.config_module)
        handler = Handler()

        self.assertTrue(
            isinstance(handler.config, ConfigRunner),
            "Handler does not load from config module"
        )

        sys.modules.pop('my_project.config')

    def test_must_fail_without_config_info(self):
        with self.assertRaises(InvalidConfigModuleException,
            msg="Must be raise a InvalidConfigModuleException"):

            Handler()

    def test_must_raise_http_404_without_url_patterns(self):
        handler = Handler(self.config_module)

        request = HttpRequestMock()
        request.method = 'GET'

        with self.assertRaises(http.Http404,
            msg="Must be raise a Http404"):

            handler.dispatch(request)

    def test_must_raise_http_405_using_controller_without_get_method(self):
        self.config_module.urls = UrlModuleMock(
            (
                url('/exp1', 'tests.mocks.controllers.GetControllerMock'),
                url('/exp2', 'tests.mocks.controllers.PutControllerMock'),
            )
        )

        handler = Handler(self.config_module)

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp2'

        with self.assertRaises(http.Http405,
            msg="Must be raise a InvalidConfigModuleException"):

            handler.dispatch(request)

    def test_middleware_level0_must_add_mw_field_to_request_and_response(self):
        self.config_module.urls = UrlModuleMock(
            (
                url('/exp1', 'tests.mocks.controllers.GetControllerMock'),
            )
        )

        CompleteMiddlewareLevel0Mock.process_request = lambda self, request: \
            setattr(request, 'mw', True)

        self.config_module.middleware_level0.append(
            CompleteMiddlewareLevel0Mock
        )

        handler = Handler(self.config_module)

        request = HttpRequestMock()
        request.method = 'GET'
        request.path_info = '/exp1'
        request.accept['text/html'] = 1.0

        response = handler.dispatch(request)



if __name__ == '__main__':
    unittest.main()
