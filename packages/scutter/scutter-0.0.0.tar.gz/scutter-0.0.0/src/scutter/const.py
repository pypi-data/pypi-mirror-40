from typing import Union
import re

DEFAULT_ENCODING = "utf-8"
_EVENT_TYPES = ("start", "end")
_HTML = Union[bytes, str]
PATTERN = re.compile(r"\s+")
HEADERS = {"h1", "h2", "h3", "h4", "h5", "h6"}

LINK_BARRIERS = {
    "body",
    "div",
    "li",
    "ul",
    "script",
    "noscript",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
}
