from django.utils.deprecation import MiddlewareMixin
import time


class DelayMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # This method is called before the view
        # You can modify the request here
        return None

    def process_response(self, request, response):
        # This method is called after the view
        # You can modify the response here
        time.sleep(0)
        return response
