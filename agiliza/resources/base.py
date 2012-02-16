import collections

from agiliza.net import http
from agiliza.net.http.exceptions import (MethodNotAllowedException,
    NotAcceptableException)
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

class Resource(metaclass=ResourceMetaclass):
    def dispatch(self, request, *args, **kwargs):
        allow_list = self._mapper.allow_methods()
        if not request.method in allow_list:
            return http.HttpResponseMethodNotAllowed(allow_list)

        accept = sorted([ (q, t) for t, q in request.accept.items() ],
            reverse=True)
        accept_list = tuple(map(lambda x: x[1], accept))
        try:
            method = self._mapper.find(request.method, accept_list)
            response = method(self, request, *args, **kwargs) # TODO classmethod for methods?
        except MethodNotAllowedException:
            response = http.HttpResponseMethodNotAllowed(allow_list)
        except NotAcceptableException as exception:
            # TODO HTTP Content Negotiation
            response = http.HttpResponseNotAcceptable()

        # TODO warning if response.content_type is not in method.accept
        return response

    def get_filestorage(self):
        '''
            Debería buscar si la vista tiene asociado algún filestorage.
            En caso de no tenerlo, se debería buscar en la aplicación y
            si no, en el proyecto. <-- ¿Cómo localizar la aplicación?
        '''
        pass # TODO
