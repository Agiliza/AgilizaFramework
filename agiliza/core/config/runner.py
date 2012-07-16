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
along with Agiliza. If not, see <http://www.gnu.org/licenses/>.

Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
Copyright (c) 2012 Álvaro Hurtado <alvarohurtado84@gmail.com>
"""
import inspect
import importlib
import re
from functools import reduce

from agiliza.urls.urls import include

from agiliza.core.config.exceptions import (InvalidApplicationException,
    BadApplicationConfigurationException, InvalidMiddlewareException,
    BadMiddlewareException, ControllerNotFoundException,
    ContextProcessorNotFoundException, URLBadformedException,)


class ConfigRunner(object):
    def __init__(self, config_module):
        self.installed_apps = self._get_installed_apps(
            config_module.installed_apps
        )
        
        self.settings = self._get_settings(config_module)
        

        self.middleware_level0 = self._get_middleware_list(
            config_module.middleware_level0,
            ('process_request', 'process_response'),
        )

        self.middleware_level1 = self._get_middleware_list(
            config_module.middleware_level1,
            ('process_controller', 'process_render'),
        )

        self.urls = self._get_url_list(config_module.url_patterns)
        
        
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
                raise BadApplicationConfigurationException(
                    '"%s" application does not have a config module' % app_name
                )

            installed_apps.append(app)

        return tuple(installed_apps)


    def _get_settings(self, config_module):
        full_settings = {}
        for installed_app in config_module.installed_apps:
            if getattr(installed_app, "settings", None):
                full_settings.update(installed_app.settings)
                
        if getattr(config_module, "settings", None):
            full_settings.update(config_module.settings)
            
        return full_settings


    def _get_middleware_list(self, middleware_level, middleware_methods):
        middleware_list = []
        for middleware_name in middleware_level:
            if isinstance(middleware_name, str):
                parts = middleware_name.split('.')
                attr_name = parts[-1]
                module_name = reduce(lambda x, y: x + '.' + y, parts[0:-1])
                try:
                    module = importlib.import_module(module_name)
                except ImportError as error:
                    raise InvalidMiddlewareException(error)

                middleware = getattr(module, attr_name, None)
            else:
                middleware = middleware_name

            any_method = any([
                    getattr(middleware, method, None)
                    for method in middleware_methods
            ])

            if not any_method:
                raise BadMiddlewareException(
                    '"%s" middleware must have any method to process \
                    in this level' % middleware_name
                )

            middleware_list.append(middleware)

        return tuple(middleware_list)
        
        
    def _get_url_list(self, url_patterns):
        urls = []
        not_finished_urls = []
        for url_list in url_patterns:
            not_finished_urls = not_finished_urls + url_list
            
        for url in not_finished_urls:
            try:
                regexp = re.compile(url[0])
            except re.error as error:
                raise URLBadformedException(error)
            
            try:
                target = importlib.import_module(url[1])
            except ImportError as error:
                raise ControllerNotFoundException(error)
            
            try:
                context_processors = [importlib.import_module(context_processor) for context_processor in url[2]],
            except ImportError as error:
                raise ContextProcessorNotFoundException(error)
            
            urls.append((
                regexp,    
                target,
                context_processors,
                url[3],
                url[4],
            ))
            
        return tuple(urls)
                