from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from agiliza.net.handlers.wsgi import WSGIHandler


if __name__ == "__main__":
    httpd = make_server('', 8888, WSGIHandler())
    print("Serving on port 8888...")
    httpd.serve_forever()
