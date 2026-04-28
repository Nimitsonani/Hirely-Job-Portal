from django.http import HttpResponse
from django_redis import get_redis_connection
import time
import uuid


redis_conn = get_redis_connection("default")
LIMIT = 50


class RateLimiting:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        current_time = time.time()
        def limit(key):
            redis_conn.zremrangebyscore(key, 0, current_time-60)
            req_in_minute = len(redis_conn.zrange(key,0,-1))
            redis_conn.zadd(key,{str(uuid.uuid4()):current_time})
            if LIMIT < req_in_minute+1:
                return HttpResponse('Rate Limit')
            return self.get_response(request)

        if request.user.is_authenticated:
            user_id = request.user.id
            response = limit(user_id)
        else:
            ip_address = request.META.get('REMOTE_ADDR')
            response = limit(ip_address)
        return response