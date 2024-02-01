def generate_json(
    available_domains: list,
    unavailable_domains: list,
    unknown_domains: list,
    domain: str,
):
    data = {
        "domain": domain,
        "available_domains": available_domains,
        "unavailable_domains": unavailable_domains,
        "unknown_domains": unknown_domains,
    }

    return data
