from .pandoc_client import PandocClient
from .johnny_decimal import JohnnyDecimal
from .shelve_cache import ShelveCache
from .constants import CACHE_FILE_NAME
from .google_drive_client import DriveClient, GoogleAuth


def sync_johnny_decimal_drive_files(base_dir: str):
    cache = ShelveCache(CACHE_FILE_NAME)
    pandoc_client = PandocClient()
    drive_client = DriveClient(GoogleAuth(cache).get_credentials())
    for drive_file in cache.wrap_callable("files", drive_client.list_files):
        if not JohnnyDecimal.is_valid(drive_file.name):
            continue
        johnny = JohnnyDecimal.parse(drive_file.name)
        target_path = johnny.fit_path(base_dir) + ".rst"
        print(f"Syncing {drive_file.name} to {target_path}")
        rst_content = pandoc_client.convert_rtf_to_rst(
            drive_client.download_doc(drive_file.drive_id)
        )
        with open(target_path, "wt", encoding="utf-8") as f_target:
            f_target.write(f'{johnny.name}\n{"=" * len(johnny.name)}\n\n')
            f_target.write(rst_content)


if __name__ == "__main__":
    sync_johnny_decimal_drive_files()
