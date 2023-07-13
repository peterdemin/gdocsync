import os
import subprocess
import tempfile


class PandocClient:
    def convert_to_rst(self, source_bytes: bytes, target_path: str, extension: str = "odt") -> None:
        target_dir = os.path.dirname(target_path)
        with tempfile.TemporaryDirectory() as temp_dir:
            source_name = os.path.join(temp_dir, f"source.{extension}")
            with open(source_name, "wb") as f_in:
                f_in.write(source_bytes)
            os.system(f"pandoc {source_name} -o {target_path} --extract-media {target_dir}")

    def html_to_rst(self, source_path: str, target_path: str) -> None:
        subprocess.check_call(
            ("pandoc", source_path, "-o", os.path.basename(target_path)),
            cwd=os.path.dirname(target_path),
        )
