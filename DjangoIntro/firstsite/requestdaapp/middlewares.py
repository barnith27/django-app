import time
from http.client import responses

from django.http import HttpRequest, HttpResponseForbidden


def setup_user_on_request_middleware(get_response):
    print('init call')
    def middleware(request: HttpRequest):
        print('before get')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get')
        return response
    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("request count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got',self.exceptions_count, 'exception so far')
'''
class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_last_request = {}

    def __call__(self, request):
        ip = self._ip_get(request)
        current_time = time.time()

        # Проверяем, был ли недавний запрос с этого IP
        if ip in self.ip_last_request:
            last_request_time = self.ip_last_request[ip]
            if current_time - last_request_time < 1000.0:  # 1 секунда между запросами
                return HttpResponseForbidden("Слишком частые запросы. Пожалуйста, подождите.")

        # Обновляем время последнего запроса
        self.ip_last_request[ip] = current_time

        return self.get_response(request)

    def _ip_get(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        print(f"IP адрес клиента: {ip_address}")
        return ip_address
'''