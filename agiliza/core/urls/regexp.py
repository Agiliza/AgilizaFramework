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
import re

class URLRegexp(object):
    def __init__(self, regexp, alias=None):
        if not isinstance(regexp, str):
            raise ValueError("Regular expression must be a str instance")

        if not alias:
            alias = ''

        if not isinstance(alias, str):
            raise ValueError("Alias must be a str instance")

        alias = '_' + alias

        self.regexp = re.compile(regexp)
        self.alias = alias

        if len(self.regexp.groupindex.keys()) != self.regexp.groups:
            raise Exception()# All groups must be named

    def match(self, url):
        print('URLRegexp:', self.regexp.pattern, 'for:', url)
        params = self.regexp.match(url)
        if params:
            params = params.groupdict()
        return params
