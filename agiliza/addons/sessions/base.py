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
import shelve
import uuid

from agiliza.addons.sessions.exceptions import InvalidSessionSettingsException
from agiliza.config import settings


class Session(dict):
    def __init__(self, cookie):
        if not cookie['sid']:
            cookie['sid'] = self.get_identifier()

        sid = cookie['sid'].value

        try:
            session_dir = settings['session']['directory']
            session_file_prefix = settings['session'].get('file_prefix', 'sess_')
            session_writeback = settings['session'].get('writeback', True)
        except AttributeError as error:
            raise InvalidSessionSettingsException(
                "%s: 'directory' for session is not defined" % error
            )

        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 02770)
            except OSError as error:
                raise InvalidSessionSettingsException(
                    "%s: Error trying to create the session directory" % error
                )

        session_file = os.path.join(session_dir, session_file_prefix + sid)
        self._data = shelve.open(session_file, writeback=session_writeback)
        if not 'cookie' in self._data:
            self._data['cookie'] = cookie

        os.chmod(session_file, 0660)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def get_identifier(self):
        return str(uuid.uuid1())

    def save(self):
        self._data.close()
