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

import html.entities, re
 
def slugify(text, separator="-"):
    ret = ""
    for c in text.lower():
        try:
            ret += html.entities.codepoint2name[ord(c)]
        except:
            ret += c
     
    ret = re.sub("([a-zA-Z])(uml|acute|grave|circ|tilde|cedil)", r"\1", ret)
    ret = ret.strip()
    ret = re.sub(" ", "_", ret)
    ret = re.sub("\W", "", ret)
    ret = re.sub("[ _]+", separator, ret)
     
    return ret.strip()
