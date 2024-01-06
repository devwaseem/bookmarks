import os

import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

Env = environ.Env(
    # set casting, default value
    REDIS_PORT=(int, 6379),
    MJML_PORT=(int, 28101),
    DJANGO_DATABASE_PORT=(int, 5432),
    CONN_MAX_AGE=(int, 60),
    EMAIL_BACKEND=(str, "django.core.mail.backends.smtp.EmailBackend"),
    EMAIL_PORT=(int, 1025),
    LOG_FILE_DJANGO=(str, "/var/log/django/django.log"),
    LOG_FILE_SECURITY=(str, "/var/log/django/security.log"),
    LOG_FILE_APP=(str, "/var/log/django/app.log"),
    LOG_FILE_CELERY=(str, "/var/log/django/celery.log"),
)
