from django.http import HttpRequest, JsonResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path == '/':
            return JsonResponse({
                'ok': True,
                'msg': 'The application is ok and running.'
            })
        return self.get_response(request)
