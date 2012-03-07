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
import collections

from agiliza.resources.mapper import ResourceMapper


def method(allow, accept='text/html'):
    def info(target):
        allow_list = allow
        if isinstance(allow, str):
            allow_list = [allow, ]

        if not isinstance(allow_list, collections.Iterable):
            raise ValueError(
                "In a method, allow parameter must be iterable")

        if not isinstance(accept, str):
            raise ValueError("In a method, accept must be a string")

        target.allow = allow_list
        target.accept = accept.strip()
        return target

    return info


class ResourceMetaclass(type):
    @classmethod
    def __prepare__(cls, name, base_classes):
        return { 'method': method }

    def __new__(cls, name, bases, class_dict):
        new_resource = type.__new__(cls, name, bases, class_dict)

        mapper = ResourceMapper()
        for att_name in class_dict.keys():
            att = getattr(new_resource, att_name)
            if callable(att) and hasattr(att, 'allow'):
                mapper.add(att)

        setattr(new_resource, '_mapper', mapper)
        return new_resource
