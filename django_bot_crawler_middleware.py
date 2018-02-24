from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
class CrawlerBlockerMiddleware(object):
    def __init__(self,get_response=None):
        self.get_response=get_response
        print "i am in init"

    def __call__(self,request):
        print "middleware class"

        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        ip=x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        ip_cache_key="django_bot_crawler_blocker:ip_rate"+ip
        ip_hits_timeout=hasattr(settings,'IP_HITS_TIMEOUT',60)
        max_allowed_hits=hasattr(settings,'MAX_ALLOWED_HITS_PER_IP',2000)

        this_ip_hits=cache.get(ip_cache_key)

        if not this_ip_hits:
            this_ip_hits = 1
            cache.set(ip_cache_key, this_ip_hits, ip_hits_timeout)
        else:
            this_ip_hits += 1
            cache.set(ip_cache_key, this_ip_hits)
        if this_ip_hits > max_allowed_hits:
            return HttpResponseForbidden()

        else:
            response = self.get_response(request)
            print("code executed after view")
            return response
