from env import Env

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": Env("POSTGRES_DB"),
        "USER": Env("POSTGRES_USER"),
        "PASSWORD": Env("POSTGRES_PASSWORD"),
        "HOST": Env("DJANGO_DATABASE_HOST"),
        "PORT": Env("DJANGO_DATABASE_PORT", int, 5432),
        "CONN_MAX_AGE": Env("CONN_MAX_AGE", int, 60),
        "OPTIONS": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000ms",
        },
    },
}
