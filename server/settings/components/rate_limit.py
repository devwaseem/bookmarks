from django.conf import settings

from server.apps.main.helpers.network import get_ip_from_request

RATELIMIT_USE_CACHE = settings.RATE_LIMIT_CACHE_BACKEND


def RATELIMIT_IP_META_KEY(request):
    return get_ip_from_request(request=request)
