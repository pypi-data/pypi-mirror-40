from enum import Enum
from typing import Optional, TypeVar
from time import sleep
from requests.utils import get_encodings_from_content

import requests
from selenium import webdriver

T = TypeVar("T")


def default(value: Optional[T], default_value: T) -> T:
    return value if value is not None else default_value


class EpisodeField(Enum):
    title = "title"
    episode = "episode"
    aired = "aired"
    content_rating = "content_rating"
    summary = "summary"
    directors = "directors"
    writers = "writers"
    rating = "rating"


def load_page(url: str,
              use_selenium: bool = False,
              encoding: Optional[str] = None) -> str:
    if use_selenium:
        driver = webdriver.Firefox()
        driver.get(url)
        sleep(1)
        return driver.page_source

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/60.0.3112.113 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if encoding is not None:
        response.encoding = encoding
    elif "charset" not in response.headers["content-type"]:
        encodings = get_encodings_from_content(response.text)
        if encodings:
            response.encoding = encodings[0]
    return response.text
