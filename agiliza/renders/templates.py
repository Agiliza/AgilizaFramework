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


Copyright (c) 2012 Álvaro Hurtado <alvarohurtado84@gmail.com>
Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
from os.path import join, exists, getmtime

from jinja2 import Environment
from jinja2 import BaseLoader, TemplateNotFound

from agiliza.renders.base import Render


class Templates(Render):
    def __init__(self, context_data={}, template=None, template_path=".", *args, **kwargs):
        self.context_data = context_data
        self.template = template
        self.template_path = template_path

    def set_template(self, template):
        self.template = template


class Jinja2Render(Templates):
    def render(self):
        env = Environment(loader=MyLoader(self.template_path))
        template = env.loader.load(env, self.template)

        return template.render(self.context_data)



class MyLoader(BaseLoader):
    """
    Loader provisional. Usaremos FileSystemLoader
    """
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == getmtime(path)
