import os
import shutil
import tempfile

import pytest

from gdocsync.html_cleaner import HTMLCleaner

from .constants import ALT_MARKUP_ASSETS, IMAGE_ASSETS, LINKS_ASSETS, MARKUP_ASSETS, MINUTES_ASSETS


@pytest.mark.parametrize(
    "test_dir",
    [
        IMAGE_ASSETS,
        MARKUP_ASSETS,
        LINKS_ASSETS,
        ALT_MARKUP_ASSETS,
        MINUTES_ASSETS,
    ],
)
def test_clean_minutes_html(test_dir: str):
    expected_path = os.path.join(test_dir, "page_clean.html")
    html_cleaner = HTMLCleaner()
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(test_dir, temp_dir, dirs_exist_ok=True)
        source_path = os.path.join(temp_dir, "page.html")
        html_cleaner(source_path, "12.34")
        with open(source_path, "rt", encoding="utf-8") as fobj:
            result = fobj.read()
    # with open(expected_path, "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    with open(expected_path, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    assert result == expected
