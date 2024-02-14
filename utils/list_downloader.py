from requests import get
from rich import print


def download_tld_list(url) -> list:
    print(f"Downloading TLD list from {url}")
    response = get(url)

    if response.status_code == 200:
        tld_list = response.text.split("\n")
    else:
        print(
            f"[red]Failed downloading PSL from {url}! Try specifying your own list using the --tld-list argument.[/red]"
        )
        exit(1)

    return tld_list
