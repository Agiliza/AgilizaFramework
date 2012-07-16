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

from agiliza.core.config import ConfigRunner
from agiliza.core.config.exceptions import *
from tests.mocks.config import *
from tests.mocks.middleware import *


class ConfigRunnerTest(unittest.TestCase):

    def setUp(self):
        self.config_module = ConfigModuleMock({
            'installed_apps': list(),
            'middleware_level0': list(),
            'middleware_level1': list(),
            'urls': UrlModuleMock(tuple()),
        })

    def test_config_must_load_an_app_name(self):
        import agiliza.core
        self.config_module.installed_apps.append('agiliza.core')

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.installed_apps, (agiliza.core,),
            "ConfigRunner does not load installed_apps"
        )

    def test_config_must_load_a_module(self):
        import agiliza.core
        self.config_module.installed_apps.append(agiliza.core)

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.installed_apps, (agiliza.core,),
            "ConfigRunner does not load installed_apps"
        )

    def test_must_not_load_a_list_as_an_app(self):
        self.config_module.installed_apps.append(['agiliza.core', ])

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner(self.config_module)

    def test_must_raise_invalid_application_exception(self):
        self.config_module.installed_apps.append('invalid.module.test')

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner(self.config_module)

    def test_config_must_load_a_empty_application_list(self):
        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.installed_apps, (),
            "ConfigRunner does not load a empty list"
        )

    def test_must_raise_bad_application_configuration_exception(self):
        self.config_module.installed_apps.append('sys')

        with self.assertRaises(BadApplicationConfigurationException,
            msg="Must be raise a BadApplicationConfigurationException"):

            ConfigRunner(self.config_module)


    def test_config_must_raise_invalid_middleware_exception_level0(self):
        self.config_module.middleware_level0.append('invalid.middleware.test')

        with self.assertRaises(InvalidMiddlewareException,
            msg="Must be raise a InvalidMiddlewareException"):

            ConfigRunner(self.config_module)

    def test_config_must_load_a_empty_list_level0(self):
        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.middleware_level0, (),
            "ConfigRunner does not load a empty list"
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

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.middleware_level0, (
                CompleteMiddlewareLevel0Mock,
                ProcessRequestMiddlewareLevel0Mock,
                ProcessResponseMiddlewareLevel0Mock,
            ),
            "ConfigRunner does not load a middleware list"
        )

    def test_config_must_not_load_bad_middleware_level0(self):
        self.config_module.middleware_level0.append(
            'tests.mocks.middleware.BadMiddlewareMock'
        )

        with self.assertRaises(BadMiddlewareException,
            msg="Must be raise a BadMiddlewareException"):

            ConfigRunner(self.config_module)

    def test_config_must_load_a_class_level0(self):
        self.config_module.middleware_level0.append(CompleteMiddlewareLevel0Mock)

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.middleware_level0, (CompleteMiddlewareLevel0Mock,),
            "ConfigRunner does not load middleware_level0"
        )


    def test_config_must_raise_invalid_middleware_exception_level1(self):
        self.config_module.middleware_level1.append('invalid.middleware.test')

        with self.assertRaises(InvalidMiddlewareException,
            msg="Must be raise a InvalidMiddlewareException"):

            ConfigRunner(self.config_module)

    def test_config_must_load_a_empty_list_level1(self):
        config = ConfigRunner(self.config_module)

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

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.middleware_level1, (
                CompleteMiddlewareLevel1Mock,
                ProcessControllerMiddlewareLevel1Mock,
                ProcessRenderMiddlewareLevel1Mock,
            ),
            "ConfigRunner does not load a middleware list"
        )

    def test_config_must_not_load_bad_middleware_level1(self):
        self.config_module.middleware_level1.append(
            'tests.mocks.middleware.BadMiddlewareMock'
        )

        with self.assertRaises(BadMiddlewareException,
            msg="Must be raise a BadMiddlewareException"):

            ConfigRunner(self.config_module)

    def test_config_must_load_a_class_level1(self):
        self.config_module.middleware_level1.append(
            CompleteMiddlewareLevel1Mock
        )

        config = ConfigRunner(self.config_module)

        self.assertEqual(
            config.middleware_level1, (CompleteMiddlewareLevel1Mock,),
            "ConfigRunner does not load middleware_level1"
        )

if __name__ == '__main__':
    unittest.main()
