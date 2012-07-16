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

def url(expression, target, layouts=None,
        name=None, common_context_processors=[]):
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
        """
        If target is a String (pointing a function) or a Function
        """
        if layouts:
            """
            If url() is called with layouts
            """
            for layout_name in layouts.keys():
                urls.append(
                    (
                        create_url(layouts[layout_name]["url_prefix"] or "",
                                   expression),
                        target,
                        common_context_processors+layouts[layout_name]["context_processors"],
                        name,
                        layout_name,
                    )
                )
                
        else:
            urls.append(
                        (
                            create_url(expression),
                            target,
                            common_context_processors,
                            name,
                            None,
                        )
                    )

            
    else:
        """
        If target is a include(...)
        """
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
                            app_url[2]+common_context_processors+layouts[layout_name]["context_processors"],
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
                            app_url[2]+common_context_processors,
                            app_url[3],
                            app_url[4],
                        )
                    )
                
    return urls



def include(module_name):
    try:
        url_file = __import__(module_name)
        url_full = getattr(url_file, "url_patterns")
    
    except ImportError:
        pass
    except AttributeError:
        pass
    
    all_urls = []
    for url_list in url_full:
        all_urls = all_urls + url_list
        
    return all_urls
    
    
    
def create_url(first, second=None):
    if not first.startswith("^"):
        first = "^"+first
    
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
        return first+second
    else:
        return first
        
