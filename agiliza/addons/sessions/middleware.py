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
from http.cookies import SimpleCookie

from agiliza.addons.sessions.exceptions import InvalidSessionSettingsException
from agiliza.config import settings


class SessionMiddleware(object):
    def __init__(self):
        sesion_settings = settings.get('sessions')
        if session_settings is not None:
            # Getting the expires function
            expires_func = None
            expires = sesion_settings.get('expires', '')
            if expires:
                if isinstance(expires, str):
                    try:
                        expires = import_object(expires)
                    except ImportError as error:
                        raise InvalidSessionSettingsException(error)

                if callable(expires):
                    expires_func = expires
                else:
                    raise InvalidSessionSettingsException(
                        "'expires' setting is not callable"
                    )

            self.expires = expires_func or expires
            self.path = sesion_settings.get('path', '') or ''
            self.comment = sesion_settings.get('comment', '') or ''
            self.domain = sesion_settings.get('domain', '') or ''
            self.max_age = sesion_settings.get('max_age', '') or ''
            self.secure = sesion_settings.get('secure', '') or ''
            self.version = sesion_settings.get('version', '') or ''
            self.httponly = sesion_settings.get('httponly', '') or ''

    def process_request(self, request):
        # Retrive the session cookie
        sid = request.cookies.get('sid')
        if sid: # Retrieve a previous session
            session_cookie = SimpleCookie() # Just 'sid' cookie
            session_cookie['sid'] = request.cookies['sid'].value
            session_cookie['sid'].update(request.cookies['sid'])
        else: # New session
            session_cookie = SimpleCookie()
            session_cookie['sid'] = ''
            session_cookie['sid']['expires'] = self.expires()
            session_cookie['sid']['path'] = self.path
            session_cookie['sid']['comment'] = self.comment
            session_cookie['sid']['domain'] = self.domain
            session_cookie['sid']['max_age'] = self.max_age
            session_cookie['sid']['secure'] = self.secure
            session_cookie['sid']['version'] = self.version
            session_cookie['sid']['httponly'] = self.httponly

        session = Session(session_cookie)
        # Link the session to request
        request.session = session

    def process_controller(self, controllerfunc, request, params):
        # Link the session to controller
        controllerfunc.session = request.session

    def process_controller_response(self, controllerfunc, request, response):
        # Unlink the session from controller
        del controllerfunc.session

    def process_response(self, request, response):
        # Retrieve the session from request
        session = request.session
        # Unlink the session from request
        del request.session
        # Check if it is a new session
        sid = request.cookies.get('sid')
        if not sid:
            response.set_cookies(session.get_cookie())
        # Save the changes on server
        session.save()
