from lxml import etree


class HTMLCleaner:
    def __call__(self, html_contents: str) -> str:
        htmlparser = etree.HTMLParser()
        tree = etree.fromstring(html_contents, htmlparser)
        etree.strip_elements(tree, 'style')
        etree.strip_tags(tree, 'span')
        return etree.tostring(tree, pretty_print=True).decode('utf-8')
