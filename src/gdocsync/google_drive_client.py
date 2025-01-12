import json
import os.path
from dataclasses import dataclass
from typing import List, cast

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .shelve_cache import ShelveCache

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


@dataclass
class DriveFile:
    drive_id: str
    name: str
    modified_time: str
    mime_type: str


class GoogleAuth:
    _CREDENTIALS_PATH = os.path.expanduser("~/.gcp/credentials.json")

    def __init__(self, cache: ShelveCache) -> None:
        self._cache = cache

    def get_credentials(self) -> Credentials:
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        with self._cache.session() as cache:
            if token := cache.get("token"):
                creds = Credentials.from_authorized_user_info(token, SCOPES)
            else:
                creds = None
            # If there are no (valid) credentials available, let the user log in.
            fresh = False
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                    except RefreshError:
                        pass
                    else:
                        fresh = True
                if not fresh:
                    flow = InstalledAppFlow.from_client_secrets_file(self._CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                cache["token"] = json.loads(creds.to_json())
            return creds


class DriveClient:
    def __init__(self, creds) -> None:
        self._service = build("drive", "v3", credentials=creds)

    def list_files(self) -> List[DriveFile]:
        """Iterates names and ids of the first 100 files the user has access to."""
        return [
            DriveFile(
                drive_id=item["id"],
                name=item["name"],
                modified_time=item["modifiedTime"],
                mime_type=item["mimeType"],
            )
            for item in self._list_file_fields()
        ]

    def _list_file_fields(self) -> List[dict]:
        """Iterates names and ids of the first 100 files the user has access to."""
        return cast(  # Google library claims return type as list of File objects, but it's not
            List[dict],
            self._service.files()  # pylint: disable=no-member
            .list(
                pageSize=100,
                fields="nextPageToken, files(id, name, modifiedTime, mimeType)",
                orderBy="modifiedTime desc",
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
            )
            .execute()
            .get("files", []),
        )

    def download_doc(self, drive_file_id: str, mime_type: str) -> bytes:
        """Downloads the doc given drive file ID as bytes.

        Supported mime types:

        - Microsoft Word
          application/vnd.openxmlformats-officedocument.wordprocessingml.document .docx
        - OpenDocument application/vnd.oasis.opendocument.text .odt
        - Rich Text application/rtf .rtf
        - PDF application/pdf .pdf
        - Plain Text text/plain .txt
        - Web Page (HTML) application/zip .zip
        - EPUB application/epub+zip .epub

        Reference:
        https://developers.google.com/drive/api/guides/ref-export-formats
        """
        return (
            self._service.files()  # pylint: disable=no-member
            .export(fileId=drive_file_id, mimeType=mime_type)
            .execute()
        )

    def download_pdf(self, drive_file_id: str) -> bytes:
        return (
            self._service.files()  # pylint: disable=no-member
            .export(fileId=drive_file_id, mimeType="application/pdf")
            .execute()
        )
