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
class SingletonMetaClass(type):
    def __init__(cls,name,bases,dic):
        super(SingletonMetaClass, cls).__init__(name, bases, dic)
        cls._singleton_instance = None

    def __call__(cls,*args,**kw):
        if cls._singleton_instance is None:
            cls._singleton_instance = \
                super(SingletonMetaClass, cls).__call__(*args, **kw)
        return cls._singleton_instance

class Singleton(metaclass=SingletonMetaClass):
    pass


class NiceDict(dict):
    def __getattr__(self, key):
        if key not in self.keys():
            return super(NiceDict, self).__getattr__(key)
        return self[key]

    def __setattr__(self, key, value):
        if key not in self.keys():
            return super(NiceDict, self).__setattr__(key, value)
        self[key] = value
