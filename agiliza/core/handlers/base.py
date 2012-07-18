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
Copyright (c) 2012 Alvaro Hurtado <alvarohurtado84@gmail.com>
"""
import re
import os
from http.cookies import SimpleCookie

from agiliza import http
from agiliza.core.config import ConfigRunner


class Handler(object):
    def __init__(self):
        self.config = ConfigRunner()
        Render = self.config.template_render
        self.render = Render(self.config.templates).render

    def dispatch(self, request):
        """Returns an Response object for the given Request."""
        params = {}
        response = None

        #
        # Execute level-0 Middlewares IN
        #
        for middleware in self.config.middleware_level0:
            middleware.process_request(request)

        #
        # Select correct URL
        #
        found = False
        for url in self.config.urls:
            results = url[0].match(request.path_info)
            if results is not None:
                params = results.groupdict()
                url_regex, url_controller, \
                    url_context_processors, url_name, url_layout = url
                found = True
                break

        if found is False:
            raise http.HttpResponseNotFound()

        #
        # Execute controller
        #
        cookies = SimpleCookie()
        url_controller.cookies = cookies

        #
        # Execute level-1 Middlewares IN
        #
        for middleware in self.config.middleware_level1:
            middleware.process_controller(url_controller, request, params)

        response = url_controller.dispatch(request, params)

        #
        # Execute level-1 Middlewares OUT
        #
        for middleware in self.config.middleware_level1:
            middleware.process_controller_response(
                url_controller, request, response
            )

        if not isinstance(response, http.response.HttpResponse):
            response_data = response
            #
            # Search apropiate template
            # It is: url_name + [_ + url_layout] + . + accept_subtype
            #
            accepts = sorted(
                [
                    [key, request.accept[key]]
                    for key in request.accept.keys()
                ],
                key=lambda accept: accept[1],
                reverse=True
            )

            any_accepted = None
            for accept in accepts:
                accept_subtype = accept[0].split("/")[1]
                if url_layout:
                    template_name = url_name + "_" + url_layout + \
                        "." + accept_subtype
                else:
                    template_name = url_name + "." + accept_subtype

                template_path = self.config.templates + template_name

                if os.path.isfile(template_path):
                    any_accepted = True
                    break

            if not any_accepted:
                raise http.HttpResponseUnsupportedMediaType()

            #
            # Execute the necessary context_processors
            #
            context_data = {}
            for context_processor in url_context_processors:
                context_data.update(
                    context_processor(
                        request,
                        params
                    )
                )

            #
            # Render the template with response + request + contexts_info
            #
            context_data.update(response_data)

            response = http.HttpResponseOk(
                content = self.render(template_name, context_data),
                content_type = accept[0]
            )

        response.set_cookies(cookies)

        #
        # Execute level-0 Middlewares OUT
        #
        for middleware in self.config.middleware_level0:
            middleware.process_response(request, response)

        return response


