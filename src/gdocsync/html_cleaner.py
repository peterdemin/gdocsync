from typing import Iterable, List, cast
from urllib.parse import parse_qs, urlparse

from lxml import etree
from lxml.etree import _Element as ElementType


class HTMLCleaner:
    GOOGLE_TRACKING = "https://www.google.com/url"
    BOLD_SELECTORS = [
        '//span[@class="c1"]',
        '//span[contains(@style,"font-weight:700")]',
    ]
    HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
    WHITESPACES = (
        "\u0020\u00A0\u1680\u2000\u2001\u2002\u2003\u2004\u2005"
        "\u2006\u2007\u2008\u2009\u200A\u200B\u202F\u205F\u3000"
    )

    def __call__(self, html_contents: str) -> str:
        tree = etree.fromstring(html_contents, cast(etree.XMLParser, etree.HTMLParser()))
        etree.strip_elements(tree, "style")
        self._fix_spans(tree)
        self._fix_links(tree)
        self._fix_headings(tree)
        return etree.tostring(tree, pretty_print=True).decode("utf-8")

    def _fix_spans(self, tree: ElementType) -> None:
        for bold_span in self._iter_bold_spans(tree):
            bold_span.tag = "b"
            if bold_span.text:
                bold_span.text = bold_span.text.strip()
        etree.strip_tags(tree, "span")

    def _iter_bold_spans(self, tree: ElementType) -> Iterable[ElementType]:
        for selector in self.BOLD_SELECTORS:
            yield from cast(List[ElementType], tree.xpath(selector))

    def _fix_headings(self, tree: ElementType) -> None:
        """Strip whitespaces from headings"""
        for level in self.HEADINGS:
            for heading in cast(List[ElementType], tree.xpath(f"//{level}")):
                if heading.text:
                    heading.text = heading.text.strip(self.WHITESPACES)

    def _fix_links(self, tree: ElementType) -> None:
        for link in cast(List[ElementType], tree.xpath("//a")):
            if not link.text.strip(self.WHITESPACES):
                # Remove links with whitespace texts.
                # Google docs likes to insert them before actual links sometimes.
                if prev := link.getprevious():
                    prev.tail += " "
                else:
                    link.getparent().text += " "
                link.getparent().remove(link)
                continue
            url = link.get("href")
            if url and url.startswith(self.GOOGLE_TRACKING):
                if real_url := parse_qs(urlparse(url).query).get("q", [""])[0]:
                    link.set("href", real_url)
