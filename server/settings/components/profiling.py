from env import Env
from server.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)

DJANGO_ENABLE_PROFILING = Env("DJANGO_ENABLE_PROFILING", bool, False)

if DJANGO_ENABLE_PROFILING:
    # Django Silk
    INSTALLED_APPS += ["silk"]
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
    SILKY_PYTHON_PROFILER = True
