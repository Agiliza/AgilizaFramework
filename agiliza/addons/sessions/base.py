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
from hashlib import sha
from http.cookies import BaseCookie


class Session(object):

    def __init__(self, cookies, expires=None, cookie_path=None):
        assert isinstance(cookies, BaseCookie)

        self._cookies = cookies

        if self._cookie.get('sid'):
            sid = self._cookie['sid'].value
        else:
            sid = sha.new(repr(time.time())).hexdigest()

        # Clear session cookie from other cookies
        self._cookie.clear()

        self.cookie['sid'] = sid

        if cookie_path:
            self.cookie['sid']['path'] = cookie_path

        session_dir = os.environ['DOCUMENT_ROOT'] + '/session'
        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 02770)
            # If the apache user can't create it create it manualy
            except OSError, e:
                errmsg =  """%s when trying to create the session directory. \
Create it as '%s'""" % (e.strerror, os.path.abspath(session_dir))
                raise OSError, errmsg
        self.data = shelve.open(session_dir + '/sess_' + sid, writeback=True)
        os.chmod(session_dir + '/sess_' + sid, 0660)

        # Initializes the expires data
        if not self.data.get('cookie'):
            self.data['cookie'] = {'expires':''}

        self.set_expires(expires)

    def close(self):
        self.data.close()

    def set_expires(self, expires=None):
        if expires == '':
            self.data['cookie']['expires'] = ''
        elif isinstance(expires, int):
            self.data['cookie']['expires'] = expires

        self.cookie['sid']['expires'] = self.data['cookie']['expires']
