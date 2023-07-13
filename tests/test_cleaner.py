import os

from gdocsync.html_cleaner import HTMLCleaner

HERE = os.path.dirname(__file__)
TEST_ASSETS = os.path.join(HERE, "assets")
SOURCE_HTML = os.path.join(TEST_ASSETS, "page.html")
EXPECTED_HTML = os.path.join(TEST_ASSETS, "page_clean.html")


def test_clean_sample_html():
    html_cleaner = HTMLCleaner()
    with open(SOURCE_HTML, "rt", encoding="utf-8") as fobj:
        source = fobj.read()
    result = html_cleaner(source)
    with open(EXPECTED_HTML, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    # with open(os.path.join(TEST_ASSETS, "clean_result.html"), "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    assert result == expected
