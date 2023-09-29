from webob import Response, Request


class API:
    def __call__(self, environ: dict, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response
