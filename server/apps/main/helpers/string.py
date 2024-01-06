def unique_split(string: str, *, delimiter: str) -> list[str]:
    return list(
        set(
            filter(
                lambda value: value != "",
                map(str.strip, string.rstrip(delimiter).split(delimiter)),
            ),
        ),
    )


def mark_as_strong_for(value: str, replacing_str: str) -> str:
    """Add strong tag for the selected substring."""
    from_index = value.lower().find(replacing_str.lower())
    if from_index >= 0:
        # subst found
        to_index = from_index + len(replacing_str)
        return (
            value[:from_index]  # noqa: W503
            + "<strong>"  # noqa: W503
            + value[from_index:to_index]  # noqa: W503
            + "</strong>"  # noqa: W503
            + value[to_index:]  # noqa: W503
        )

    return value
