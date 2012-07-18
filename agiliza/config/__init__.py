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
class LazySettingsImport(object):
    def __init__(self):
        self._settings = None

    def _get_settings(self):
        from agiliza.core.config import ConfigRunner
        config = ConfigRunner()
        self._settings = config.settings

    def __getitem__(self, key):
        if self._settings is None:
            self._get_settings()
        return self._settings[key]

    def __setitem__(self, key, value):
        if self._settings is None:
            self._get_settings()
        self._settings[key] = value

    def __getattr__(self, name):
        if self._settings is None:
            self._get_settings()
        return getattr(self._settings, name)

settings = LazySettingsImport()




