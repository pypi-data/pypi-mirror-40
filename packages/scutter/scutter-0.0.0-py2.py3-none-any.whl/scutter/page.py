from scutter.models import ExtractedPage
from requests_html import HTML
from scutter.const import _HTML
from dragnet import extract_content


class PageExtractor(object):
    def __init__(self, html: _HTML, url: str):
        self.url = url
        self.html = HTML(html=html)

    @property
    def page(self):
        return ExtractedPage(
            url=self.url,
            title=self.title,
            author=self.author,
            keywords=self.keywords,
            description=self.description,
            twitter_site=self.twitter_site,
            twitter_creator=self.twitter_creator,
            twitter_image=self.twitter_image,
            twitter_description=self.twitter_description,
            og_type=self.og_type,
            og_image=self.og_image,
            og_description=self.og_description,
            content=self.content,
        )

    def get_first(self, selector):
        element = self.html.xpath(selector=selector)
        return str(element[0]) if element else None

    @property
    def title(self):
        return self.get_first("//title/text()")

    @property
    def author(self):
        return self.get_first("//meta[@name='author']/@content")

    @property
    def keywords(self):
        return self.get_first("//meta[@name='keywords']/@content")

    @property
    def description(self):
        return self.get_first("//meta[@name='description']/@content")

    @property
    def twitter_site(self):
        return self.get_first("//meta[@name='twitter:site']/@content")

    @property
    def twitter_creator(self):
        return self.get_first("//meta[@name='twitter:creator']/@content")

    @property
    def twitter_image(self):
        return self.get_first("//meta[@name='twitter:image']/@content")

    @property
    def twitter_description(self):
        return self.get_first("//meta[@name='twitter:description']/@content")

    @property
    def og_type(self):
        return self.get_first("//meta[@property='og:type']/@content")

    @property
    def og_image(self):
        return self.get_first("//meta[@property='og:image']/@content")

    @property
    def og_description(self):
        return self.get_first("//meta[@property='og:description']/@content")

    @property
    def content(self):
        return extract_content(self.html.raw_html)


def extract_page(html: _HTML, url: str) -> ExtractedPage:
    extractor = PageExtractor(html, url)
    return extractor.page
