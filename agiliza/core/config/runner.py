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
import os
from functools import reduce

from agiliza.core.config.exceptions import (InvalidApplicationException,
    BadApplicationConfigurationException, InvalidMiddlewareException,
    BadMiddlewareException, ControllerNotFoundException,
    ContextProcessorNotFoundException, URLBadformedException,
    ConfigModuleImportException, TemplatePathException, InvalidRenderException)
from agiliza.core.utils.imports import import_object
from agiliza.core.utils.patterns import Singleton
from agiliza.renders import Jinja2Render


class ConfigRunner(Singleton):
    def __init__(self):
        try:
            config_module_name = os.environ['AGILIZA_CONFIG']
            config_module = importlib.import_module(config_module_name)
        except KeyError as error:
            raise ConfigModuleImportException(
                "Environment has not '%s' variable" %
                    error.args[0].decode('utf-8')
            )
        except ImportError as error:
            raise ConfigModuleImportException(error)

        self._internal = {
            'debug': False,
            'media_root': None,
            'media_url': '/media/',
            'static_root': None,
            'static_url': '/static/',
            'installed_apps': (),
            'middleware_level0': (),
            'middleware_level1': (),
            'urls': (),
            'templates': {
                'directory': None,
                'render': Jinja2Render,
            }
        }

        # Load templates info
        templates = self._get_templates_info(config_module)
        self._internal.update({'templates': templates})

        if hasattr(config_module, 'media_root'):
            self._internal.update({'media_root': config_module.media_root})
        if hasattr(config_module, 'media_url'):
            self._internal.update({'media_url': config_module.media_url})

        if hasattr(config_module, 'static_root'):
            self._internal.update({'static_root': config_module.static_root})
        if hasattr(config_module, 'static_url'):
            self._internal.update({'static_url': config_module.static_url})

        # Load installed apps
        try:
            installed_apps = self._get_installed_apps(
                config_module.installed_apps
            )
            self._internal.update({'installed_apps': installed_apps})
        except AttributeError:
            pass

        # Load settings
        self.settings = self._get_settings(config_module)

        # Load middleware level0
        try:
            middleware_level0 = self._get_middleware_list(
                config_module.middleware_level0,
                ('process_request', 'process_response'),
            )
            self._internal.update({'middleware_level0': middleware_level0})
        except AttributeError:
            pass

        # Load middleware level1
        try:
            middleware_level1 = self._get_middleware_list(
                config_module.middleware_level1,
                ('process_controller', 'process_controller_response'),
            )
            self._internal.update({'middleware_level1': middleware_level1})
        except AttributeError:
            pass

        # Load urls
        try:
            urls_module_name = '%s.urls' % config_module_name
            urls_module = importlib.import_module(urls_module_name)
            urls = self._get_url_list(urls_module.url_patterns)
            self._internal.update({'urls': urls})
        except AttributeError:
            raise ConfigModuleImportException(
                "'%s' module has not 'url_patterns' attribute" %
                    urls_module_name
            )
        except ImportError as error:
            raise ConfigModuleImportException(
                "'config' module has not 'config.urls' submodule: %s" % error
            )


    def _get_templates_info(self, config_module):
        templates = getattr(config_module, 'templates', {})
        assert type(templates) == dict, "templates must be an dictionary"

        directory = templates.get('directory')
        if directory is not None:
            if not os.path.exists(directory):
                raise TemplatePathException(
                    "Template path '%s' does not exist" % directory
                )

        render = templates.get('render', Jinja2Render)

        if isinstance(render, str):
            try:
                render = import_object(render)
            except ImportError as error:
                raise InvalidRenderException(error)

        if not callable(render):
            raise InvalidRenderException("render must be callable")
        else:
            templates['render'] = render

        return templates


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
                    "'%s' application must be a module or a string" % app_name
                )

            installed_apps.append(app)

        return tuple(installed_apps)


    def _get_settings(self, config_module):
        full_settings = {}
        for installed_app in self.installed_apps:
            app_config = getattr(installed_app, 'config', None)
            if app_config is not None:
                app_settings = getattr(app_config, 'settings', None)
                if app_settings is not None:
                    full_settings.update(app_settings)

        if getattr(config_module, 'settings', None):
            full_settings.update(config_module.settings)

        return full_settings


    def _get_middleware_list(self, middleware_level, middleware_methods):
        middleware_list = []
        for middleware_name in middleware_level:
            if isinstance(middleware_name, str):
                try:
                    middleware = import_object(middleware_name)
                    middleware = middleware()
                except (ImportError, AttributeError) as error:
                    raise InvalidMiddlewareException(error)
                except TypeError as error: # It is not callable
                    raise InvalidMiddlewareException(error)
            elif callable(middleware_name):
                middleware = middleware_name()
            else:
                middleware = middleware_name

            any_method = any([
                getattr(middleware, method, None)
                for method in middleware_methods
            ])

            if not any_method:
                raise BadMiddlewareException(
                    "'%s' middleware must have any method to process \
                    in this level" % middleware_name
                )

            middleware_list.append(middleware)

        return tuple(middleware_list)

    def _get_url_list(self, url_patterns):
        from agiliza.config.urls import include

        assert type(url_patterns) == list or type(url_patterns) == tuple,\
            "'url_pattern' must be a list or tuple"

        urls = []
        not_finished_urls = []
        for url_list in url_patterns:
            not_finished_urls = not_finished_urls + url_list

        for url in not_finished_urls:
            regexp, target, context_processors, name, layout_name = url
            try:
                regexp = re.compile(regexp)
            except re.error as error:
                raise URLBadformedException(error)

            if isinstance(target, str):
                try:
                    target_class = import_object(target)
                    target = target_class()
                except (ImportError, AttributeError) as error:
                    raise ControllerNotFoundException(error)
                except TypeError as error: # It is not callable
                    raise ControllerNotFoundException(error)

            if callable(target):
                target = target()

            try:
                context_processors = tuple([
                    import_object(context_processor)
                    for context_processor in context_processors
                ])
            except (ImportError, AttributeError) as error:
                raise ContextProcessorNotFoundException(error)

            urls.append((
                regexp,
                target,
                context_processors,
                name,
                layout_name,
            ))

        return tuple(urls)

    def __getattr__(self, name):
        try:
            attr = self._internal[name]
        except KeyError:
            raise AttributeError(name)

        return attr
