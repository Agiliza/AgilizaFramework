class BaseHandler(object):
    def load_middleware(self):
        """Populate middleware lists from settings.MIDDLEWARE_CLASSES."""
        pass

    def get_response(self, request):
        """Returns an Response object for the given Request."""
        pass
