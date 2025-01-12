import os
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

    def __call__(self, file_path: str, prefix: str) -> None:
        with open(file_path, "rt", encoding="utf-8") as fobj:
            html_contents = fobj.read()
        tree = etree.fromstring(html_contents, cast(etree.XMLParser, etree.HTMLParser()))
        etree.strip_elements(tree, "style")
        self._fix_spans(tree)
        self._fix_links(tree)
        self._fix_headings(tree)
        self._rename_images(tree, os.path.dirname(file_path), prefix)
        html_contents = self._postprocess_html(
            etree.tostring(tree, pretty_print=True).decode("utf-8")
        )
        with open(file_path, "wt", encoding="utf-8") as fobj:
            fobj.write(html_contents)

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
            if not (link.text or "").strip(self.WHITESPACES):
                # Remove links with whitespace texts.
                # Google docs likes to insert them before actual links sometimes.
                parent = link.getparent()
                if prev := link.getprevious():
                    prev.tail = (prev.tail or "") + " "
                elif parent:
                    parent.text = (link.getparent().text or "") + " "
                if parent:
                    parent.remove(link)
                continue
            url = link.get("href")
            if url and url.startswith(self.GOOGLE_TRACKING):
                if real_url := parse_qs(urlparse(url).query).get("q", [""])[0]:
                    link.set("href", real_url)

    def _postprocess_html(self, html: str) -> str:
        return html.replace("<br/></b>", "</b><br/>")

    def _rename_images(self, tree: ElementType, dir_path: str, prefix: str) -> None:
        for idx, img in enumerate(cast(List[ElementType], tree.xpath("//img")), 1):
            image_rel_path = img.attrib["src"]
            image_rel_dir = os.path.dirname(image_rel_path)
            _, ext = os.path.splitext(image_rel_path)
            target_rel_path = f"{image_rel_dir}/{prefix}-{idx}{ext}"
            img.attrib["src"] = target_rel_path
            os.rename(
                os.path.join(dir_path, image_rel_path),
                os.path.join(dir_path, target_rel_path),
            )
