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
import mimetypes
import os

from agiliza.config import settings
from agiliza.http import HttpResponseNotFound, HttpResponseOk
from agiliza.core.config import ConfigRunner
from agiliza.core.utils.decorators import cached_property


class ServingFilesMiddleware(object):
    @cached_property
    def paths(self):
        config = ConfigRunner()
        path_info = {}
        path_info.update(settings.get('servingfiles', {}))
        # Media files
        media_url = config.media_url
        media_root = config.media_root
        if media_url and media_root:
            path_info.update({ media_url: media_root })
        # Static files
        static_url = config.static_url
        static_root = config.static_root
        if static_url and static_root:
            path_info.update({ static_url: static_root })

        return path_info

    def get_file(self, path):
        mimetype, encoding = mimetypes.guess_type(path)
        mimetype = mimetype or 'application/octet-stream'

        with open(path, 'rb') as f:
            name = f.name
            data = f.read()

        return {
            'mimetype': mimetype,
            'encoding': encoding,
            'filename': name,
            'content': data,
        }

    def process_request(self, request):
        for url, base_path in self.paths.items():
            if request.path_info.startswith(url):
                resource = request.path_info.replace(url, '', 1)
                file_path = os.path.join(base_path, resource)
                if os.path.isfile(file_path):
                        response = HttpResponseNotFound()
                        response.status_code = 200
                        response.status_text = 'OK'

                        data = self.get_file(file_path)
                        response.set_content(
                            data['content'],
                            data['mimetype'],
                            data['encoding'],
                        )

                        response['Content-Disposition'] = \
                            'attachment; filename=%s' % data['filename']

                        raise response

    def process_response(self, request, response):
        pass


