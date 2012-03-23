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
import inspect

from agiliza import http
from agiliza.core.urls import URLRegexp


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

    #def render(self, data,

    def dispatch(self, request, session, config, user, *args, **kwargs):
        url = request.meta['path_info']

        match = None
        for regexp in self.urls():
            match = regexp.match(url)
            if match is not None: break

        alias = regexp.alias

        try:
            kwargs = match or {}
            method_name = request.method.lower() + alias
            # Getting the method
            method = getattr(self, method_name)
            # Inspecting method's args
            argspec = inspect.getfullargspec(method)
            for arg in kwargs.keys():
                if not arg in argspec.args:
                    raise http.HttpMethodNotAllowedException()

            # Calling the method
            self.request = request
            self.session = session
            self.config = config
            self.user = user
            context_data, templates = method(**kwargs)
            # Cheking the content-type
            if self.request.accept:
                raise http.HttpNotAcceptableException()

            # Rendering the template
            response = http.HttpResponseOk()
        except (AttributeError, HttpMethodNotAllowedException) as e:
            # TODO: ¿Cómo generar Allow methods?
            allow = []
            response = http.HttpResponseMethodNotAllowed(allow)
        except HttpNotAcceptableException as e: # Part of HTTP Content Negotiation
            response = http.HttpResponseNotAcceptable()

        return response

