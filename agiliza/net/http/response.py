import abc


class HttpResponse(metaclass=abc.ABCMeta):
    """
    A basic HTTP response, with content and dictionary-accessed headers.
    """
    @abc.abstractproperty
    def status_code(self):
        pass

    @abc.abstractproperty
    def status_text(self):
        pass

    @property
    def status(self):
        return '%s %s' % (self.status_code, self.status_text)
