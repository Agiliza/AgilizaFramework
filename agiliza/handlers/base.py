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
from agiliza.handlers.context import ContextManager

from agiliza.views import View
class EntryView(View):
    def url_patterns(self):
        return (
            (r'^$', ''),

            (r'^list/$', 'list'),
            (r'^list/page/(?P<page>\d+)/$', 'list'),

            (r'^list/(?P<year>\d+)/$', 'list'),
            (r'^list/(?P<year>\d+)/page/(?P<page>\d+)/$', 'list'),

            (r'^list/(?P<year>\d+)/(?P<month>\d+)/$', 'list'),
            (r'^list/(?P<year>\d+)/(?P<month>\d+)/page/(?P<page>\d+)/$', 'list'),

            (r'^list/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'list'),
            (r'^list/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/page/(?P<page>\d+)/$', 'list'),

            (r'^entry/$', 'entry'),
            (r'^entry/(?P<slug>\w+)/$', 'entry'),
        )

    def get(self):
        """Most important entry list"""
        context_data = 'get'
        templates = None
        return context_data, templates

    def get_list(self, page=1):
        """Retrieve a page of full entry list"""
        context_data = 'get_list'
        templates = None
        return context_data, templates

    def post_list(self):
        """Modify entry list parameters. For example: items per page"""
        context_data = 'post_list'
        templates = None
        return context_data, templates

    def get_entry(self, slug):
        """Retrieve the entry identified by ``slug``"""
        context_data = 'get_entry'
        templates = None
        return context_data, templates

    def post_entry(self, slug):
        """Modify the entry identified by ``slug``"""
        context_data = 'post_entry'
        templates = None
        return context_data, templates

    def put_entry(self):
        """Create a new entry"""
        context_data = 'put_entry'
        templates = None
        return context_data, templates

    def delete_entry(self, slug):
        """Delete the entry identified by ``slug``"""
        context_data = 'delete_entry'
        templates = None
        return context_data, templates

class FakeRequest(object):
    def __init__(self, method, meta):
        self.method = method
        self.meta = meta


view = EntryView()

class Handler(object):
    def get_response(self, request):
        """Returns an Response object for the given Request."""
        # Locate the appropiate resource
        #view = None # TODO: Locate
        view = EntryView()
        params = {} # TODO: URL params
        response = http.HttpResponseInternalServerError()
        with ContextManager(request, params) as context:
            context_data = context.get_data()
            try:
                response = view.dispatch(**context_data)
            except Exception:
                response = http.HttpResponseInternalServerError()
        return response
