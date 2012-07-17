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
import importlib

from agiliza.config.exceptions import (UrlNoneNameException,
    UrlFileNotFoundException, UrlPatternsNotFoundException)


def url(expression, target, name=None, layouts=None, context_processors=[]):
    """
    Create a list of urls.
    Must return one of these:
        * [
            (
            'regular expression',
            "target.function",
            [context_processor1, context_processor2] or [],
            'name' or None,
            'layout_name' or None),

            (),
        ...]
    """
    urls=[]

    if isinstance(target, str) or callable(target):
        if name is None or name is "":
            raise UrlNoneNameException("Name can not be None if target is not \
                                    a include method.")
        # if target is a String (pointing a function) or a Function
        if layouts:
            # if url() is called with layouts
            for layout_name in layouts.keys():
                urls.append(
                    (
                        create_url(
                            layouts[layout_name]["url_prefix"] or "",
                            expression
                        ),
                        target,
                        context_processors + \
                            layouts[layout_name]["context_processors"],
                        name,
                        layout_name,
                    )
                )

        else:
            urls.append(
                (
                    create_url(expression),
                    target,
                    context_processors,
                    name,
                    None,
                )
            )


    else:
        # if target is a include(...)
        if layouts:

            for layout_name in layouts:
                for app_url in target:
                    urls.append(
                        (
                            create_url(
                                create_url(
                                    layouts[layout_name]["url_prefix"] or "",
                                    expression),
                                app_url[0]
                            ),
                            app_url[1],
                            app_url[2] + \
                                context_processors + \
                                layouts[layout_name]["context_processors"],
                            app_url[3],
                            layout_name,
                        )
                    )


        else:

            for app_url in target:
                urls.append(
                    (
                        create_url(expression, app_url[0]),
                        app_url[1],
                        app_url[2] + context_processors,
                        app_url[3],
                        app_url[4],
                    )
                )

    return urls



def include(module_name):
    try:
        url_module = importlib.import_module(module_name)
        url_patterns = getattr(url_module, 'url_patterns')
    except ImportError:
        raise UrlFileNotFoundException("URLs file not found.")
    except AttributeError:
        raise UrlPatternsNotFoundException("URLs file do not contains an url_patterns.")

    urls = []
    for url_list in url_patterns:
        urls = urls + url_list

    return urls





def create_url(first, second=None):
    if not first.startswith("^"):
        first = "^" + first

    if second:
        if first.endswith("$"):
            first = first[:-1]
        if second.startswith("^"):
            second = second[1:]
        if not second.endswith("$"):
            second = second + "$"
    else:
        if not first.endswith("$"):
            first = first + "$"

    if second:
        return first + second
    else:
        return first
