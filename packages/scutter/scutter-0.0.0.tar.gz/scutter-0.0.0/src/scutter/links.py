from typing import List
from scutter.models import ExtractedLink
from .const import (
    HEADERS,
    DEFAULT_ENCODING,
    LINK_BARRIERS,
    PATTERN,
    _HTML,
    _EVENT_TYPES,
)

from io import BytesIO
from lxml import etree


class Headers(object):
    def __init__(self):
        self.headers = [None] * 6

    def __setitem__(self, key, value):
        if value and key in HEADERS:
            index = min(max(int(key[-1]) - 1, 0), 5)
            remain = 6 - index
            self.headers = self.headers[:index] + [value] + [None] * remain

    def get(self):
        return list(filter(None, self.headers))


class LinkExtractor(object):
    def __init__(self, from_url):
        self.from_url = from_url
        self.headers = Headers()
        self.links = []
        self.clear_link()
        self.clear_header()
        self.anchor_text = None

    def clear_header(self):
        self.in_header = None
        self.header_text_collect = []

    def stash_header(self):
        self.headers[self.in_header] = self.header_text
        self.clear_header()

    def clear_link(self):
        self.is_in_link = False
        self.is_after_link = False
        self.is_after_break = False

        self.prior_text_collect = []
        self.to_url = None
        self.link_text_collect = []
        self.after_text_collect = []

    def stash_link(self):
        if self.to_url is not None:
            link = ExtractedLink(
                self.to_url,
                self.prior_text,
                self.link_text,
                self.after_text,
                self.headers.get(),
                self.anchor_text,
                self.from_url,
            )
            if link.is_valid():
                self.links.append(link)
        self.clear_link()

    def start(self, tag, attrib):
        if self.should_stash_link(tag):
            self.stash_link()

        if tag == "a":
            self.to_url = attrib.get("href", "")
            if self.to_url.startswith("#"):
                self.anchor_text = self.to_url
            else:
                self.is_in_link = True

        if tag in HEADERS:
            self.clear_header()
            self.in_header = tag

    def data(self, data):
        data = data.strip() if isinstance(data, str) else data
        if not data:
            return

        if self.is_in_link:
            self.link_text_collect.append(data)
        elif self.is_after_link:
            self.after_text_collect.append(data)
        else:
            self.prior_text_collect.append(data)

        if self.in_header:
            self.header_text_collect.append(data)

    def end(self, tag):
        self.is_after_break = tag == "br"

        if tag == "a":
            self.is_in_link = False
            self.is_after_link = True

        if tag in HEADERS:
            self.stash_header()

    @staticmethod
    def clean(str_collect):
        text = " ".join(str_collect)
        text = PATTERN.sub(" ", text).strip()
        if text:
            return text

    @property
    def prior_text(self):
        return self.clean(self.prior_text_collect)

    @property
    def link_text(self):
        return self.clean(self.link_text_collect)

    @property
    def after_text(self):
        return self.clean(self.after_text_collect)

    @property
    def header_text(self):
        return self.clean(self.header_text_collect)

    def should_stash_link(self, tag):
        return (
            (tag in LINK_BARRIERS)
            or (tag in {"a", "br"} and self.is_after_link)
            or (tag == "br" and self.is_after_break)
        )


def extract_links(html: _HTML, from_url: str = None) -> List[ExtractedLink]:
    html = html.encode(DEFAULT_ENCODING) if isinstance(html, str) else html
    html_io = BytesIO(html)
    extractor = LinkExtractor(from_url)
    for action, elem in etree.iterparse(
        html_io, events=_EVENT_TYPES, recover=True
    ):
        if action == "start":
            extractor.start(elem.tag, elem.attrib)
            extractor.data(elem.text)
        elif action == "end":
            extractor.end(elem.tag)
            extractor.data(elem.tail)

    # todo: setup loguru and this is debug mode.
    # for link in extractor.links:
    #     print(link)

    return extractor.links
