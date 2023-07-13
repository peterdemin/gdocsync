from gdocsync.html_cleaner import HTMLCleaner

from .constants import (
    ALT_MARKUP_CLEAN_HTML,
    ALT_MARKUP_SOURCE_HTML,
    CLEAN_HTML,
    MARKUP_CLEAN_HTML,
    MARKUP_SOURCE_HTML,
    SOURCE_HTML,
)


def test_clean_image_html():
    html_cleaner = HTMLCleaner()
    with open(SOURCE_HTML, "rt", encoding="utf-8") as fobj:
        source = fobj.read()
    result = html_cleaner(source)
    with open(CLEAN_HTML, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    # with open(os.path.join(IMAGE_ASSETS, "clean_result.html"), "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    assert result == expected


def test_clean_markup_html():
    html_cleaner = HTMLCleaner()
    with open(MARKUP_SOURCE_HTML, "rt", encoding="utf-8") as fobj:
        source = fobj.read()
    result = html_cleaner(source)
    with open(MARKUP_CLEAN_HTML, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    # with open(f"{MARKUP_ASSETS}/clean_result.html", "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    assert result == expected


def test_clean_alt_markup_html():
    html_cleaner = HTMLCleaner()
    with open(ALT_MARKUP_SOURCE_HTML, "rt", encoding="utf-8") as fobj:
        source = fobj.read()
    result = html_cleaner(source)
    with open(ALT_MARKUP_CLEAN_HTML, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    with open(ALT_MARKUP_CLEAN_HTML, "wt", encoding="utf-8") as fobj:
        fobj.write(result)
    assert result == expected
