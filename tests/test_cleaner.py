import os
import pytest
from gdocsync.html_cleaner import HTMLCleaner

from .constants import (
    IMAGE_ASSETS,
    MARKUP_ASSETS,
    ALT_MARKUP_ASSETS,
    MINUTES_ASSETS,
)


@pytest.mark.parametrize(
    'test_dir',
    [
        IMAGE_ASSETS,
        MARKUP_ASSETS,
        ALT_MARKUP_ASSETS,
        MINUTES_ASSETS,

    ]
)
def test_clean_minutes_html(test_dir: str):
    source_path = os.path.join(test_dir, 'page.html')
    expected_path = os.path.join(test_dir, 'page_clean.html')
    html_cleaner = HTMLCleaner()
    with open(source_path, "rt", encoding="utf-8") as fobj:
        source = fobj.read()
    result = html_cleaner(source)
    with open(expected_path, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    with open(expected_path, "wt", encoding="utf-8") as fobj:
        fobj.write(result)
    assert result == expected
