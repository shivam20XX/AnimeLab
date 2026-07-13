import re


def clean_description(description):
    if not description:
        return ""

    description = re.sub(
        r"<[^>]+>",
        "",
        description,
    )

    return description