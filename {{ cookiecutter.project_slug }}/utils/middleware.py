import json
from django.middleware.common import MiddlewareMixin


class BaseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        return request

    def process_response(self, response):
        return response

    def __call__(self, request, *args, **kwargs):
        request = self.process_request(request)
        response = self.get_response(request)
        response = self.process_response(response)

        return response


class LoggerMiddleware(BaseMiddleware):
    def __call__(self, request, *args, **kwargs):
        print(f"[{request.method}] - {getattr(request, request.method, {})}")
        print(json.dumps(getattr(request, request.method, {}), indent=4))
        return self.get_response(request)


class IPMiddleware(BaseMiddleware):
    def get_request_ip(self, request):
        return (
            request.META.get("HTTP_X_FORWARDED_FOR")
            if request.META.get("HTTP_X_FORWARDED_FOR")
            else request.META.get("REMOTE_ADDR", None)
        )

    def process_request(self, request):
        ip = self.get_request_ip(request)
        setattr(request, 'ip', ip)
        return request
