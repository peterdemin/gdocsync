import json
import os.path
from dataclasses import dataclass
from typing import List

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
    md5: str = ""


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
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
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
            DriveFile(drive_id=item["id"], name=item["name"])
            for item in self._service.files()  # pylint: disable=no-member
            .list(pageSize=100, fields="nextPageToken, files(id, name)")
            .execute()
            .get("files", [])
        ]

    def download_doc(self, drive_file_id: str, mime_type="application/rtf") -> bytes:
        return (
            self._service.files()  # pylint: disable=no-member
            .export(fileId=drive_file_id, mimeType=mime_type)
            .execute()
        )
