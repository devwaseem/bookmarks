from dataclasses import asdict, dataclass

from django.http import HttpRequest


@dataclass(slots=True, frozen=True)
class DomainContext:
    domain_name: str
    site_name: str
    protocol: str
    base_url: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def get_domain_context_from_request(request: HttpRequest) -> DomainContext:
    # site = ...
    # site_name = site.site_name
    # hostname = site.hostname
    # port = site.port
    # domain_name = hostname
    # if port and port != 80:
    #     domain_name += ":" + str(port)
    # protocol = "https" if request.is_secure() else "http"
    # base_url = f"{protocol}://{domain_name}"
    #
    # return DomainContext(
    #     domain_name=domain_name,
    #     site_name=site_name,
    #     protocol=protocol,
    #     base_url=base_url,
    # )
    raise NotImplementedError()
