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
import importlib
import unittest
import os
import re
import sys

from agiliza.core.config import ConfigRunner
from agiliza.core.config.exceptions import *
from agiliza.config.urls import url, include
from tests.mocks.config import *
from tests.mocks.controllers import *
from tests.mocks.middleware import *


class ConfigRunnerTest(unittest.TestCase):

    def setUp(self):
        self.config_module = ConfigModuleMock()

        sys.modules.setdefault('my_config_module', self.config_module)
        sys.modules.setdefault('my_config_module.urls', self.config_module.urls)
        os.environ['AGILIZA_CONFIG'] = 'my_config_module'

        ConfigRunner.invalidateInstance()

    def tearDown(self):
        try:
            sys.modules.pop('my_config_module')
        except KeyError:
            pass

        try:
            sys.modules.pop('my_config_module.urls')
        except KeyError:
            pass


    def test_config_must_not_load_a_config_module(self):
        os.environ['AGILIZA_CONFIG'] = 'invalid_config_module'
        with self.assertRaises(ConfigModuleImportException,
            msg="Must be raise a ConfigModuleImportException"):

            ConfigRunner()

    def test_config_must_not_load_without_environ_variable(self):
        del os.environ['AGILIZA_CONFIG']
        with self.assertRaises(ConfigModuleImportException,
            msg="Must be raise a ConfigModuleImportException"):

            ConfigRunner()

    def test_config_must_load_simplest_configuration(self):
        del self.config_module.installed_apps
        del self.config_module.settings
        del self.config_module.middleware_level0
        del self.config_module.middleware_level1
        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (),
            "ConfigRunner does not load installed_apps"
        )

    def test_config_must_raise_exception_without_url_patterns(self):
        del self.config_module.urls.url_patterns

        with self.assertRaises(ConfigModuleImportException,
            msg="Must be raise a ConfigModuleImportException"):

            ConfigRunner()

    def test_config_must_raise_exception_without_urls_submodule(self):
        sys.modules.pop('my_config_module.urls')

        with self.assertRaises(ConfigModuleImportException,
            msg="Must be raise a ConfigModuleImportException"):

            ConfigRunner()

    def test_config_must_not_load_an_invalid_render(self):
        self.config_module.templates['render'] = 'invalid.Render'

        with self.assertRaises(InvalidRenderException,
            msg="Must be raise a InvalidRenderException"):

            ConfigRunner()

    def test_config_must_not_load_a_not_callable_render(self):
        self.config_module.templates['render'] = 'notcallable.Render'
        notcallable = types.ModuleType('notcallable')
        notcallable.Render = 'A string is not callable'
        sys.modules.setdefault('notcallable', notcallable)

        with self.assertRaises(InvalidRenderException,
            msg="Must be raise a InvalidRenderException"):

            ConfigRunner()

        sys.modules.pop('notcallable')

    def test_config_must_load_template_directory(self):
        self.config_module.templates['directory'] = '/'
        config = ConfigRunner()

        self.assertEqual(
            config.templates['directory'], '/',
            "ConfigRunner does not load template directory"
        )

    def test_config_must_raise_exception_with_template_directory(self):
        self.config_module.templates['directory'] = '/path/to/project/'

        with self.assertRaises(TemplatePathException,
            msg="Must be raise a TemplatePathException"):

            ConfigRunner()

    def test_config_must_load_an_app_name(self):
        app = ApplicationModuleMock('test_app')
        sys.modules.setdefault('test_app', app)
        self.config_module.installed_apps.append('test_app')

        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (app,),
            "ConfigRunner does not load installed_apps"
        )

        sys.modules.pop('test_app')

    def test_config_must_load_an_app_without_config(self):
        app = ApplicationModuleMock('test_app')
        del app.config

        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (app,),
            "ConfigRunner does not load installed_apps"
        )

    def test_config_must_load_an_app_without_settings(self):
        app = ApplicationModuleMock('test_app')
        del app.config.settings

        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (app,),
            "ConfigRunner does not load installed_apps"
        )

    def test_config_must_load_a_module(self):
        app = ApplicationModuleMock()
        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (app,),
            "ConfigRunner does not load installed_apps"
        )

    def test_must_not_load_a_list_as_an_app(self):
        self.config_module.installed_apps.append(['agiliza.core', ])

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner()

    def test_must_raise_invalid_application_exception(self):
        self.config_module.installed_apps.append('invalid.module.test')

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner()

    def test_config_must_load_a_empty_application_list(self):
        config = ConfigRunner()

        self.assertEqual(
            config.installed_apps, (),
            "ConfigRunner does not load a empty list"
        )

    def test_config_must_raise_invalid_middleware_exception_level0(self):
        self.config_module.middleware_level0.append('invalid.middleware.test')

        with self.assertRaises(InvalidMiddlewareException,
            msg="Must be raise a InvalidMiddlewareException"):

            ConfigRunner()

    def test_config_must_load_a_empty_list_level0(self):
        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level0, (),
            "ConfigRunner does not load a empty list"
        )

    def test_config_must_load_project_settings(self):
        self.config_module.settings = { 'agiliza': 'rocks' }
        config = ConfigRunner()

        self.assertEqual(
            config.settings, { 'agiliza': 'rocks' },
            "ConfigRunner does not load project settings"
        )

    def test_config_must_load_app_settings(self):
        app = ApplicationModuleMock()
        app.config.settings = { 'app': 'rocks' }
        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.settings, { 'app': 'rocks' },
            "ConfigRunner does not load app settings"
        )

    def test_config_must_load_multiple_app_settings(self):
        app1 = ApplicationModuleMock()
        app2 = ApplicationModuleMock()
        app2.config.settings = { 'app': 'rocks' }

        self.config_module.installed_apps.append(app1)
        self.config_module.installed_apps.append(app2)

        config = ConfigRunner()

        self.assertEqual(
            config.settings, { 'app': 'rocks' },
            "ConfigRunner does not load app settings"
        )

    def test_config_must_load_only_project_settings(self):
        app = ApplicationModuleMock()
        self.config_module.settings = { 'agiliza': 'rocks' }
        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.settings, { 'agiliza': 'rocks' },
            "ConfigRunner does not load app settings"
        )

    def test_config_must_load_project_and_app_settings(self):
        app = ApplicationModuleMock()
        app.config.settings = { 'app': 'rocks' }
        self.config_module.settings = { 'agiliza': 'rocks' }
        self.config_module.installed_apps.append(app)

        config = ConfigRunner()

        self.assertEqual(
            config.settings, { 'agiliza': 'rocks', 'app': 'rocks' },
            "ConfigRunner does not load app settings"
        )

    def test_config_must_load_a_middleware_list_level0(self):
        self.config_module.middleware_level0.append(
            'tests.mocks.middleware.CompleteMiddlewareLevel0Mock'
        )
        self.config_module.middleware_level0.append(
            'tests.mocks.middleware.ProcessRequestMiddlewareLevel0Mock'
        )
        self.config_module.middleware_level0.append(
            'tests.mocks.middleware.ProcessResponseMiddlewareLevel0Mock'
        )

        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level0, (
                CompleteMiddlewareLevel0Mock(),
                ProcessRequestMiddlewareLevel0Mock(),
                ProcessResponseMiddlewareLevel0Mock(),
            ),
            "ConfigRunner does not load a middleware list"
        )

    def test_config_must_not_load_bad_middleware_level0(self):
        self.config_module.middleware_level0.append(
            'tests.mocks.middleware.BadMiddlewareMock'
        )

        with self.assertRaises(BadMiddlewareException,
            msg="Must be raise a BadMiddlewareException"):

            ConfigRunner()

    def test_config_must_load_a_class_level0(self):
        self.config_module.middleware_level0.append(
            CompleteMiddlewareLevel0Mock
        )

        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level0, (CompleteMiddlewareLevel0Mock(),),
            "ConfigRunner does not load middleware_level0"
        )

    def test_config_must_load_an_instance_level0(self):
        self.config_module.middleware_level0.append(
            CompleteMiddlewareLevel0Mock()
        )

        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level0, (CompleteMiddlewareLevel0Mock(),),
            "ConfigRunner does not load middleware_level0"
        )

    def test_config_must_not_load_an_not_callable_middleware(self):
        test_module = types.ModuleType('test_module')
        test_module.NotCallableMiddleware = 'fake'

        sys.modules.setdefault('test_module', test_module)

        self.config_module.middleware_level0.append(
            'test_module.NotCallableMiddleware'
        )

        with self.assertRaises(InvalidMiddlewareException,
            msg="Middleware not callable"):

            ConfigRunner()

        sys.modules.pop('test_module')


    def test_config_must_raise_invalid_middleware_exception_level1(self):
        self.config_module.middleware_level1.append('invalid.middleware.test')

        with self.assertRaises(InvalidMiddlewareException,
            msg="Must be raise a InvalidMiddlewareException"):

            ConfigRunner()

    def test_config_must_load_a_empty_list_level1(self):
        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level1, (),
            "ConfigRunner does not load a empty list"
        )

    def test_config_must_load_a_middleware_list_level1(self):
        self.config_module.middleware_level1.append(
            'tests.mocks.middleware.CompleteMiddlewareLevel1Mock'
        )
        self.config_module.middleware_level1.append(
            'tests.mocks.middleware.ProcessControllerMiddlewareLevel1Mock'
        )
        self.config_module.middleware_level1.append(
            'tests.mocks.middleware.ProcessRenderMiddlewareLevel1Mock'
        )

        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level1, (
                CompleteMiddlewareLevel1Mock(),
                ProcessControllerMiddlewareLevel1Mock(),
                ProcessRenderMiddlewareLevel1Mock(),
            ),
            "ConfigRunner does not load a middleware list"
        )

    def test_config_must_not_load_bad_middleware_level1(self):
        self.config_module.middleware_level1.append(
            'tests.mocks.middleware.BadMiddlewareMock'
        )

        with self.assertRaises(BadMiddlewareException,
            msg="Must be raise a BadMiddlewareException"):

            ConfigRunner()

    def test_config_must_load_a_class_level1(self):
        self.config_module.middleware_level1.append(
            CompleteMiddlewareLevel1Mock
        )

        config = ConfigRunner()

        self.assertEqual(
            config.middleware_level1, (CompleteMiddlewareLevel1Mock(),),
            "ConfigRunner does not load middleware_level1"
        )

    def test_config_must_load_url_patterns(self):
        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp1',
                    'tests.mocks.controllers.CompleteControllerMock',
                    'exp1'
                ),
                url('/exp2', GetControllerMock, 'exp2'),
            )
        )

        config = ConfigRunner()

        self.assertEqual(
            config.urls,
            (
                (
                    re.compile('^/exp1$'),
                    CompleteControllerMock(),
                    (),
                    'exp1',
                    None
                ),
                (
                    re.compile('^/exp2$'),
                    GetControllerMock(),
                    (),
                    'exp2',
                    None
                ),
            ),
            "ConfigRunner does not load url patterns"
        )

    def test_config_must_raise_on_bad_re(self):
        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp[\w-\b]',
                    'tests.mocks.controllers.CompleteControllerMock',
                    'exp1'
                ),
            )
        )

        with self.assertRaises(URLBadformedException,
            msg="Error on regular expression"):

            ConfigRunner()

    def test_config_must_raise_on_bad_import(self):
        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp1',
                    'tests.mocks.controllers.NoReallyMock',
                    'exp1'
                ),
            )
        )

        with self.assertRaises(ControllerNotFoundException,
            msg="Controller not found"):

            ConfigRunner()

    def test_config_must_not_load_an_not_callable_controller(self):
        test_module = types.ModuleType('test_module')
        test_module.NotCallableController = 'fake'

        sys.modules.setdefault('test_module', test_module)

        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp1',
                    'test_module.NotCallableController',
                    'exp1'
                ),
            )
        )

        with self.assertRaises(ControllerNotFoundException,
            msg="Controller not callable"):

            ConfigRunner()

        sys.modules.pop('test_module')

    def test_config_must_raise_on_bad_context_processor(self):
        self.config_module.urls.url_patterns = (
            (
                url(
                    '/exp1',
                    'tests.mocks.controllers.CompleteControllerMock',
                    'exp1',
                    context_processors=(
                        'tests.mocks.context_processors.bad_context_processor',
                    )
                ),
            )
        )

        with self.assertRaises(ContextProcessorNotFoundException,
            msg="Context processor not found"):

            ConfigRunner()



if __name__ == '__main__':
    unittest.main()
