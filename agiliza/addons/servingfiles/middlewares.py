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
from agiliza.core.utils.decorators import cached_property


class ServingFilesMiddleware(object):
    @cached_property
    def paths(self):
        path_info = {}
        path_info.update(settings.get('servingfiles', {}))
        # Media files
        media_url = settings.get('media_url')
        media_root = settings.get('media_root')
        path_info.update({ media_url: media_root })
        # Static files
        static_url = settings.get('static_url')
        static_root = settings.get('static_root')
        path_info.update({ static_url: static_root })

        return path_info

    def get_file(self, path):
        mimetype, encoding = mimetypes.guess_type(path)
        mimetype = mimetype or 'application/octet-stream'

        with open(fullpath, 'rb') as f:
            name = f.name
            encoding = f.encoding
            data = f.read()

        return {
            'mimetype': mimetype,
            'encoding': encoding,
            'filename': name,
            'content': data,
        }

    #def process_request(self, request):
    #    pass

    def process_response(self, request, response):
        if isinstance(response, HttpResponseNotFound):
            return

        for url, base_path in self.paths:
            if request.path_info.startswith(url):
                resource = request.path_info.replace(url, '', 1)
                file_path = os.path.join(base_path, resource)
                if os.path.isfile(file_path):
                        respose.status_code = 404
                        respose.status_text = 'NOT FOUND'

                        data = self.get_file(file_path)
                        response.set_content(
                            data['content'],
                            data['mimetype'],
                            data['encoding'],
                        )

                        response['Content-Disposition'] = \
                            'attachment; filename=%s' % data['filename']

                        return


