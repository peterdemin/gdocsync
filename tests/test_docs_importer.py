import logging
import os
import tempfile
from unittest import mock

import pytest

from gdocsync.docs_importer import DocsImporter
from gdocsync.google_drive_client import DriveClient, DriveFile
from gdocsync.html_cleaner import HTMLCleaner
from gdocsync.pandoc_client import PandocClient

from .constants import IMAGE_ASSETS, LINKS_ASSETS, MARKUP_ASSETS, MINUTES_ASSETS

CATEGORY_DIR = "13_category"


@pytest.mark.parametrize(
    "test_dir",
    [
        IMAGE_ASSETS,
        MARKUP_ASSETS,
        LINKS_ASSETS,
        MINUTES_ASSETS,
    ],
)
def test_import_sample_html_bundle(test_dir: str):
    source_path = os.path.join(test_dir, "html_bundle.zip")
    expected_path = os.path.join(test_dir, "imported.rst")
    drive_client = load_drive_client(source_path)
    pandoc_client = PandocClient()
    logger = mock.Mock(spec_set=logging.Logger)
    docs_importer = DocsImporter(
        drive_client=drive_client,
        pandoc_client=pandoc_client,
        logger=logger,
        html_cleaner=HTMLCleaner(),
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(os.path.join(temp_dir, CATEGORY_DIR))
        docs_importer(temp_dir)
        result_file = os.path.join(temp_dir, CATEGORY_DIR, "68-name.rst")
        assert os.path.exists(result_file)
        with open(result_file, "rt", encoding="utf-8") as fobj:
            result = fobj.read()
        # with open(expected_path, "wt", encoding="utf-8") as fobj:
        #     fobj.write(result)
        with open(expected_path, "rt", encoding="utf-8") as fobj:
            expected = fobj.read()
        assert result == expected


def load_drive_client(html_bundle_path: str) -> mock.Mock:
    drive_client = mock.Mock(spec_set=DriveClient)
    drive_client.list_files.return_value = [DriveFile(drive_id="drive_id", name="[13.68] - Name")]
    with open(html_bundle_path, "rb") as fobj:
        drive_client.download_doc.return_value = fobj.read()
    return drive_client
