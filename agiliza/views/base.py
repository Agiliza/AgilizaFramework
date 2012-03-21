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
import abc

from agiliza import http
from agiliza.core.urls import URLRegexp
from agiliza.http.exceptions import (MethodNotAllowedException,
    NotAcceptableException)


__all__ = ('View',)


class View(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def url_patterns(self):
        """URL patterns for this view."""

    def urls(self):
        url_list = [
            pattern if isinstance(pattern, URLRegexp)
            else URLRegexp(*pattern)
            for pattern in self.url_patterns()
        ]
        return tuple(url_list)

    def dispatch(self, request, session, config, user, *args, **kwargs):
        url = request.meta['path_info']

        print('')
        print('DISPATCH', '*'*10)
        match = None
        for regexp in self.urls():
            match = regexp.match(url)
            if match is not None: break

        alias = regexp.alias

        method_name = request.method.lower() + alias
        try:
            print('URL:', alias)
            print('METHOD NAME:', method_name)
            method = getattr(self, method_name)
            self.request = request
            self.session = session
            self.config = config
            self.user = user
            kwargs = match or {}
            response = method(**kwargs)
        except AttributeError as e:
            response = http.HttpResponseMethodNotAllowed()
        print('')
        return response

