from typing import Any, TypeVar

T = TypeVar("T", dict[str, Any], list[Any])


def clean_empty(value: T) -> T:
    if isinstance(value, dict):
        return {
            key: value
            for key, value in (
                (key, clean_empty(value)) for key, value in value.items()
            )
            if value
        }
    if isinstance(value, list):
        return [v for v in map(clean_empty, value) if v]
    return value
