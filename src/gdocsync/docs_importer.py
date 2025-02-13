import glob
import io
import logging
import os
import shutil
import tempfile
import zipfile

from .constants import CACHE_FILE_NAME
from .google_drive_client import DriveClient, DriveFile, GoogleAuth
from .html_cleaner import HTMLCleaner
from .johnny_decimal import JohnnyDecimal
from .pandoc_client import PandocClient
from .shelve_cache import ShelveCache


class DocsImporter:
    PDF_EXPORT_DIR = "_static"

    def __init__(
        self,
        pandoc_client: PandocClient,
        drive_client: DriveClient,
        logger: logging.Logger,
        html_cleaner: HTMLCleaner,
    ) -> None:
        self._pandoc_client = pandoc_client
        self._drive_client = drive_client
        self._logger = logger
        self._html_cleaner = html_cleaner

    def __call__(self, base_dir: str) -> None:
        for drive_file in self._drive_client.list_files():
            if JohnnyDecimal.is_valid(drive_file.name):
                self._import_drive_file(drive_file, base_dir)
            else:
                self._maybe_update_pdf(drive_file, base_dir)

    def _maybe_update_pdf(self, drive_file: DriveFile, base_dir: str) -> None:
        target_path = os.path.join(
            base_dir, self.PDF_EXPORT_DIR, os.path.splitext(drive_file.name)[0] + ".pdf"
        )
        if os.path.exists(target_path):
            self._logger.info(f"Syncing {drive_file.name} to {target_path}")
            with open(target_path, "wb") as fobj:
                fobj.write(self._drive_client.download_pdf(drive_file.drive_id))

    def _import_drive_file(self, drive_file: DriveFile, base_dir: str) -> None:
        johnny = JohnnyDecimal.parse(drive_file.name)
        target_path = johnny.fit_path(base_dir) + ".rst"
        if not self._is_modified(target_path, drive_file):
            self._logger.info(f"{drive_file.name} already in sync with {target_path}")
            return
        self._logger.info(f"Syncing {drive_file.name} to {target_path}")
        with tempfile.TemporaryDirectory() as temp_dir:
            self._extract_zip_from_bytes(
                self._drive_client.download_doc(
                    drive_file.drive_id,
                    mime_type="application/zip",
                ),
                temp_dir,
            )
            source_html_path = glob.glob(os.path.join(temp_dir, "*.html"))[0]
            self._clean_html(source_html_path, johnny.full_index)
            temp_output = os.path.join(temp_dir, f"{johnny.file_name}.rst")
            self._pandoc_client.html_to_rst(source_html_path, temp_output)
            self._add_preamble(temp_output, johnny.name, drive_file.modified_time)
            self._copy_result_to_destination(source_html_path, os.path.dirname(target_path))

    def _clean_html(self, file_path: str, prefix: str) -> None:
        self._html_cleaner(file_path, prefix)

    def _copy_result_to_destination(self, source_html_path: str, target_dir: str) -> None:
        os.unlink(source_html_path)
        source_dir = os.path.dirname(source_html_path)
        shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)

    def _add_preamble(self, file_path: str, title: str, modified_time: str) -> None:
        with open(file_path, "rt", encoding="utf-8") as fobj:
            content = fobj.read()
        with open(file_path, "wt", encoding="utf-8") as fobj:
            if title.lower() not in content.lower():
                fobj.write(f'{title}\n{"=" * len(title)}\n\n')
            fobj.write(self._format_modified_time(modified_time) + "\n" + content)

    def _is_modified(self, target_path: str, drive_file: DriveFile) -> bool:
        if not os.path.exists(target_path):
            return True
        with open(target_path, "rt", encoding="utf-8") as fobj:
            return self._format_modified_time(drive_file.modified_time) not in fobj

    def _format_modified_time(self, modified_time: str) -> str:
        return f".. modified_time: {modified_time}\n"

    def _extract_zip_from_bytes(self, content: bytes, target_dir: str) -> None:
        with zipfile.ZipFile(io.BytesIO(content)) as zip_file:
            zip_file.extractall(target_dir)


def build_docs_importer():
    return DocsImporter(
        pandoc_client=PandocClient(),
        drive_client=DriveClient(GoogleAuth(ShelveCache(CACHE_FILE_NAME)).get_credentials()),
        logger=logging.getLogger(__name__),
        html_cleaner=HTMLCleaner(),
    )
