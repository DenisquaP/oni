from webob import Response, Request
from parse import parse
import inspect
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
import os
from jinja2 import Environment, FileSystemLoader


class API:
    def __call__(self, environ: dict, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def __init__(self, templates_dir="templates"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))  # noqa 501

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def route(self, path):
        if path in self.routes:
            raise AssertionError("Such route already exists")

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)  # noqa 501
                if handler is None:
                    raise AttributeError("Method now allowed", request.method)
            handler(request, response, **kwargs)
        else:
            self.not_found(response)

        return response

    def not_found(self, response):
        response.status_code = 404
        response.text = 'Not found'
