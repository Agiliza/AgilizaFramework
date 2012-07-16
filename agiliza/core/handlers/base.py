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
from agiliza import http
from agiliza.http import HttpResponseNotFound, HttpResponseNotAllowed
from agiliza.core.handlers.context import ContextManager

import re
import os

class Handler(object):
    def __init__(self):
        self.config = object()

    def dispatch(self, request):
        """Returns an Response object for the given Request."""
        params = {} # TODO: URL params
        response = None


        #"""
        #Execute level-0 Middlewares IN
        #"""
        for mw in self.config.middleware_level0:
            mw.process_request(request)
        
        
        #"""
        #Select correct URL
        #"""
        found = False
        for url in self.config.urls:
            results = url[0].match(request.path_info)
            if results is not None:
                params = results.groupdict()
                url_regex, url_controller, \
                    url_context_processors, url_name, url_name = url
                break
            
        if found is False:
            raise HttpResponseNotFound()
            
        
        #"""
        #Execute controller with request + params + config
        #"""
        response = url_controller.dispatch(
            request = request,
            params = params,
            settings = self.config.settings,
            session = request.session, #TODO
            cookies = request.cookies, #TODO
        )
        
        if not isinstance(response, http.HttpResponse):
            
            response_data = response
            
            #"""
            #Search apropiate template
            #It is: url_name + [_ + url_layout] + . + accept_subtype
            #"""
            accepts = sorted(
                [[key, request.accept[key]] for key in request.accept.keys()],
                key=lambda accept: accept[1],
                reverse=True
                )
            
            any_accepted = None
            for accept in accepts:
                accept_subtype = accept[0].split("/")[1]
                if url_layout:
                    template_name = url_name+"_" + url_layout + "." + accept_subtype
                else:
                    template_name = url_name+"."+accept_subtype
                    
                template_path = self.config.templates + template_name
    
                if os.path.isfile(template_path):
                    any_accepted = True
                    break
    
                
            if not any_accepted:
                raise HttpResponseUnsuporttedMediaType()
            
            
            #"""
            #Execute the necessary context_processors
            #"""
            context_data = {}
            for context_processor in url_context_processors:
                context_data.update(
                    context_processor(request,
                                  params,
                                  self.config.settings,
                                  request.session)
                    )
    
            #"""
            #Render the template with response + request + contexts_info
            #"""
            context_data.update(response_data)
            render = Render(
                template = template_path,
                context = context_data,
            )

            
            response = http.HttpResponse(
                content = render.render(),
                content_type = accept,
                )
            
            
        response.set_cookies(cookies)
        
        #"""
        #Execute level-0 Middlewares OUT
        #"""
        for mw in self.config.middleware_level0:
            mw.process_response(request, response)


        return response

        
