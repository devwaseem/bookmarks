# REDIS_HOST = Env("REDIS_HOST")
# REDIS_PORT = Env("REDIS_PORT")
#
# CELERY_BROKER_URL = Env("CELERY_BROKER_URL") or f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
# CELERY_RESULT_BACKEND = (
#     Env("CELERY_RESULT_BACKEND") or f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
# )
# CELERY_IMPORTS = ("server.apps.main.tasks",)
