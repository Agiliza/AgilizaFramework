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
import types

from tests.mocks.utils import NiceDict


class ConfigModuleMock(types.ModuleType):
    """Simulate the module ``site/config`` with initial configuration."""
    def __init__(self, name='config_module', *args, **kwargs):
        super(types.ModuleType, self).__init__(name, *args, **kwargs)
        self.installed_apps = list()
        self.middleware_level0 = list()
        self.middleware_level1 = list()
        self.templates = { 'directory': '/' }
        self.urls = UrlModuleMock('config_module.urls')

class ApplicationModuleMock(types.ModuleType):
    """Simulate the module ``application/config`` with initial configuration."""
    def __init__(self, name='app_test', *args, **kwargs):
        super(types.ModuleType, self).__init__(name, *args, **kwargs)
        self.config = ConfigModuleMock('app_test.config')

class UrlModuleMock(types.ModuleType):
    """Simulate the module ``config/urls`` with initial configuration."""
    def __init__(self, name='config.urls', *args, **kwargs):
        super(UrlModuleMock, self).__init__(name, *args, **kwargs)
        self.url_patterns = tuple()
