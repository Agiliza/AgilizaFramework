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


Copyright (c) 2012 Alvaro Hurtado <alvarohurtado84@gmail.com>
"""
import unittest
import sys

from agiliza.urls import include
from agiliza.urls import url
from agiliza.urls import create_url

from agiliza.urls.exceptions import NoneNameException, \
    UrlFileNotFoundException, UrlPatternsNotFoundException

from tests.mocks.utils import NiceDict



class StringOrFunctionTargetUrlTest(unittest.TestCase):

    def test_create_url(self):
        created_url = url("", "blog.controller.home", name="one" )

        self.assertEqual(
            created_url,
            [("^$", "blog.controller.home", [], "one", None),],
            msg="URL do not create a simple url tuple"
        )

    def test_create_url_with_none_name(self):

        with self.assertRaises(
            NoneNameException,
            msg="URL without a include method as target can not have a \
                None name or empty Name"
        ):
            created_url = url("", "blog.controller.home",)

    def test_create_url_with_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            context_processors=["menu", "users"]
        )

        self.assertEqual(
            set(created_url[0][2]),
            set(["menu", "users"]),
            msg="URL do not create a url with context_processors"
        )

    def test_create_url_with_one_layout_without_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":"blog/",
                    "context_processors":[],
                },
            }
        )

        self.assertEqual(
            created_url,
            [("^blog/$", "blog.controller.home", [], "one", "default")],
            msg="URL do not create a url with one layout without \
                context_processors"
        )

    def test_create_url_with_one_layout(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":"blog/",
                    "context_processors":["menu", "users"],
                },
            }
        )

        self.assertEqual(
            set(created_url[0][2]),
            set(["menu", "users"]),
            msg="URL do not create a url with full layout"
        )

    def test_create_url_with_multiple_layouts_without_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":None,
                    "context_processors":[],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":[],
                }
            }
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^$", "blog.controller.home", [], "one", "default"),
                ("^android/$", "blog.controller.home", [], "one", "android")
            ]),
            msg="URL do not create a url with multiple layouts without \
                context_processors"
        )

    def test_create_url_with_multiple_layouts_with_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":None,
                    "context_processors":[],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":[],
                }
            },
            context_processors=["menu", "users"],
        )

        self.assertEqual(
            set(created_url[0][2]),
            set(["menu", "users"]),
            msg="URL do not add common context processors to the first URL"
        )

        self.assertEqual(
            set(created_url[1][2]),
            set(["menu", "users"]),
            msg="URL do not add common context processors to the second URL"
        )

    def test_create_url_with_multiple_layouts_with_custom_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":None,
                    "context_processors":["menu", "users"],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":["mobile"],
                }
            },
        )

        if created_url[0][4] is "default":
            self.assertEqual(
                set(created_url[0][2]),
                set(["menu", "users"]),
                msg="URL do not add custom context processors to the first URL"
            )

            self.assertEqual(
                set(created_url[1][2]),
                set(["mobile"]),
                msg="URL do not add custom context processors to the second URL"
            )
        else:
            self.assertEqual(
                set(created_url[1][2]),
                set(["menu", "users"]),
                msg="URL do not add custom context processors to the first URL"
            )

            self.assertEqual(
                set(created_url[0][2]),
                set(["mobile"]),
                msg="URL do not add custom context processors to the second URL"
            )

    def test_create_url_with_multiple_layouts_with_custom_and_context_processors(self):
        created_url = url(
            "",
            "blog.controller.home",
            name="one",
            layouts={
                "default":{
                    "url_prefix":None,
                    "context_processors":["menu", "users"],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":[],
                }
            },
            context_processors=["common", "context"]
        )

        if created_url[0][4] is "default":
            self.assertEqual(
                set(created_url[0][2]),
                set(["menu", "users", "common", "context"]),
                msg="URL do not add custom context processors to the first URL"
            )

            self.assertEqual(
                set(created_url[1][2]),
                set(["common", "context"]),
                msg="URL do not add custom context processors to the second URL"
            )
        else:
            self.assertEqual(
                set(created_url[1][2]),
                set(["menu", "users", "common", "context"]),
                msg="URL do not add custom context processors to the first URL"
            )

            self.assertEqual(
                set(created_url[0][2]),
                set(["common", "context"]),
                msg="URL do not add custom context processors to the second URL"
            )
            
    def test_create_url_method(self):
        self.assertEqual(
            create_url("^url/"),
            "^url/$",
            msg="CreateUrl with one word must starts with '^' and finish with \
                '$'")
        

class IncludeTargetUrlTest(unittest.TestCase):

    def test_from_include(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "one", None),
                ("^post/$", "blog.controller.post", [], "two", None),
            ]
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^blog/$", "blog.controller.home", [], "one", None),
                ("^blog/post/$", "blog.controller.post", [], "two", None),
            ]),
            msg="URL do not create good urls from include"
        )

    def test_from_include_with_names(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "get", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ]
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^blog/$", "blog.controller.home", [], "get", None),
                ("^blog/post/$", "blog.controller.post", [], "post", None),
            ]),
            msg="URL do not create good urls from include with names"
        )


    def test_from_include_with_context_processors(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            context_processors=["menu", "users"],
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^blog/$", "blog.controller.home", ["menu", "users"], "home", None),
                ("^blog/post/$", "blog.controller.post", ["menu", "users"], "post", None),
            ]),
            msg="URL do not create good urls with common context processors"
        )


    def test_from_include_with_one_layout_without_context_processors(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                    "url_prefix":"myweb/",
                    "context_processors":[],
                },
            }
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^myweb/blog/$", "blog.controller.home", [], "home", "default"),
                ("^myweb/blog/post/$", "blog.controller.post", [], "post", "default"),
            ]),
            msg="URL do not create good urls from include with layout \
                without context_processors"
        )

    def test_from_include_with_one_layout(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                    "url_prefix":"myweb/",
                    "context_processors":["menu", "users"],
                },
            }
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^myweb/blog/$", "blog.controller.home", ["menu", "users"], "home", "default"),
                ("^myweb/blog/post/$", "blog.controller.post", ["menu", "users"], "post", "default"),
            ]),
            msg="URL do not create good urls from include with layout"
        )

    def test_from_include_with_one_layout_without_context_processors(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                    "url_prefix":"myweb/",
                    "context_processors":[],
                    },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":[],
                }
            }
        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^myweb/blog/$", "blog.controller.home", [], "home", "default"),
                ("^myweb/blog/post/$", "blog.controller.post", [], "post", "default"),
                ("^android/blog/$", "blog.controller.home", [], "home", "android"),
                ("^android/blog/post/$", "blog.controller.post", [], "post", "android"),
            ]),
            msg="URL do not create good urls from include with several \
                layouts without context_processors"
        )

    def test_from_include_with_multiple_layouts(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                    "url_prefix":"myweb/",
                    "context_processors":["users", "menu"],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":["mobile"],
                }
            }

                        )

        self.assertEqual(
            sorted(created_url),
            sorted([
                ("^myweb/blog/$", "blog.controller.home", ["users", "menu"], "home", "default"),
                ("^myweb/blog/post/$", "blog.controller.post", ["users", "menu"], "post", "default"),
                ("^android/blog/$", "blog.controller.home", ["mobile"], "home", "android"),
                ("^android/blog/post/$", "blog.controller.post", ["mobile"], "post", "android"),
            ]),
            msg="URL do not create good urls from include with several layouts"
        )


    def test_from_include_with_multiple_layouts_with_context_processors(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                    "url_prefix":"myweb/",
                    "context_processors":[],
                },
                "android":{
                    "url_prefix":"android/",
                    "context_processors":[],
                }
            },
            context_processors=["menu", "users"],
        )

        for url_i in created_url:
            self.assertEqual(
                set(url_i[2]),
                set(["menu", "users"]),
                msg="URL do not add common context processors to all URL"
            )


    def test_from_include_with_multiple_layouts_with_common_and_custom_context_processors(self):
        created_url = url(
            "blog/",
            [
                ("^$", "blog.controller.home", [],  "home", None),
                ("^post/$", "blog.controller.post", [], "post", None),
            ],
            layouts={
                "default":{
                "url_prefix":"myweb/",
                "context_processors":["menu", "users"],
                },
                "android":{
                "url_prefix":"android/",
                "context_processors":[],
                }
            },
            context_processors=["common", "context"],
        )

        for url_i in created_url:
            if url_i[4] is "default":
                self.assertEqual(
                    set(url_i[2]),
                    set(["menu", "users", "common", "context"]),
                    msg="URL do not add common context processors to all URL"
                )
            else:
                self.assertEqual(
                    set(url_i[2]),
                    set(["common", "context"]),
                    msg="URL do not add common context processors to all URL"
                )


class IncludeUrlTest(unittest.TestCase):
    def virtual_include(self, dict):
        self.mock_urls = NiceDict(dict)
    
    def test_include_with_empty_urlpatterns(self):
        self.virtual_include({"url_patterns":()})
        
        sys.modules.setdefault('my_project.urls', self.mock_urls)
        include_results = include('my_project.urls')
        
        self.assertEqual(
            set([]),
            set(include_results),
            msg="Include must return a list of tuples of Urls."
        )
        sys.modules.pop('my_project.urls')
    
    def test_include_basic(self):
        self.virtual_include({"url_patterns":(
            [("/exp1", "target.function", (), "function", None)],
            )
        })
        sys.modules.setdefault('my_project.urls', self.mock_urls)
        include_results = include('my_project.urls')
        
        self.assertEqual(
            set([("/exp1", "target.function", (), "function", None)]),
            set(include_results),
            msg="Include must return a list of tuples of Urls."
        )
        sys.modules.pop('my_project.urls')
        
    def test_include_two_urls_in_two_list(self):
        self.virtual_include({"url_patterns":(
            [("/exp1", "target.function", (), "function", None)],
            [("/exp2", "target.function2", (), "function2", None)]
            )
        })
        sys.modules.setdefault('my_project.urls', self.mock_urls)
        
        include_results = include('my_project.urls')
        
        self.assertEqual(
            set([("/exp1", "target.function", (), "function", None),
                ("/exp2", "target.function2", (), "function2", None)]),
            set(include_results),
            msg="Include must return a list of tuples of Urls when it has \
                two list with one url."
        )
        sys.modules.pop('my_project.urls')
    
    def test_include_two_urls_in_one_list(self):
        self.virtual_include({"url_patterns":(
            [("/exp1", "target.function", (), "function", None),
            ("/exp2", "target.function2", (), "function2", None)],
            )
        })
        sys.modules.setdefault('my_project.urls', self.mock_urls)
        include_results = include('my_project.urls')
        
        self.assertEqual(
            set([("/exp1", "target.function", (), "function", None),
                ("/exp2", "target.function2", (), "function2", None)]),
            set(include_results),
            msg="Include must return a list of tuples of Urls when it has \
                a list with two urls."
        )
        sys.modules.pop('my_project.urls')
        
    def test_include_with_several_urls(self):
        self.virtual_include({"url_patterns":(
            [("/exp1", "target.function", (), "function", None),
                ("/exp2", "target.function2", (), "function2", None)],
            [("/exp3", "target.function3", (), "function3", None)],
            [("/exp7", "target.function7", (), "function7", None),
                ("/exp5", "target.function5", (), "function5", None)],
            [("/exp6", "target.function6", (), "function6", None)],
            )
        })
        sys.modules.setdefault('my_project.urls', self.mock_urls)
        include_results = include('my_project.urls')
        
        self.assertEqual(
            set([("/exp1", "target.function", (), "function", None),
                ("/exp2", "target.function2", (), "function2", None),
                ("/exp3", "target.function3", (), "function3", None),
                ("/exp7", "target.function7", (), "function7", None),
                ("/exp6", "target.function6", (), "function6", None),
                ("/exp5", "target.function5", (), "function5", None)]),
            set(include_results),
            msg="Include must return a list of tuples of Urls when it has\
                several urls in several lists."
        )
        sys.modules.pop('my_project.urls')
        
    def test_include_must_fail_with_not_existing_module(self):
        with self.assertRaises(UrlFileNotFoundException,
                          msg="Include is importin something not existing."):
            include('my_project.urls.not_exist')
                          
        
    def test_include_must_fail_without_urlpatterns(self):
        self.virtual_include({"u":()})
        sys.modules.setdefault('my_project.urls', self.mock_urls)

        with self.assertRaises(UrlPatternsNotFoundException,
            msg="Include must raise Exception if urls does not contain \
                url_patterns."
        ):
            include('my_project.urls')
        
        sys.modules.pop('my_project.urls')


if __name__ == '__main__':
    unittest.main()
