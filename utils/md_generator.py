from mdutils.mdutils import MdUtils
from itertools import zip_longest
from datetime import datetime as dt


def generate_markdown(
    available_domains: list,
    unavailable_domains: list,
    unknown_domains: list,
    domain: str,
    rentry: bool = False,
):
    mdFile = MdUtils(
        file_name="output",
        title=f"[masstld](https://github.com/ItsNiceCraft/masstld) results for {domain}",
    )

    mdFile.new_line(f"Generated on {dt.today().strftime('%Y-%m-%d %H:%M:%S')}")

    headers = ["Available", "Unavailable", "Unknown"]

    content = list(
        zip_longest(
            available_domains, unavailable_domains, unknown_domains, fillvalue=""
        )
    )

    flat_content = [item for sublist in [headers] + content for item in sublist]

    mdFile.new_table(columns=3, rows=len(content) + 1, text=flat_content)

    if rentry:
        mdFile.new_line(
            "[comment]: <> (SUPPORT-RENTRY-PATREON)"
        )  # this removes ads on the rentry page, see https://rentry.co/x9dq79#potential-solution

    return mdFile.get_md_text()
