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
class ConfigRunnerException(Exception):
    """This exception is a base for all ``ConfigRunner`` exceptions."""


class InvalidApplicationException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it can't load an
    application from ``installed_apps``."""

class BadApplicationConfigurationException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it load an
    application from ``installed_apps`` and this application doesn't have a
    ``config`` module."""


class InvalidMiddlewareException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it can't load a
    middleware from middleware list."""

class BadMiddlewareException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it load a
    middleware from middleware list and this middleware doesn't have any method
    to process in its level."""

class ControllerNotFoundException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it try to
    import a Controller while it is creatig the urls list."""

class ContextProcessorNotFoundException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it try to
    import a ContextProcessor while it is creating the urls list."""

class URLBadformedException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it try to
    compile a url to regular expresion while it is creatig the urls list."""

class ConfigModuleImportException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it try to load the
    config module."""

class TemplatePathException(ConfigRunnerException):
    """This exception is launched by ``ConfigRunner`` when it check the template
    path."""
