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
import inspect
import importlib

from agiliza.core.config.exceptions import (InvalidApplicationException,
    ConfigMissingInApplicationException)


class ConfigRunner(object):
    def __init__(self, config_module):
        self.installed_apps = self._get_installed_apps(
            config_module.installed_apps
        )

    def _get_installed_apps(self, config_installed_apps):
        installed_apps = []
        for app_name in config_installed_apps:
            if isinstance(app_name, str):
                try:
                    app = importlib.import_module(app_name)
                except ImportError as error:
                    raise InvalidApplicationException(error)
            elif inspect.ismodule(app_name):
                app = app_name
            else:
                raise InvalidApplicationException(
                    '"%s" application must be a module or a string' % app_name
                )

            if not getattr(app, 'config', None):
                raise ConfigMissingInApplicationException(
                    '"%s" application does not have a config module' % app_name
                )

            installed_apps.append(app)

        return tuple(installed_apps)
