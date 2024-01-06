from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class SchemaOrgBreadCrumb:
    name: str
    item_or_url: str


@dataclass(slots=True, frozen=True)
class SchemaOrgBreadCrumbList:
    items: list[SchemaOrgBreadCrumb]

    def build_json(self) -> dict[str, Any]:
        schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index + 1,
                    "name": item.name,
                    "item": item.item_or_url,
                }
                for index, item in enumerate(self.items)
            ],
        }
        return schema
