import dns
from rich import print


def check_domains(domains: list):
    available_domains = []
    unavailable_domains = []
    unknown_domains = []

    def domain_available(domain: str):
        available_domains.append(domain)
        print(f"[bold green][✓][/bold green] {domain}")

    def domain_unavailable(domain: str):
        unavailable_domains.append(domain)
        print(f"[bold red][X][/bold red] {domain}")

    def domain_unknown(domain: str):
        unknown_domains.append(domain)
        print(f"[yellow][?][/yellow] {domain}")

    for domain in domains:
        try:
            dns.resolver.resolve(domain, "NS")
        except dns.resolver.NXDOMAIN:
            domain_available(domain)
        except dns.resolver.NoAnswer:
            domain_unknown(domain)
        except dns.resolver.NoNameservers:
            domain_unknown(domain)
        except dns.resolver.LifetimeTimeout:
            domain_unknown(domain)
        else:
            domain_unavailable(domain)

    return available_domains, unavailable_domains, unknown_domains
