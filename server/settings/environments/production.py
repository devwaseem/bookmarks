import re

from server.settings.components.logging import LOGGING
from server.settings.components.common import INSTALLED_APPS
from env import Env
from server.settings.components.csp import (
    CSP_CONNECT_SRC,
    CSP_FONT_SRC,
    CSP_IMG_SRC,
    CSP_MEDIA_SRC,
    CSP_SCRIPT_SRC,
    CSP_STYLE_SRC,
)

DEBUG = False

SECRET_KEY = Env("SECRET_KEY")

INSTALLED_APPS += ["storages"]

BASE_URL = Env("DOMAIN_NAME")

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

ALLOWED_HOSTS = Env("DJANGO_ALLOWED_HOSTS", default="").split()
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
# SECURE_HSTS_SECONDS = 86400  # 1 day
SECURE_HSTS_SECONDS = 300  # 5 Minutes
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = Env("CSRF_TRUSTED_ORIGINS", default="").split()

MEDIA_URL = "/media"

# whitenoise
STATICFILES_STORAGE = "whitenoise.storage.ManifestStaticFilesStorage"
STATIC_HOST = Env("DJANGO_STATIC_HOST", str, "")
STATIC_URL = STATIC_HOST + "/static/"
STATIC_ROOT = "/var/www/static"


def immutable_file_test(_, url):
    # Match filename with 12 hex digits before the extension
    # e.g. app.db8f2edc0c8a.js
    return re.match(r"^.+\.\w+\..+$", url)


WHITENOISE_IMMUTABLE_FILE_TEST = immutable_file_test


# Django Vite
DJANGO_VITE_DEV_MODE = False
# DJANGO_VITE_MANIFEST_PATH = DJANGO_VITE_ASSETS_PATH / "manifest.json"

# Configure CSP to work with AWS s3

CSP_SCRIPT_SRC += (STATIC_URL,)
CSP_CONNECT_SRC += (
    STATIC_URL,
    MEDIA_URL,
)
CSP_MEDIA_SRC += (
    STATIC_URL,
    MEDIA_URL,
)
CSP_FONT_SRC += (STATIC_URL,)
CSP_IMG_SRC += (
    STATIC_URL,
    MEDIA_URL,
)
CSP_STYLE_SRC += (STATIC_URL,)

# Logging
LOGGING["handlers"].update(  # type: ignore[attr-defined]
    {
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_DJANGO"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "django_security_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_SECURITY"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "app_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_APP"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
        "celery_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Env("LOG_FILE_CELERY"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "console",
        },
    }
)
LOGGING["loggers"] = {
    "django.server": {
        "handlers": ["django_file", "mail_admins"],
        "propagate": True,
        "level": "INFO",
    },
    "django.security": {
        "handlers": ["django_security_file", "mail_admins"],
        "level": "WARNING",
        "propagate": True,
    },
    "celery": {
        "handlers": ["celery_file", "mail_admins"],
        "level": "INFO",
        "propagate": True,
    },
    "src": {
        "handlers": ["app_file", "mail_admins"],
        "level": "INFO",
        "propagate": True,
    },
}
