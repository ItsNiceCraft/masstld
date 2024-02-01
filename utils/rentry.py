import requests
from random import randint
from string import ascii_letters


def random_string(length=20):
    return "".join(
        [ascii_letters[randint(0, len(ascii_letters) - 1)] for _ in range(length)]
    )


def new(url, edit_code, text):
    _headers = {"Referer": "https://rentry.co"}
    session = requests.Session()
    session.headers.update(_headers)

    payload = {
        "csrfmiddlewaretoken": session.get("https://rentry.co").cookies["csrftoken"],
        "url": url,
        "edit_code": edit_code,
        "text": text,
    }

    response = session.post("https://rentry.co/api/new", data=payload)
    return response
