def get_variations(tlds: list, domain_raw: str):
    for tld in tlds:
        domain = f"{domain_raw}.{tld}"
        yield domain
