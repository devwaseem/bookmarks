import re

from server.apps.main.constants import REGEX_URL


def is_valid_url(url: str) -> bool:
    return bool(re.match(REGEX_URL, url))
