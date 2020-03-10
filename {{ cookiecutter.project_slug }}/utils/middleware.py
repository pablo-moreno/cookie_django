class IPMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def get_request_ip(self, request):
        return request.META.get('HTTP_X_FORWARDED_FOR')[0] \
            if request.META.get('HTTP_X_FORWARDED_FOR') \
            else request.META.get('REMOTE_ADDR', None)

    def __call__(self, request, *args, **kwargs):
        ip = self.get_request_ip(request)
        setattr(request, 'ip', ip)
        response = self.get_response(request)

        return response
