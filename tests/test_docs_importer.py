import os
import logging
from unittest import mock
import tempfile

import pytest

from gdocsync.docs_importer import DocsImporter
from gdocsync.google_drive_client import DriveClient, DriveFile
from gdocsync.pandoc_client import PandocClient
from gdocsync.html_cleaner import HTMLCleaner

HERE = os.path.dirname(__file__)
TEST_ASSETS = os.path.join(HERE, "assets")
SOURCE_HTML_BUNDLE = os.path.join(TEST_ASSETS, "html_bundle.zip")
EXPECTED_RST = os.path.join(TEST_ASSETS, "imported.rst")
CATEGORY_DIR = '13_category'


def test_import_sample_html_bundle(drive_client: DriveClient):
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
        result_file = os.path.join(temp_dir, CATEGORY_DIR, '68-name.rst')
        assert os.path.exists(result_file)
        with open(result_file, 'rt', encoding='utf-8') as fobj:
            result = fobj.read()
        with open(EXPECTED_RST, 'rt', encoding='utf-8') as fobj:
            expected = fobj.read()
        assert result == expected


@pytest.fixture(name='drive_client')
def load_drive_client() -> mock.Mock:
    drive_client = mock.Mock(spec_set=DriveClient)
    drive_client.list_files.return_value = [
        DriveFile(drive_id="drive_id", name="[13.68] - Name")
    ]
    with open(SOURCE_HTML_BUNDLE, 'rb') as fobj:
        drive_client.download_doc.return_value = fobj.read()
    return drive_client
