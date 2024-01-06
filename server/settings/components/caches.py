from env import Env

# Caching
# https://docs.djangoproject.com/en/3.2/topics/cache/


REDIS_HOST = Env("REDIS_HOST")
REDIS_PORT = Env("REDIS_PORT")

RATE_LIMIT_CACHE_BACKEND = "ratelimiting"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    },
    RATE_LIMIT_CACHE_BACKEND: {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    },
}
