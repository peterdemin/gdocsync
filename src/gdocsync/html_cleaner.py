from typing import Iterable
from urllib.parse import parse_qs, urlparse

from lxml import etree


class HTMLCleaner:
    GOOGLE_TRACKING = "https://www.google.com/url"
    BOLD_SELECTORS = [
        '//span[@class="c1"]',
        '//span[contains(@style,"font-weight:700")]',
    ]

    def __call__(self, html_contents: str) -> str:
        htmlparser = etree.HTMLParser()
        tree = etree.fromstring(html_contents, htmlparser)
        etree.strip_elements(tree, "style")
        self._fix_spans(tree)
        self._fix_links(tree)
        return etree.tostring(tree, pretty_print=True).decode("utf-8")

    def _fix_spans(self, tree: etree.ElementTree) -> None:
        for bold_span in self._iter_bold_spans(tree):
            bold_span.tag = "b"
            bold_span.text = bold_span.text.strip()
        etree.strip_tags(tree, "span")

    def _iter_bold_spans(self, tree: etree.ElementTree) -> Iterable[etree.Element]:
        for selector in self.BOLD_SELECTORS:
            yield from tree.xpath(selector)

    def _fix_links(self, tree: etree.ElementTree) -> None:
        for link in tree.xpath("//a"):
            url = link.get("href")
            if not url or not url.startswith(self.GOOGLE_TRACKING):
                continue
            if real_url := parse_qs(urlparse(url).query).get("q", [""])[0]:
                link.set("href", real_url)
