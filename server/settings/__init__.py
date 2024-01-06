"""
This is a django-split-settings main file.
For more information read this:
https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from env import Env
from pathlib import Path

from split_settings.tools import include

# from split_settings.tools import optional
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = Env("DJANGO_ENV") or "development"


base_settings = [
    "components/common.py",
    "components/allauth.py",
    "components/database.py",
    "components/caches.py",
    "components/emails.py",
    "components/logging.py",
    "components/csp.py",
    # You can even use glob:
    # 'components/*.py'
    # Select the right env:
    f"environments/{ENV}.py",
    # Optionally override some settings:
    # optional("environments/local.py"),
]

# Include settings:
include(*base_settings)
