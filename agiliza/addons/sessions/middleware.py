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

from agiliza.addons.sessions.base import Session
from agiliza.addons.sessions.exceptions import InvalidSessionSettingsException
from agiliza.config import settings
from agiliza.core.utils.decorators import cached_property


class SessionMiddleware(object):
    @cached_property
    def expires(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            # Getting the expires function
            expires_func = None
            expires = session_settings.get('expires', '')
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

            return expires_func or expires
        return ''
    
    @cached_property
    def path(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('path', '') or ''
        return ''
    
    @cached_property
    def comment(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('comment', '') or ''
        return ''
    
    @cached_property
    def domain(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('domain', '') or ''
        return ''
    
    @cached_property
    def max_age(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('max_age', '') or ''
        return ''
    
    @cached_property
    def secure(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('secure', '') or ''
        return ''
            
    @cached_property
    def version(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('version', '') or ''
        return ''
    
    @cached_property
    def httponly(self):
        session_settings = settings.get('sessions')
        if session_settings is not None:
            return session_settings.get('httponly', '') or ''
        return ''

    def process_request(self, request):
        # Retrive the session cookie
        sid = request.cookies.get('sid')
        if sid: # Retrieve a previous session
            session_cookie = SimpleCookie() # Just 'sid' cookie
            session_cookie['sid'] = request.cookies['sid'].value
            session_cookie['sid'].update(request.cookies['sid'])
            session = Session(request.cookies, request.cookies['sid'].value)
        else: # New session
            session_cookie = SimpleCookie()
            session_cookie['sid'] = ''
            if self.expires:
                session_cookie['sid']['expires'] = self.expires()
            session_cookie['sid']['path'] = self.path
            session_cookie['sid']['comment'] = self.comment
            session_cookie['sid']['domain'] = self.domain
            session_cookie['sid']['max-age'] = self.max_age
            session_cookie['sid']['secure'] = self.secure
            session_cookie['sid']['version'] = self.version
            session_cookie['sid']['httponly'] = self.httponly
            session = Session(session_cookie)
        
        #session = Session(sid)
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
        
