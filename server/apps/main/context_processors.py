from dataclasses import asdict, dataclass

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


@dataclass(slots=True, frozen=True)
class DomainContext:
    domain_name: str
    site_name: str
    protocol: str
    base_url: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def get_site_data(request: HttpRequest):
    site = get_current_site(request)
    site_name = site.name
    domain_name = site.domain
    protocol = "https" if request.is_secure() else "http"
    base_url = f"{protocol}://{domain_name}"

    return DomainContext(
        domain_name=domain_name,
        site_name=site_name,
        protocol=protocol,
        base_url=base_url,
    ).as_dict()
