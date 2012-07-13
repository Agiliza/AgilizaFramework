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
from agiliza.core.config.exceptions import (InvalidApplicationException,
    ConfigMissingInApplicationException)


class ConfigRunnerTest(unittest.TestCase):

    def get_config_module(self):

        class FakeConfigModule(dict):
            """Simulate the module ``site/config.py`` with initial
            configuration."""
            def __getattr__(self, key):
                if key not in self.keys():
                    raise KeyError
                return self[key]

            def __setattr__(self, key, value):
                if key not in self.keys():
                    raise KeyError
                self[key] = value


        return FakeConfigModule({
            'installed_apps': list(),
            'middleware_level0': list(),
            'middleware_level1': list(),
        })

    def test_config_must_load_an_app_name(self):
        import agiliza.core
        config_module = self.get_config_module()
        config_module.installed_apps.append('agiliza.core')

        config = ConfigRunner(config_module)

        self.assertEqual(
            config.installed_apps, (agiliza.core,),
            "ConfigRunner does not load installed_apps"
        )

    def test_config_must_load_a_module(self):
        import agiliza.core
        config_module = self.get_config_module()
        config_module.installed_apps.append(agiliza.core)

        config = ConfigRunner(config_module)

        self.assertEqual(
            config.installed_apps, (agiliza.core,),
            "ConfigRunner does not load installed_apps"
        )

    def test_must_not_load_a_list_as_an_app(self):
        config_module = self.get_config_module()
        config_module.installed_apps.append(['agiliza.core', ])

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner(config_module)

    def test_must_raise_invalid_application_exception(self):
        config_module = self.get_config_module()
        config_module.installed_apps.append('invalid.module.test')

        with self.assertRaises(InvalidApplicationException,
            msg="Must be raise a InvalidApplicationException"):

            ConfigRunner(config_module)

    def test_must_raise_config_missing_in_application_exception(self):
        config_module = self.get_config_module()
        config_module.installed_apps.append('sys')

        with self.assertRaises(ConfigMissingInApplicationException,
            msg="Must be raise a ConfigMissingInApplicationException"):

            ConfigRunner(config_module)

if __name__ == '__main__':
    unittest.main()
