# Parser exceptcions
class ParserException(Exception): pass

class AcceptHeaderException(ParserException): pass

class FormDataProcessingException(ParserException): pass


# HTTP Header exceptions
class HttpHeaderException(Exception): pass

class MethodNotAllowedException(HttpHeaderException): pass

class NotAcceptableException(HttpHeaderException): pass
