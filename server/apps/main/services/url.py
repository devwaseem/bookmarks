from typing import NamedTuple
from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
import structlog
import tldextract

from server.apps.main.models.bookmark import LinkType


class LinkResult(NamedTuple):
    link: str
    link_type: LinkType
    title: str


domain_link_types = {
    LinkType.VIDEO: ["youtube", "vimeo"],
    LinkType.SOCIAL_POST: ["facebook", "instagram", "twitter"],
}


logger = structlog.get_logger()

common_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def is_url_active(url: str):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers=common_headers,
        )
        if response.status_code != 404:
            return True

        # if 200 <= response.status_code < 400:
        #     return True

    except Timeout:
        return True  # if timeout, assume it exists. We would want to save this

    except Exception as error:
        logger.error(error)

    return False


def extract_title_from_url(url: str):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers=common_headers,
        )

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title from the HTML
            title_tag = soup.find("title")
            if title_tag:
                return title_tag.text.strip()

        else:
            logger.error(
                f"Unable to fetch content from {url}. Status code: {response.status_code}"
            )

    except Exception as e:
        logger.error(f"{e}")

    return None


def guess_link_type(url: str) -> LinkType:
    try:
        domain_info = tldextract.extract(url)
        domain = domain_info.domain.lower()

        for link_type, supported_domains in domain_link_types.items():
            if domain in supported_domains:
                return link_type

    except Exception:
        pass

    return LinkType.LINK
