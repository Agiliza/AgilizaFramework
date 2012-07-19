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
import os
from http.cookies import SimpleCookie

from agiliza.addons.sessions.exceptions import InvalidSessionSettingsException
from agiliza.config import settings


class Session(object):
    def __init__(self, cookie, sid=None):
        if not sid:
            session_id = self.get_identifier()
        else:
            session_id = sid

        try:
            session_dir = settings['sessions']['directory']
            session_writeback = settings['sessions'].get('writeback', True)
        except AttributeError as error:
            raise InvalidSessionSettingsException(
                "%s: 'directory' for session is not defined" % error
            )

        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 0o2770)
            except OSError as error:
                raise InvalidSessionSettingsException(
                    "%s: Error trying to create the session directory" % error
                )

        session_file = os.path.join(session_dir, session_id)
        if sid and not os.path.isfile(session_file):
            # It requests a session that it does not exist, so we create a new one
            session_id = self.get_identifier()

        self._data = shelve.open(session_file, writeback=session_writeback)


        if not sid:
            self._data.update({
                'sid': session_id,
                'cookie': { k:v for k,v in cookie['sid'].items() }
            })


        os.chmod(session_file+".db", 0o660)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def get_identifier(self):
        return str(uuid.uuid1())

    def get_cookie(self):
        sid = self._data['sid']
        cookie_data = self._data['cookie']
        cookie = SimpleCookie()
        cookie['sid'] = sid
        cookie['sid'].update(cookie_data)
        return cookie

    def save(self):
        self._data.close()
