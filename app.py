import dns.resolver
from random import choice
from string import ascii_lowercase, ascii_letters
from time import time
from utils.rentry import new as rentry_new
from utils.md_generator import generate_markdown
from utils.json_generator import generate_json
from utils.get_variations import get_variations
from utils.check_domains import check_domains
from rich import print
from rich.panel import Panel
from json import dump
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("domain", help="The domain name to check TLDs for")
parser.add_argument(
    "-c",
    "--count",
    type=int,
    help="Amount of TLDs to check",
)
parser.add_argument(
    "-r",
    "--resolvers",
    action="append",
    help="Specify resolvers to use. Example: -r 1.1.1.1 -r 9.9.9.9",
)
parser.add_argument(
    "-l",
    "--tld-list",
    type=str,
    help="Path to the custom TLD list",
)
parser.add_argument(
    "-psl",
    "--use-psl",
    action="store_true",
    help="Use the Public Suffix List as the TLD list. Can't be used when a custom TLD list is used",
)
parser.add_argument(
    "--export-markdown",
    type=str,
    help="Export results to a specified markdown file",
)
parser.add_argument(
    "--export-json",
    type=str,
    help="Export results to a specified json file",
)
parser.add_argument(
    "-u",
    "--upload",
    action="store_true",
    help="Upload the results to rentry.co in markdown format",
)
args = parser.parse_args()

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)

resolvers = args.resolvers or ["9.9.9.9"]  # https://quad9.net

dns.resolver.default_resolver.nameservers = resolvers


def main():
    if args.tld_list:
        with open(args.tld_list, "r", encoding="utf8") as f:
            tlds_raw = f.readlines()
    else:
        with open(
            "lists/public_suffix_list.dat" if args.use_psl else "lists/tlds.txt",
            "r",
            encoding="utf8",
        ) as f:
            tlds_raw = f.readlines()

    tlds = []

    for tld in tlds_raw:
        if args.count:
            if len(tlds) >= args.count:
                break

        tld = tld.strip().lower()

        if tld == "":
            continue
        elif tld.startswith("//") or tld.startswith("#"):
            continue
        else:
            tlds.append(tld)

    print(
        Panel(
            f"Checking domain {args.domain} against {len(tlds)} TLDs.\nResolver: {', '.join(resolvers)}",
            title="masstld",
            border_style="blue",
        )
    )

    domains_to_check = list(get_variations(tlds, args.domain))

    available_domains, unavailable_domains, unknown_domains = check_domains(
        domains_to_check
    )

    print(
        Panel(
            f"[green]Available[/green]: {len(available_domains)}\n[red]Unavailable[/red]: {len(unavailable_domains)}\n[yellow]Unknown[/yellow]: {len(unknown_domains)}",
            title="Results",
            border_style="green",
        )
    )

    if args.upload:
        markdown = generate_markdown(
            available_domains,
            unavailable_domains,
            unknown_domains,
            args.domain,
            rentry=True,
        )
        rentry_url = f"{args.domain}-{int(time())}_{''.join(choice(ascii_lowercase) for _ in range(5))}"
        rentry_editcode = "".join(choice(ascii_letters) for _ in range(10))

        rentry_response = rentry_new(rentry_url, rentry_editcode, markdown)

        if rentry_response.status_code == 200:
            print(
                Panel(
                    f"Rentry URL: [link=https://rentry.co/{rentry_url}]https://rentry.co/{rentry_url}[/link]\nEdit code: {rentry_editcode}",
                    title="Rentry",
                    border_style="green",
                )
            )

    if args.export_markdown:
        markdown = generate_markdown(
            available_domains, unavailable_domains, unknown_domains, args.domain
        )

        with open(args.export_markdown, "w", encoding="utf8") as f:
            f.write(markdown)

    if args.export_json:
        json_data = generate_json(
            available_domains, unavailable_domains, unknown_domains, args.domain
        )

        with open(args.export_json, "w", encoding="utf8") as f:
            dump(json_data, f, indent=4)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[red]User exited[/red]")
        exit(130)
