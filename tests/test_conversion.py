import os
import shutil
import tempfile

from gdocsync.pandoc_client import PandocClient

from .constants import (
    CLEAN_HTML,
    CONVERTED_RST,
    IMAGES_DIR,
    MARKUP_CLEAN_HTML,
    MARKUP_CONVERTED_RST,
)


def test_html_bundle_with_image_to_rst_conversion():
    pandoc_client = PandocClient()
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(IMAGES_DIR, os.path.join(temp_dir, "images"))
        result_path = os.path.join(temp_dir, "output.rst")
        pandoc_client.html_to_rst(CLEAN_HTML, result_path)
        with open(result_path, "rt", encoding="utf-8") as fobj:
            result = fobj.read()
    # with open(CONVERTED_RST, "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    with open(CONVERTED_RST, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    assert result == expected


def test_html_bundle_with_markup_to_rst_conversion():
    pandoc_client = PandocClient()
    with tempfile.TemporaryDirectory() as temp_dir:
        result_path = os.path.join(temp_dir, "output.rst")
        pandoc_client.html_to_rst(MARKUP_CLEAN_HTML, result_path)
        with open(result_path, "rt", encoding="utf-8") as fobj:
            result = fobj.read()
    # with open(MARKUP_CONVERTED_RST, "wt", encoding="utf-8") as fobj:
    #     fobj.write(result)
    with open(MARKUP_CONVERTED_RST, "rt", encoding="utf-8") as fobj:
        expected = fobj.read()
    assert result == expected
