import logging
import socket

from server.settings.components.caches import CACHES
from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.csp import (
    CSP_CONNECT_SRC,
    CSP_DEFAULT_SRC,
    CSP_SCRIPT_SRC,
    CSP_STYLE_SRC,
)
from server.settings.components.logging import LOGGING


import structlog


def get_host_ip_address() -> str:
    try:
        ip_address_list = socket.gethostbyname_ex(socket.gethostname())[2]
        if len(ip_address_list) > 1:
            for ip_address in ip_address_list:
                if ip_address.startswith("192.168"):
                    return ip_address
            return ip_address_list[-1]
        return ip_address_list[0]
    except (socket.herror, socket.gaierror):
        return "127.0.0.1"


DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-47gh%z!d^2#@q(vp17ppxwg=f)iblmojmgq*j#pqs-4+@a2_yl"

BASE_URL = "http://localhost:8000"

# ALLOWED_HOSTS = [
#     "localhost",
#     "0.0.0.0",
#     "127.0.0.1",
#     "[::1]",
#     "192.168.0.155",
# ]  # noqa: S104

ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
    "django_browser_reload",
    "nplusone.ext.django",
]

CACHES["default"]["BACKEND"] = "django.core.cache.backends.dummy.DummyCache"

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# Django Browser Reload
MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

# Django Vite
DJANGO_VITE_DEV_MODE = True
DJANGO_VITE_DEV_SERVER_HOST = get_host_ip_address()
DJANGO_VITE_DEV_SERVER_PORT = 5173

# This will make debug toolbar to work with django-csp,
# since `ddt` loads some scripts from `ajax.googleapis.com`:
CSP_DEFAULT_SRC += (  # type: ignore[assignment]
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
    f"ws://{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)
CSP_SCRIPT_SRC += (  # type: ignore[assignment]
    "'self'",
    "ajax.googleapis.com",
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)
CSP_STYLE_SRC += (f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",)  # type: ignore[assignment]
CSP_CONNECT_SRC += (  # type: ignore[assignment]
    f"{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
    f"ws://{DJANGO_VITE_DEV_SERVER_HOST}:{DJANGO_VITE_DEV_SERVER_PORT}",
)

# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = [
    "nplusone.ext.django.NPlusOneMiddleware",
] + MIDDLEWARE  # noqa  # noqa: WPS440

# Logging N+1 requests:
# NPLUSONE_RAISE = True  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = structlog.getLogger("django")  # noqa
NPLUSONE_LOG_LEVEL = logging.WARN  # type:ignore
NPLUSONE_WHITELIST = [{"model": "admin.LogEntry", "field": "user"}]


LOGGING["loggers"] = {
    "django.request": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    "django.server": {
        "handlers": ["plain_console"],
        "propagate": False,
        "level": "DEBUG",
    },
    # "django.db": {
    #     "handlers": ["plain_console"],
    #     "propagate": True,
    #     "level": "DEBUG",
    # },
    "django.core.cache": {
        "handlers": ["plain_console"],
        "propagate": True,
        "level": "DEBUG",
    },
    # "django.template": {
    #     "handlers": ["plain_console"],
    #     "propagate": True,
    #     "level": "DEBUG",
    # },
    "django.security": {
        "handlers": ["plain_console"],
        "level": "WARNING",
        "propagate": False,
    },
    "celery": {
        "handlers": ["plain_console"],
        "level": "INFO",
        "propagate": False,
    },
    "server": {
        "handlers": ["plain_console"],
        "level": "DEBUG",
        "propagate": True,
    },
}

# Django CProfile
MIDDLEWARE += ["django_cprofile_middleware.middleware.ProfilerMiddleware"]
DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF = False

# Django Silk
# INSTALLED_APPS += ["silk"]
# MIDDLEWARE += ("silk.middleware.SilkyMiddleware",)

# dbbackup
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": "./data"}
