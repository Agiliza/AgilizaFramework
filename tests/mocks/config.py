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
class NiceDict(dict):
    def __getattr__(self, key):
        if key not in self.keys():
            raise KeyError
        return self[key]

    def __setattr__(self, key, value):
        if key not in self.keys():
            raise KeyError
        self[key] = value

class ConfigModuleMock(NiceDict):
    """Simulate the module ``site/config`` with initial configuration."""
    pass

class UrlModuleMock(NiceDict):
    def __init__(self, url_patterns):
        self['url_patterns'] = url_patterns
